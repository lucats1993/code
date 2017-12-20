# -*- coding=UTF-8 -*-

from pymongo import *

class Mymongodb(object):
    def __init__(self, Databaseip, Databaseport, Databasename):
        self.client = MongoClient(Databaseip, Databaseport)
        self.db = self.client[Databasename]

    def Save(self, data, Databasetable):
        self.db[Databasetable].save(data)