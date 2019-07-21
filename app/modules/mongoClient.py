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
        userdata={"openid":openid,"userInfo":None,"courseware":[]}
        if self.client.userData["user"].find_one({"openid":openid})==None:
            #正常使用情况下不会出现重复
            self.client.userData["user"].insert_one(userdata)

    def setUserInfo(self,openid,userInfo):
        self.client.userData["user"].update_one(
            {"openid": openid},
            {
                "$set": {
                    "userid": userInfo['userid'],
                    "userInfo": userInfo
                }
            }
        )

    def getUserInfo(self,openid='',userid=''):
        """
        获取用户全部信息
        :param openid:
        :return: userInfo
        """
        if openid!='':
            getUserInfoResult=self.client.userData["user"].find_one({"openid":openid})
        else:
            getUserInfoResult=self.client.userData["user"].find_one({"userid":userid})
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
        getCoursewareResult = self.client.userData["user"].find_one({"openid": openid})["courseware"]
        #获取当前收藏课件
        if not courseware in getCoursewareResult:
            #去重
            getCoursewareResult.append(courseware)
            newCoursewareList=getCoursewareResult
            #添加新课件
            self.client.userData["user"].update_one(
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
        getCoursewareResult = self.client.userData["user"].find_one({"openid": openid})["courseware"]
        # 获取当前收藏课件
        for i in range(len(getCoursewareResult)):
            if getCoursewareResult[i]['url']==courseware['url']:
                getCoursewareResult.pop(i)
                break
        # 删除
        self.client.userData["user"].update_one(
            {"openid": openid},
            {
                "$set": {
                    "courseware": getCoursewareResult
                }
            }
            )

    def getCourseware(self, openid):
        """
        :param openid:
        :return: getCoursewareResult(列表)
        """
        getCoursewareResult=self.client.userData["user"].find_one({"openid":openid})["courseware"]
        return getCoursewareResult

    def getFavorite(self,openid):
        favoriteDict={}
        favoriteDict["courseware"]=self.getCourseware(openid)
        return favoriteDict

    def saveFeedback(self,feedback):
        """
        :param feedback:
        :return:
        """
        self.client.feedback["msg"].insert_one(feedback)

    def getFeedback(self):
        fb=self.client.feedback["msg"].find({'answered':False})
        res=[]
        for item in fb:
            item.pop("_id")
            res.append(item)
        return res

    def answerFeedback(self,formId):
        self.client.feedback["msg"].update_one({"formId":formId},{"$set":{"answered":True}})

    def newFile(self,id,courseware):
        """
        :param id:
        :param courseware:
        :return:
        """
        tempfileData={"id":id,"courseware":courseware,"time":time.time()}
        self.client.file["tempfile"].insert_one(tempfileData)

    def getFile(self,id):
        """
        :param id:
        :return:
        """
        getCoursewareResult = self.client.file["tempfile"].find_one({"id":id})
        return getCoursewareResult