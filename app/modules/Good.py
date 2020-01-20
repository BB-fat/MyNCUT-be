from app.utils.DB import DB
import datetime
import re


class Good():

    @staticmethod
    def create(data, user):
        DB.c.myNCUT.Goods.insert_one({
            "title": data.get("title"),
            "time": datetime.datetime.utcnow(),
            "describe": data.get("describe"),
            "price": float(data.get("price")),
            "photos": data.get("photos").split(","),
            "state": 1,
            "owner": user.sno,
            "contact": data.get("contact")
        })

    @staticmethod
    def findById(_id):
        try:
            _id = DB.str2ObjectId(_id)
        except:
            return None
        g = DB.c.myNCUT.Goods.find_one({"_id": _id})
        g["_id"] = str(g["_id"])
        g["time"] = str(g["time"])
        return g

    @staticmethod
    def findByArgs(args):
        args = args.to_dict()
        if args.get("state") is not None:
            args["state"] = int(args["state"])
        if args.get("title") is not None:
            args["title"] = re.compile(args.get("title"))
        goods = DB.c.myNCUT.Goods.find(args).sort("time",-1)
        res = []
        for item in goods:
            item["_id"] = str(item["_id"])
            item["time"] = str(item["time"])
            res.append(item)
        return res

    @staticmethod
    def update(_id, data):
        try:
            _id = DB.str2ObjectId(_id)
        except:
            return False
        new = {
            "title": data.get("title"),
            "time": datetime.datetime.utcnow(),
            "describe": data.get("describe"),
            "state":int(data.get("state")),
            "contact": data.get("contact")
        }
        if data.get("price")is not None:
            new["price"] = float(data.get("price"))
        if data.get("photos")is not None:
            new["photos"] = data.get("photos").split(",")
        submitData = {}
        for k in new:
            if new[k]is not None:
                submitData[k] = new[k]
        DB.c.myNCUT.Goods.update_one({"_id": _id}, {"$set": submitData})
        return True
