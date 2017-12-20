# -*- coding=UTF-8 -*-

import sys, shutil
import xml.dom.minidom
from mymongodb import *
from dealpage import *
from dealfile import *

class Manage(object):
    def __init__(self):
        self.num = 1

    def ReadSet(self):
        inpath = ""
        outpath = ""
        Databaseip = ""
        Databaseport = 0
        ResultData = {}
        if os.path.exists("set.conf"):
            dom = xml.dom.minidom.parse('set.conf')
            data = dom.documentElement
            try:
                inpath = data.getElementsByTagName("inpath")[0].childNodes[0].data
                outpath = data.getElementsByTagName("outpath")[0].childNodes[0].data
                Databaseip = data.getElementsByTagName("Databaseip")[0].childNodes[0].data
                Databaseport = data.getElementsByTagName("Databaseport")[0].childNodes[0].data
                try:
                    Databaseport = int(Databaseport)
                except:
                    Databaseport = 27017
                Nodes = data.getElementsByTagName("Database")
                if Nodes:
                    database = Nodes[0].getAttribute("name")
                    if database:
                        val = Nodes[0].childNodes[0].data
                        if val:
                            ResultData["database"] = database
                            ResultData["table"] = val
            except:
                print "The configuration information is incomplete"
                sys.exit(0)
        return inpath, outpath, Databaseip, Databaseport, ResultData

    def ReadFile(self, inpath):
        fileslist = []
        dirlist = []
        try:
            for rt, dirs, files in os.walk(inpath):
                for file in files:
                    name = os.path.join(rt, file)
                    fileslist.append(name)
                for d in dirs:
                    path = os.path.join(rt, d)
                    dirlist.append(path)
        except Exception as e:
            logger.warning("readfile() read %s failed" % inpath)
        return fileslist, dirlist

    def GetPath(self, outpath):
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        pathname = time.strftime('%Y%m%d', time.localtime(time.time()))
        path = os.path.join(outpath, pathname)
        if not os.path.exists(path):
            os.mkdir(path)
            self.num = 1
        return path

    def DelNulldir(self, dirlist):
        pathname = time.strftime('%Y%m%d', time.localtime(time.time()))
        for i in range(0, len(dirlist)):
            for dd in dirlist:
                if os.path.exists(dd):
                    if (not os.listdir(dd)) and (pathname not in dd):
                        os.rmdir(dd)
                        dirlist.remove(dd)
                        logger.info("delete %s success!" % dd)
            if len(dirlist) == 0:
                break

    def ChangeName(self, filenewname):
        filename = filenewname
        try:
            i = 1
            while os.path.exists(filename):
                filename = os.path.splitext(filenewname)[0] + "_" + str(i) + os.path.splitext(filenewname)[1]
                i += 1
        except Exception as e:
            logger.warning("changename " + str(e))
        return filename

    def Judgedir(self, path, file):
        nfile = ""
        while True:
            filepath = os.path.join(path, str(self.num))
            if os.path.exists(filepath):
                num = sum([len(x) for _, _, x in os.walk(filepath)])
                if num < 5000:
                    nfile = os.path.join(filepath, os.path.basename(file))
                    break
            else:
                os.mkdir(filepath)
                nfile = os.path.join(filepath, os.path.basename(file))
                break
            self.num += 1
        return nfile

    def ExtractData(self,source_path, file, path, db, table):
        try:
            info = {}
            check = {"phone": "", "email": "", "address":"", "online_account": {}, "copyright": "","co_name":"", "logo_text": "",
                     "logo_alt": ""}
            info, count = DealPage(source_path,file).GetInfo()
            if cmp(info, check) != 0:
                # print info
                strr = os.path.basename(file)
                info["domain"] = strr[:strr.find('_')]
                # raw_input("#")
                try:
                    db.Save(info, table)
                    os.remove(file)
                except Exception as e:
                    logger.warning("Manage::Run()--" + str(e))
            else:
                # raw_input("*")
                newpath = os.path.join(path, "error")
                if not os.path.exists(newpath):
                    os.mkdir(newpath)
                newfile = self.Judgedir(newpath, os.path.basename(file))
                if newfile:
                    newfile = self.ChangeName(newfile)
                    shutil.move(file, newfile)
                    logger.warning(file + "-- no information")
            return count
        except Exception as e:
            logger.warning("Manage::ExtractData()--")

    def Run(self, inpath, outpath, Databaseip, Databaseport, ResultData):
        try:
            db = Mymongodb(Databaseip, Databaseport, ResultData["database"])
            flist, dirlist = self.ReadFile(inpath)
            fileslist = []
            filelist = []
            for a in flist:
                if (os.path.splitext(a)[1] == ".tar") or (os.path.splitext(a)[1] == ".gz"):
                    fileslist.append(a)
                elif os.path.splitext(a)[1] == ".html":
                    filelist.append(a)
                else:
                    os.remove(a)
            path = self.GetPath(outpath)
            if filelist:
                count = 0
                for file in filelist:
                    count += self.ExtractData(os.path.split(file)[0],file, path, db, ResultData["table"])
                # print count
            if fileslist:
                for filename in fileslist:
                    dirpath = DealFile(filename).getpath()
                    if dirpath:
                        newfile = os.path.join(path, os.path.basename(filename))
                        newfile = self.ChangeName(newfile)
                        shutil.move(filename, newfile)
                        if os.path.exists(newfile):
                            content = "move %s success" % os.path.basename(filename)
                            logger.info(content)
                        elif os.path.exists(filename):
                            content = "move %s fialed" % os.path.basename(filename)
                            logger.info(content)
                        else:
                            content = "%s is not existed" % os.path.basename(filename)
                            logger.info(content)
                        files, newdirlist = self.ReadFile(dirpath)
                        for file in files:
                            if os.path.splitext(file)[1] == ".html":
                                self.ExtractData(filename,file, path, db, ResultData["table"])
                            else:
                                os.remove(file)
                        if newdirlist:
                            for d in newdirlist:
                                os.rmdir(d)
                        if os.path.exists(dirpath):
                            os.rmdir(dirpath)
            if dirlist:
                self.DelNulldir(dirlist)
        except Exception as e:
            logger.warning("Manage::Run()--" + str(e))

if __name__ == "__main__":
    m = Manage()
    inpath, outpath, Databaseip, Databaseport, ResultData = m.ReadSet()
    if os.path.exists(inpath):
        m.Run(inpath, outpath, Databaseip, Databaseport, ResultData)
    else:
        Warning("inpath isn't exists")