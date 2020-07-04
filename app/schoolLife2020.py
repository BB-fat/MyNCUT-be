from datetime import datetime

from flask import request

from app.modules.User import User
from app.utils.DB import DB
from app import app
from app.modules.Session import Session
from app.utils.MyResponse import responseOK


@app.route("/sl_2020/login" , methods=["GET"])
def sl2020_login():
    openid = Session(request.header.get("Token")).openid
    logined = DB.c.SL2020.user.find({"openid": openid})

    if logined != None:
        num = DB.c.SL2020.count.find_one({"tar": "count"})["count"]
        DB.c.SL2020.count.update({"tar": "count"} , {"$inc": {"count": 1}})
        DB.c.SL2020.user.insert({"openid": openid , "index": num + 1})
    return responseOK(None)


@app.route("/sl_2020/bullet-chat" , methods=["GET" , "POST"])
def bullet_chat():
    if request.method == "GET":
        msgCursor = DB.c.SL2020.msg.aggregate([{"$sample": {"size": 60}}])
        msgList = []
        for i in msgCursor:
            i.pop("_id")
            i.pop("openid")
            i.pop("sendTime")
            msgList.append(i)
        return responseOK(msgList)

    elif request.method == "POST":
        openid = Session(request.form.get("Token")).openid
        msg = request.form.get("msg")
        u = User(openid)
        userType = ""
        DB.c.SL2020.msg.insert({"openid": openid ,
                                "sendTime": datetime.datetime.utcnow() ,
                                "avatarUrl": u.avatarUrl ,
                                "type": userType ,
                                "msg": msg
                                })
        return responseOK(None)


@app.route("/test")
def test():
    for i in range(100):
        DB.c.SL2020.msg.insert({"openid": str(i*100) ,
                                "sendTime": datetime.datetime.utcnow() ,
                                "avatarUrl": "22222222" ,
                                "type": "222222" ,
                                "msg": "3333333333333"
                                })
