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
        if self.client.myNCUT.User.find_one({"openid":openid})==None:
            #正常使用情况下不会出现重复
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
            getUserInfoResult=self.client.myNCUT.User.find_one({"openid":openid})
        else:
            getUserInfoResult=self.client.myNCUT.User.find_one({"userid":userid})
        if getUserInfoResult is not None:
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

    def addCourseware(self,openid,courseware):
        """
        :param openid:
        :param courseware: 新课件，字典形式
        :return:
        """
        getCoursewareResult = self.client.myNCUT.User.find_one({"openid": openid})["courseware"]
        #获取当前收藏课件
        if not courseware in getCoursewareResult:
            #去重
            getCoursewareResult.append(courseware)
            newCoursewareList=getCoursewareResult
            #添加新课件
            self.client.myNCUT.User.update_one(
                {"openid": openid},
                {
                    "$set": {
                        "courseware":newCoursewareList
                    }
                }
            )

    def deleteCourseware(self,openid,courseware):
        """
        :param openid:
        :param courseware:
        :return:
        """
        getCoursewareResult = self.client.myNCUT.User.find_one({"openid": openid})["courseware"]
        # 获取当前收藏课件
        for i in range(len(getCoursewareResult)):
            if getCoursewareResult[i]['url']==courseware['url']:
                getCoursewareResult.pop(i)
                break
        # 删除
        self.client.myNCUT.User.update_one(
            {"openid": openid},
            {
                "$set": {
                    "courseware": getCoursewareResult
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