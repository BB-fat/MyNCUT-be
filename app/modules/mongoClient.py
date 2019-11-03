from pymongo import MongoClient
from setting import *
import random
import time
class mongoClient ():
    def __init__(self,debug):
        """
        数据库初始化，初始化userInfo集合
        """
        if debug:
            self.client =MongoClient(DATABASEIP,DATABASEPORT)
        else:
            self.client = MongoClient(DATABASEIP, DATABASEPORT, username=DB_USER, password=DB_PASSWD)

    def newUser(self,openid):
        """
        插入用户信息
        :param openid:
        :return:
        userData 数据库
        user 集合（openid 字段、userInfo 字段）
        """
        userdata={
            "openid":openid,
            "userid":None,
            "name":None,
            "avatar":None,
            "sex":None,
            "courseware":[]
        }
        self.client.myNCUT.User.insert_one(userdata)

    def setUserInfo(self,openid,userInfo):
        self.client.myNCUT.User.update_one(
            {"openid": openid},
            {
                "$set": {**userInfo}
            }
        )

    def getUserInfo(self,openid='',userid=''):
        """
        获取用户全部信息
        :param openid:
        :return: userInfo
        """
        if openid!='':
            getUserInfoResult=self.client.myNCUT.User.find_one({"openid":openid},{"_id":0})
        else:
            getUserInfoResult=self.client.myNCUT.User.find_one({"userid":userid},{"_id":0})
        return getUserInfoResult

    def getPublicInfo(self):
        """
        获取新闻信息
        :return: {"indexBannner":,"indexNotice":}
        """
        bannner=[]
        notice=[]
        for eachBanner in self.client.publicInfo["indexBanner"].find({},{"_id":0}):
            bannner.append(eachBanner)
        for eachNotice in self.client.publicInfo["indexNotice"].find({},{"_id":0}):
            notice.append(eachNotice)
        return {"indexBanner":bannner,"indexNotice":notice}

    def addCourseware(self,openid,courseware):
        """
        :param openid:
        :param courseware: 新课件，字典形式
        :return:
        """
        self.client.myNCUT.User.update_one(
            {"openid": openid},
            {
                "$addToSet": {
                    "courseware":courseware
                }
            }
        )

    def deleteCourseware(self,openid,courseware):
        """
        :param openid:
        :param courseware:
        :return:
        """
        self.client.myNCUT.User.update_one(
            {"openid": openid},
            {
                "$pull": {
                    "courseware": {"url":courseware["url"]}
                }
            }
        )

    def getFavorite(self, openid):
        """
        :param openid:
        :return: getCoursewareResult(列表)
        """
        favourite=self.client.myNCUT.User.find_one({"openid":openid})["courseware"]
        return favourite

    def newFile(self,id,courseware):
        """
        :param id:
        :param courseware:
        :return:
        """
        tempfileData={"id":id,"courseware":courseware,"time":time.time()}
        self.client.myNCUT.File.insert_one(tempfileData)

    def getFile(self,id):
        """
        :param id:
        :return:
        """
        f = self.client.myNCUT.File.find_one({"id":id})
        return f

    def createTrade(self,openid,pay_money,order,url):
        '''
        在数据库中生成交易订单
        '''
        self.client.myNCUT.Trade.insert_one({
            "openid":openid,
            "type":order[:2],
            "time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "pay_money":pay_money,
            "state":1,
            "order":order,
            "url":url
        })

    def getTradeHistory(self,openid,type):
        '''
        返回某用户特定类型交易的全部历史数据
        '''
        data=[]
        for i in self.client.myNCUT.Trade.find({"type":type,"openid":openid}):
            i.pop("_id")
            data.append(i)
        return data