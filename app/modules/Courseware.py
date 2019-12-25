from app.utils.DB import DB
import requests
import datetime


class Courseware():
    def __init__(self, data):
        self.type = data.get("type")
        self.size = data.get("size")
        self.date = data.get("date")
        self.filename = data.get("filename")
        self.url = data.get("url")
        self.code = data.get("course_code")

    @staticmethod
    def privateDowmload(course_code, filename):
        data = DB.c.myNCUT.Courseware.find_one({"course_code": course_code, "filename": filename})
        if data is not None:
            return requests.get(data["url"]).content
        else:
            return None

    @staticmethod
    def makeUrl(course_code, filename):
        data = DB.c.myNCUT.Courseware.find_one({"course_code": course_code, "filename": filename})
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
        tempFile = None
        try:
            tempFile = DB.c.myNCUT.TempFile.find_one({"_id": DB.str2ObjectId(id)})
        except:
            pass
        if tempFile is None:
            return None, None
        else:
            courseware = DB.c.myNCUT.Courseware.find_one({"_id": DB.str2ObjectId(tempFile["id"])})
            return courseware["filename"], requests.get(courseware["url"]).content
