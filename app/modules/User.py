from app.utils.DB import DB
from app.modules.Courseware import Courseware
from app.modules.Course import Course
from app.utils.Net import getNetInfo
import requests
import json
from setting import *


class User():
    def __init__(self, openid):
        data = DB.c.myNCUT.User.find_one({"openid": openid}, {"_id": 0})
        self.sno = data.get("sno")
        self.sex = data.get("sex")
        self.nickName = data.get("nickName")
        self.avatarUrl = data.get("avatarUrl")
        self.name = data.get("name")
        self.openid = openid
        self.courseware = data.get("courseware")
        # 此处为了防止和关键字冲突将class改为clazz
        self.clazz = data.get("class")
        self.college = data.get("college")
        self.source = data.get("source")
        data.pop("courseware")
        self.baseData = data

    @staticmethod
    def fromSno(sno):
        data = DB.c.myNCUT.User.find_one({"sno": sno}, {"_id": 0})
        if data is None:
            return None
        data.pop("openid")
        data.pop("courseware")
        return data

    @staticmethod
    def OAuth(openid: str, code: str):
        '''
        筛选从云校服务器上拿到的数据，返回筛选后的用户信息
        :param code:
        '''
        data = {
            'appid': yxAPPID,
            'appsecret': yxAPPSECRET
        }
        res = requests.get(
            'https://ucpay.ncut.edu.cn/open/api/access/token', params=data)
        data = {
            'code': code,
            'access_token': json.loads(res.text)['d']['access_token']
        }
        res = requests.get(
            'https://ucpay.ncut.edu.cn/open/user/user/user-by-code', params=data)
        tempInfo = json.loads(res.text)
        userInfo = {
            "openid": openid,
            "courseware": [],
        }
        if tempInfo['d']['sex'] == 1:
            userInfo['sex'] = "男"
        else:
            userInfo['sex'] = "女"
        userInfo['sno'] = tempInfo['d']['userid']
        userInfo['name'] = tempInfo['d']['name']
        DB.c.myNCUT.User.insert(userInfo)
        return User(openid)

    def update(self):
        '''
        更新头像和昵称
        '''
        DB.c.myNCUT.User.update_one(
            {"openid": self.openid},
            {"$set": {
                "avatarUrl": self.avatarUrl,
                "nickName": self.nickName
            }}
        )

    def getNetInfo(self):
        '''
        获取用户校网信息
        TODO 完善文档，写明网络数据含义
        :return:
        '''
        return getNetInfo(self.sno)

    def getCourseList(self):
        '''
        获取该用户的课程列表
        :return: 课程列表
        '''
        return Course.getAll(self.sno)

    def addCourseware(self, id):
        '''
        添加课件收藏
        通过[addToSet]去重
        :param id: 课件id
        :return:
        '''
        DB.c.myNCUT.User.update_one(
            {"openid": self.openid},
            {"$addToSet": {"courseware": id}}
        )

    def getCourseware(self):
        '''
        获取收藏的全部课件
        :return:
        '''
        cwList = []
        for id in self.courseware:
            cwList.append(Courseware.getOne(id))
        return cwList

    def delCourseware(self, id):
        '''
        删除一个课件
        :param id:
        :return: 成功返回True，失败False
        '''
        if id not in self.courseware:
            return False
        self.courseware.pop(self.courseware.index(id))
        DB.c.myNCUT.User.update_one(
            {"openid": self.openid},
            {"$set": {"courseware": self.courseware}}
        )
        return True
