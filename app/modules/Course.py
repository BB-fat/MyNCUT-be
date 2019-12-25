import time
import json
import requests
from app.utils.ParseUrl import parseUrl
from app.utils.DB import DB


class Course():

    @staticmethod
    def getCourseware(course_code):
        """
        获取当前课程所有的课件
        """
        res = json.loads(requests.get('http://v.ncut.edu.cn/document', params={"code": course_code}).text)
        if res['data'] == []:
            return None
        wareList = []
        for key, value in res['data'].items():
            tempDict = value
            # 解析url参数
            quote = parseUrl(tempDict['url'])
            tempDict['course_code'] = quote['cidReq']
            tempDict['filename'] = key.split('/')[-1]
            # TODO 将插入优化成1条语句
            tmp = DB.c.myNCUT.Courseware.find_one(tempDict)
            if tmp is None:
                DB.c.myNCUT.Courseware.insert_one(tempDict)
                tempDict["_id"] = str(tempDict["_id"])
            else:
                tempDict["_id"] = str(tmp["_id"])
            wareList.append(tempDict)
        # 按照课件发布时间进行排序
        wareList.sort(key=lambda k: (k.get('date', 0)), reverse=True)
        # 格式化时间
        for i in range(len(wareList)):
            wareList[i]['date'] = time.strftime(
                "%Y-%m-%d", time.localtime(wareList[i]['date']))
        return wareList

    @staticmethod
    def getAll(sno: str):
        courselist = json.loads(
            requests.get('http://v.ncut.edu.cn/course', params={"sno": sno}).text)['data']
        for course in courselist:
            tmpList = course['course_name'].split('：')
            course['course_name'] = '：'.join(tmpList[:-1])
            course['course_class'] = tmpList[-1]
        return courselist[::-1]
