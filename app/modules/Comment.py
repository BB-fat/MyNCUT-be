from app.utils.DB import DB
from app.modules.User import User
import datetime


class Comment():
    @staticmethod
    def get(good_id):
        '''
        获取某个物品的所有评论数据
        '''
        res = DB.c.myNCUT.Comment.find(
            {"good_id": good_id}).sort("create_time")
        comments = []
        for comment in res:
            comment["_id"] = str(comment["_id"])
            comment["create_time"] = str(comment["create_time"])
            comment["from"] = DB.c.myNCUT.User.find_one(
                {"openid": comment["from_openid"]}, {"_id": 0})
            comment["to"] = DB.c.myNCUT.User.find_one(
                {"openid": comment["to_openid"]}, {"_id": 0})
            comments.append(comment)
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
