from pymongo import MongoClient
from setting import *
class mongoInit ():
    def __init__(self):
        """
        Fix
        数据库初始化，初始化userInfo集合
        """
        client =MongoClient(DATABASEIP,27017)
        #Fix
        userDatabase=client.userDatabase
        #userData库
        userInfo=userDatabase["userInfo"]
        #集合userInfo
