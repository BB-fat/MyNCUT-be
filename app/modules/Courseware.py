from app.utils.DB import DB
import requests
import datetime


class Courseware():

    @staticmethod
    def fileStream(cw):
        '''
        从多模式服务器请求并生成文件流
        '''
        req = requests.get(cw["url"], stream=True)
        for chunk in req.iter_content(1024*100):
            yield chunk

    @staticmethod
    def makeUrl(id):
        data = Courseware.getOne(id)
        if data is not None:
            tempFile = {
                "id": data["_id"],
                "createTime": datetime.datetime.utcnow()
            }
            DB.c.myNCUT.TempFile.insert_one(tempFile)
            return str(tempFile["_id"])
        else:
            return None

    @staticmethod
    def publicDownload(id: str):
        '''
        传入临时文件id
        返回真实文件id
        '''
        try:
            tempFile = DB.c.myNCUT.TempFile.find_one(
                {"_id": DB.str2ObjectId(id)})
        except:
            return None
        if tempFile is None:
            return None
        else:
            return tempFile["id"]

    @staticmethod
    def getOne(id: str):
        '''
        根据id查询并返回一个课件字典
        '''
        try:
            cw = DB.c.myNCUT.Courseware.find_one({"_id": DB.str2ObjectId(id)})
        except:
            return None
        cw["_id"] = str(cw["_id"])
        return cw
