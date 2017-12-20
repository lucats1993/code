# -*- coding=UTF-8 -*-

import tarfile
from log import *

class DealFile():
    def __init__(self, filename):
        self.path = ""
        if os.path.splitext(filename)[1] == ".tar":
            self.dealtar(filename)
        elif os.path.splitext(filename)[1] == ".gz":
            self.dealgz(filename)

    def dealtar(self, filename):
        try:
            tar = tarfile.open(filename, "r")
            file_names = tar.getnames()
            self.path = os.path.splitext(filename)[0]
            for file_name in file_names:
                tar.extract(file_name, self.path)
            tar.close()
        except Exception as e:
            logger.info(filename + " " + str(e))

    def dealgz(self, filename):
        try:
            tar = tarfile.open(filename, "r:gz")
            file_names = tar.getnames()
            filename = os.path.splitext(filename)[0]
            self.path = os.path.splitext(filename)[0]
            for file_name in file_names:
                tar.extract(file_name, self.path)
            tar.close()
        except Exception as e:
            logger.info(filename + " " + str(e))

    def getpath(self):
        return self.path