# -*- coding=UTF-8 -*-

import logging, os, time
from logging.handlers import RotatingFileHandler

# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger(object):
    def __init__(self):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        path = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(path,"log")
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path,"log.txt")
        # 创建一个logger
        self.logger = logging.getLogger('main')
        self.logger.setLevel(logging.INFO)
        #创建一个handler，用于写入日志文件
        handler = RotatingFileHandler(filename, maxBytes=10 * 1024 * 1024, backupCount=100)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(handler)

    def GetLog(self):
        return self.logger

logger = Logger().GetLog()