# -*- coding=UTF-8 -*-
import re
import sys
from log import *
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')
from log import *
from co_name import CoName

class DealPage():
    def __init__(self,source_path, name):
        # print source_path
        self.source_path=source_path
        self.name = name
        self.count = 0
        # self.info = {"phone": "", "email": "", "address": "", "online_account": {}, "copyright": "", "logo_text": "",
        #              "logo_alt": ""}
        self.info = {"file_name":"","copyright": "","co_name":""}
        self.content = ""
        try:
            with open(self.name, 'r') as f:
                self.content = f.read()
            if self.content:
                self.tree = etree.HTML(self.content)
                self.Extract()
        except Exception as e:
            logger.info(self.name + "--DealPage()--" + str(e))

    def Extract(self):
        try:
            self.ExtractLocation()
            self.ExtractCopyright()
            self.ExtractCoName()
            # self.ExtractLogoText()
            # self.ExtractAll()
            # self.ExtractPhone()
            # self.ExtractEmail()
            # self.ExtractAddress()
            # self.ExtractOnlien()
        except Exception as e:
            logger.warning(self.name + "--DealPage::extract()--" + str(e))
    def ExtractLocation(self):
        file_location=os.path.split(self.source_path)
        if file_location:
            self.info["file_name"] = file_location[1]
            # print file_location[1]

    def ExtractCopyright(self):
        # 过滤一些干扰元素
        html = self.content
        try:
            co = CoName(html)
            copyright = co.get_copyright()
            # print copyright
        except Exception as e:
            logger.warning(self.name + "--copyright--" + str(e))
        else:
            if copyright:
                self.info["copyright"] = copyright

    def ExtractCoName(self):
        # 过滤一些干扰元素
        html = self.content
        try:
            copyright = self.info.get('copyright')
            if copyright.strip():
                co_name = CoName.get_co_name(copyright)
                print co_name
            else:
                co_name=''
        except Exception as e:
            logger.warning(self.name + "--co_name--" + str(e))
        else:
            if copyright:
                self.info["co_name"] = co_name


    # def ExtractCopyright(self):
    #     try:
    #         node = self.tree.xpath('//body//div[@class="footer"]//div[@class="fl"]')
    #         if node:
    #             self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//footer[@id="footer"]//div[@class="footer-btm"]//span')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@id="mjs-browser"]//div[@id="mjs-object_66"]'
    #                                    '//div[@class="mjs-object-content"]//span')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@class="bottomBox"]//div[@class="link tc clearfix"]//p[@class="p3"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@id="copyright"]//div[@class="copyright-text copyright-col1"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)').replace('\t', '').replace('\n', '')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//footer[@class="art-footer"]'
    #                                    '//div[@class="art-layout-cell layout-item-1"]//span')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@class="footer"]//p')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@id="footer_wrap"]//div[@id="copyright"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)').replace('\t', '').replace('\n', '')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@class="footertext"]//div[@class="footertextleft"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@id="ja-footer"]//div[@class="ja-copyright"]//div[not(@class)]')
    #             if node:
    #                 self.info["copyright"] = re.findall("Copyright(.*)", node[0].xpath('string(.)'))[0]
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@class="container"]//div[@class="oi_footer"]'
    #                                    '//div[@class="col-md-12"]')
    #             if node:
    #                 self.info["copyright"] = re.sub('\s\s+', ' ', node[0].xpath('string(.)').replace('\n', ''))
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//footer[@id="footer"]//div[@id="copyright"]//p')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@id="footer"]')
    #             if node:
    #                 text = node[0].xpath('string(.)')
    #                 if (("Copyright" in text) or ("copyright" in text)):
    #                     self.info["copyright"] = text.replace('\t', '').replace('\n', '')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//footer//div[@class="copyright"]')
    #             if node:
    #                 self.info["copyright"] = re.sub('\s\s+', ' ', node[0].xpath('string(.)').replace('\n', ''))
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@class="footer-btm-wrapper"]//div[@class="footer-btm"]//span')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//div[@id="footer"]//p[@id="copyrightText"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//td[@class="copyright"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//footer[@class="footer"]//div[@class="footer__bottom"]//p[@class="footer__botom__left"]')
    #             if node:
    #                 self.info["copyright"] = node[0].xpath('string(.)')
    #         if not self.info["copyright"]:
    #             node = self.tree.xpath('//body//footer//section[@id="footer-area"]')
    #             if node:
    #                 text = node[0].xpath('string(.)')
    #                 if (("Copyright" in text) or ("copyright" in text)):
    #                     self.info["copyright"] = text.replace('\t', '').replace('\n', '')
    #         content = re.sub('<span.*?>', '', self.content)
    #         content = re.sub('</span>', '', content)
    #         content = re.sub('<a.*?>', '', content)
    #         content = re.sub('</a>', '', content)
    #         print repr(content)
    #         if not self.info["copyright"]:
    #             texts = re.findall('(©[^<]+?)[\n<]', content)
    #             # print texts
    #             if texts:
    #                 for text in texts:
    #                     if text and (len(text) > 2):
    #                         self.info["copyright"] = text
    #         if not self.info["copyright"]:
    #             texts = re.findall('(Copyright[^\"<]+?)[\n<]', content, re.I)
    #             if texts:
    #                 for text in texts:
    #                     if text and (len(text) > 10) and ("copyright-content" not in text):
    #                         self.info["copyright"] = text
    #         # if not self.info["copyright"]:
    #         #     node = self.tree.xpath('//body//div[@id="foottx"]//p[@align="center"]//font')
    #         #     if node:
    #         #         self.info["copyright"] = node[0].xpath('string(.)')
    #         if self.info["copyright"]:
    #             print self.info["copyright"]
    #             self.count = 1
    #     except Exception as e:
    #         logger.warning(self.name + "--DealPage::ExtractCopyright()--" + str(e))

    def ExtractLogoText(self):
        try:
            node = self.tree.xpath('//body//div[@class="navbar navbar-default navbar-fixed-top yamm"]'
                                   '//div[@class="container"]//div[@class="navbar-header"]//img')
            if node:
                self.info["logo_text"] = node[0].xpath('string(.)')
                if node[0].xpath('./@alt'):
                    self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@class="m"]//div[@class="logo f_l"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//header//div[@id="logo"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@class="container"]//div[@class="main2"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//header//a[@class="logo"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@class="oi_head_holder"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//header[@class="header-container"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@class="navbar-header"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@class="logosg"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@class="header"]//div[@class="logo"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
            if (not self.info["logo_text"]) and (not self.info["logo_alt"]):
                node = self.tree.xpath('//body//div[@id="logo"]//img')
                if node:
                    self.info["logo_text"] = node[0].xpath('string(.)')
                    if node[0].xpath('./@alt'):
                        self.info["logo_alt"] = node[0].xpath('./@alt')[0]
        except Exception as e:
            logger.warning(self.name + "--DealPage::ExtractLogoText()--" + str(e))

    def ExtractAll(self):
        try:
            nodes = self.tree.xpath('//body//footer[@id="footer"]//div[@class="container"]//div[@class="footer-col"]')
            if nodes:
                for node in nodes:
                    Node = node.xpath('./h3')
                    if Node:
                        title = Node[0].xpath('string(.)')
                        if "contact" in title:
                            Nodes = node.xpath('.//li/p')
                            for thisnode in Nodes:
                                text = thisnode.xpath('string(.)')
                                if "Address" in text:
                                    self.info["address"] = re.sub('\s\s+', ' ', text[text.find(':'):].replace('\n', '').replace('\t', ' '))
                                if "Email" in text:
                                    self.info["email"] = text[text.find(':'):].replace('\n', '').replace('\t', ' ')
                                if "Phone" in text:
                                    self.info["phone"] = text[text.find(':'):].replace('\n', '').replace('\t', ' ')
            nodes = self.tree.xpath('//body//div[@class="bottomBox"]//div[@class="contact"]//div[@class="fl"]//p')
            if nodes:
                for node in nodes:
                    text = node.xpath('string(.)')
                    if u'服务热线' in text:
                        self.info["phone"] = text[text.find(u'：')+1:text.find(u'（')]
                    if u'客服邮箱' in text:
                        self.info["email"] = text[text.find(u'：')+1:]
                    if u'官方Q群' in text:
                        thisnodes = node.xpath('.//img')
                        if thisnodes:
                            for thisnode in thisnodes:
                                if thisnode.xpath('./@alt'):
                                    name = thisnode.xpath('./@alt')[0]
                                    if name and (not self.info["online_account"].has_key("QQ_group")):
                                        self.info["online_account"]["QQ_group"] = name.encode('utf-8')
                                    elif name and (isinstance(self.info["online_account"]["QQ_group"], str)):
                                        self.info["online_account"]["QQ_group"] = [self.info["online_account"]["QQ_group"]]
                                        self.info["online_account"]["QQ_group"].append(name.encode('utf-8'))
                                    elif name and (isinstance(self.info["online_account"]["QQ_group"], list)):
                                        self.info["online_account"]["QQ_group"].append(name.encode('utf-8'))
            nodes = self.tree.xpath('//body//footer//div[@class="four columns"]//div[@id="contact-2"]//address')
            if nodes:
                for node in nodes:
                    if node.xpath('.//span[@class="email"]//a'):
                        self.info["email"] = node.xpath('.//span[@class="email"]//a')[0].xpath('string(.)')
            nodes = self.tree.xpath('//body//footer//div[@class="textwidget"]//p')
            if nodes:
                text = nodes[0].xpath('string(.)')
                if text:
                    datas = text.split('\n')
                    for data in datas:
                        if "Adresse" in data:
                            if not self.info["address"]:
                                self.info["address"] = data[data.find(':')+1:].encode('utf-8')
                            elif isinstance(self.info["address"], str):
                                self.info["address"] = [self.info["address"]]
                                self.info["address"].append(data[data.find(':')+1:].encode('utf-8'))
                            elif isinstance(self.info["address"], list):
                                self.info["address"].append(data[data.find(':')+1:].encode('utf-8'))
                        else:
                            self.info["phone"] = re.findall("phone:[\s]*(.*?)[\s]*Fax", data)[0]
                            self.info["email"] = re.findall("E-Mail:[\s]*(.*)", data)[0]
            # nodes = self.tree.xpath('//body//div[@id="container"]//div[@id="homeMap"]//ul//li[contains(@class,"location")]')
            # if nodes:
            #     for node in nodes:
            #         print node.xpath('.//div[@class="location-details"]')
        except Exception as e:
            logger.warning(self.name + "--DealPage::ExtractAll()--" + str(e))

    def ExtractPhone(self):
        try:
            if not self.info["phone"]:
                node = self.tree.xpath('//body//div[@id="headeraddress"]//span[@class="telephonenumber"]')
                if node:
                    text = node[0].xpath('string(.)')
                    if text:
                        self.info["phone"] = text[text.find(':'):].replace('\n', '').replace('\t', '')
            if not self.info["phone"]:
                node = self.tree.xpath('//body//div[@id="mjs-browser"]//div[@id="mjs-object_69"]'
                                       '//div[@class="mjs-object-content"]//span')
                if node:
                    self.info["phone"] = node[0].xpath('string(.)')
            if not self.info["phone"]:
                node = self.tree.xpath('//body//div[@class="rightBar"]//li[@class="chat"]//p')
                if node:
                    self.info["phone"] = node[0].xpath('string(.)')
            if not self.info["phone"]:
                node = self.tree.xpath('//body//div[@class="sidebar sidebar-left"]//span[@id="call-us"]')
                if node:
                    self.info["phone"] = node[0].xpath('string(.)')
        except Exception as e:
            logger.warning(self.name + "--DealPage::ExtractPhone()--" + str(e))

    def ExtractEmail(self):
        try:
            if not self.info["email"]:
                node = self.tree.xpath('//body//div[@class="sidebar sidebar-left"]//span[@id="email-us"]')
                if node:
                    self.info["email"] = node[0].xpath('string(.)')
        except Exception as e:
            logger.warning(self.name + "--DealPage::ExtractEmail()--" + str(e))

    def ExtractAddress(self):
        try:
            if not self.info["address"]:
                node = self.tree.xpath('//body//div[@id="headeraddress"]//span[@class="branchaddress"]')
                if node:
                    self.info["address"] = node[0].xpath('string(.)').replace('\n', ' ')
        except Exception as e:
            logger.warning(self.name + "--DealPage::ExtractAddress()--" + str(e))

    def ExtractOnlien(self):
        try:
            nodes = self.tree.xpath('//body//footer[@class="art-footer"]'
                                    '//div[@class="art-layout-cell layout-item-0 responsive-tablet-layout-cell"]//img')
            if nodes:
                for node in nodes:
                    url = node.xpath('../@href')
                    if url:
                        url = url[0]
                        tag = ""
                        if url == "#":
                            url = ""
                        if "linkedin.com" in url:
                            tag = "linkedin"
                        elif "facebook.com" in url:
                            tag = "facebook"
                        if tag and url:
                            self.InsertOnline(tag, url)
            node = self.tree.xpath('//body//div[@class="rightBar"]//li[@class="qq"]//a/@href')
            if node:
                self.InsertOnline("QQ", node[0])
            node = self.tree.xpath('//body//div[@class="rightBar"]//li[@class="xz"]//p')
            if node:
                self.InsertOnline("WeChat", node[0].xpath('string(.)'))
            nodes = self.tree.xpath('//body//div[@class="sidebar sidebar-right"]//div[@class="some-container"]//a')
            if nodes:
                for node in nodes:
                    url = node.xpath('./@href')
                    if url:
                        url = url[0]
                        tag = ""
                        if url == "#":
                            url = ""
                        if "linkedin.com" in url:
                            tag = "linkedin"
                        elif "facebook.com" in url:
                            tag = "facebook"
                        elif "twitter.com" in url:
                            tag = "twitter"
                        elif "behance.net" in url:
                            tag = "behance"
                        elif "instagram.com" in url:
                            tag = "instagram"
                        if tag and url:
                            self.InsertOnline(tag, url)
            node = self.tree.xpath('//body//div[@class="footer"]//div[@class="footer-top"]//a[@class="follow"]')
            if node:
                url = node[0].xpath('./@href')
                if url:
                    url = url[0]
                    tag = ""
                    if url == "#":
                        url = ""
                    if "linkedin.com" in url:
                        tag = "linkedin"
                    if tag and url:
                        self.InsertOnline(tag, url)
        except Exception as e:
            logger.warning(self.name + "--DealPage::ExtractOnlien()--" + str(e))

    def InsertOnline(self, tag, val):
        try:
            if not self.info["online_account"].has_key(tag):
                self.info["online_account"][tag] = val.encode('utf-8')
            elif isinstance(self.info["online_account"][tag], str):
                self.info["online_account"][tag] = [self.info["online_account"][tag]]
                self.info["online_account"][tag].append(val.encode('utf-8'))
            elif isinstance(self.info["online_account"][tag], list):
                self.info["online_account"][tag].append(val.encode('utf-8'))
        except Exception as e:
            logger.warning(self.name + "--DealPage::InsertOnline()--" + str(e))

    def GetInfo(self):
        return self.info, self.count
