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
        :return:
        userData 数据库
        user 集合（openid 字段、userInfo 字段）
        """
        userdata={"openid":openid,"userInfo":userInfo,"courseware":[]}
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

    def deleteCourseware(self,openid,index):
        """
        :param openid:
        :param courseware:
        :return:
        """
        getCoursewareResult = self.client.userData["user"].find_one({"openid": openid})["courseware"]
        # 获取当前收藏课件
        getCoursewareResult.pop(index)
        newCoursewareList =getCoursewareResult
        # 删除
        self.client.userData["user"].update_one(
            {"openid": openid},
            {
                "$set": {
                    "courseware": newCoursewareList
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
    def saveFeedback(self,feedback):
        """
        :param feedback:
        :return:
        """
        state=feedback["type"]
        feedback.pop("type")
        feedback["read"]=False
        if state==0:
            self.client.feedback["bug"].insert_one(feedback)
        elif state == 1:
            self.client.feedback["update"].insert_one(feedback)
        elif state == 2:
            self.client.feedback["other"].insert_one(feedback)
    def getFavorite(self,openid):
        favoriteDict={}
        favoriteDict["courseware"]=self.getCourseware(openid)
        return favoriteDict
    def pushFeedback(self):
        pass


