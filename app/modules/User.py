from app.utils.DB import DB
from app.modules.Courseware import Courseware
from app.modules.Course import Course
from app.utils.Net import getNetInfo
import requests
import json


class User():
    def __init__(self, openid):
        data = DB.c.myNCUT.User.find_one({"openid": openid}, {"_id": 0})
        self.sno = data.get("sno")
        self.sex = data.get("sex")
        self.nickName = data.get("nickName")
        self.avatarUrl = data.get("avatarUrl")
        self.name = data.get("name")
        self.openid = openid
        self.courseware = [Courseware(x) for x in data.get("courseware")]
        # 此处为了防止和关键字冲突将class改为clazz
        self.clazz = data.get("class")
        self.college = data.get("college")
        self.source = data.get("source")
        data.pop("courseware")
        self.baseData = data

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
