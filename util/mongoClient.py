from pymongo import MongoClient
from setting import *
class mongoClient ():
    def __init__(self):
        """
        数据库初始化，初始化userInfo集合
        """
        self.client =MongoClient(DATABASEIP,DATABASEPORT)


    def newUser(self,openid,userInfo):
        """
        插入用户信息
        :param openid:
        :param userInfo:
        :return: none
        userData 数据库
        user 集合（openid 字段、userInfo 字段）
        """
        userdata={"openid":openid,"userInfo":userInfo}
        if self.client.userData["user"].find_one({"openid":openid})==None:
            #正常使用情况下不会出现重复
            self.client.userData["user"].insert_one(userdata)

    def getUserInfo(self,openid):
        """
        获取用户全部信息
        :param openid:
        :return: userInfo
        """
        getUserInfoResult=self.client.userData["user"].find_one({"openid":openid})
        if getUserInfoResult!=None:
            getUserInfoResult.pop('_id')
        return getUserInfoResult

    def getPublicInfo(self):
        """
        获取新闻信息
        :return: {"indexBannner":,"indexNotice":}
        """
        bannner=[]
        notice=[]
        for eachBanner in self.client.publicInfo["indexBanner"].find():
            eachBanner.pop('_id')
            bannner.append(eachBanner)
        for eachNotice in self.client.publicInfo["indexNotice"].find():
            eachNotice.pop('_id')
            notice.append(eachNotice)
        return {"indexBanner":bannner,"indexNotice":notice}
