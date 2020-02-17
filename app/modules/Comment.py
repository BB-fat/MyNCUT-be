from app.utils.DB import DB
from app.modules.User import User
import datetime


class Comment():
    @staticmethod
    def processComment(comment):
        comment["_id"] = str(comment["_id"])
        comment["create_time"] = str(comment["create_time"])
        comment["from"] = DB.c.myNCUT.User.find_one(
            {"openid": comment["from_openid"]}, {"_id": 0})
        if comment["to_openid"] is not None:
            comment["to"] = DB.c.myNCUT.User.find_one(
                {"openid": comment["to_openid"]}, {"_id": 0})
        else:
            comment["to"] = None
        return comment

    @staticmethod
    def getOne(_id):
        res = DB.c.myNCUT.Comment.find_one({
            "_id": DB.str2ObjectId(_id)
        })
        return Comment.processComment(res)

    @staticmethod
    def get(good_id):
        '''
        获取某个物品的所有评论数据
        '''
        res = DB.c.myNCUT.Comment.find(
            {"good_id": good_id}).sort("create_time")
        comments = []
        for comment in res:
            comments.append(Comment.processComment(comment))
        return comments

    @staticmethod
    def create(good_id, reply_id, from_openid, to_openid, content):
        DB.c.myNCUT.Comment.insert_one({
            "good_id": good_id,
            "reply_id": reply_id,
            "create_time": datetime.datetime.utcnow(),
            "from_openid": from_openid,
            "to_openid": to_openid,
            "content": content
        })

    @staticmethod
    def delete(_id):
        DB.c.myNCUT.Comment.delete_one({
            "_id": DB.str2ObjectId(_id)
        })
