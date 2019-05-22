from pymongo import MongoClient
from setting import *
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
        state=feedback["type"]
        feedback.pop("type")
        feedback["read"]=False
        if state=='0':
            self.client.feedback["bug"].insert_one(feedback)
        elif state == '1':
            self.client.feedback["update"].insert_one(feedback)
        elif state == '2':
            self.client.feedback["other"].insert_one(feedback)

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

    def getPasswd(self):
        '''
        临时后台的密码
        :return:
        '''
        res=self.client.publicInfo['auth'].find_one({
            "name":"admin"
        })
        return res['passwd']


    def setIndexBanner(self,tempInfo):
        self.client.publicInfo['indexBanner'].update_one(
            {"index":tempInfo['index']},
            {
                "$set":{
                    "msgUrl":tempInfo['msgUrl'],
                    "imgUrl":tempInfo['imgUrl'],
                }
            }
        )


    def setIndexNotice(self,tempInfo):
        self.client.publicInfo['indexNotice'].update_one(
            {"index": tempInfo['index']},
            {
                "$set": {
                    "text": tempInfo['text'],
                }
            }
        )

    def SL_countPlus(self,userid):
        '''
        返回点滴校园计数信息
        :param userid:
        :return:
        '''
        count = self.client.SL2019.count.find_one({"tar": "count"})
        res=self.client.SL2019.user.find_one({"userid": userid})
        if res is None:
            self.client.SL2019.user.insert_one({"userid":userid,"count":count+1})
            self.client.SL2019.count.update_one({"tar":"count"},{"$set":{"count":count+1}})
            return count+1
        else:
            return res['count']