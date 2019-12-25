from app.utils.DB import DB
import datetime
import uuid
import json
from setting import *
import requests


class Session():
    def __init__(self, token):
        s = DB.c.myNCUT.Session.find_one({"token": token})
        if s is not None:
            self.openid = s["openid"]
            self.token = token
            self.createTime = s.get("createTime")
            self.alive = True
        else:
            self.alive = False

    @staticmethod
    def create(code: str):
        '''
        创建一个Session
        MongoDB通过TTL索引控制会话的生命周期
        :param code: 微信临时登陆凭证
        :return: openid合法的情况下返回token 否则返回None
        '''
        grant_type = 'authorization_code'
        data = {}
        data['appid'] = wxAPPID
        data['secret'] = wxAPPSECRET
        data['grant_type'] = grant_type
        data['js_code'] = code
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=data)
        openid = json.loads(r.text).get("openid")
        if openid is None:
            return None
        if DB.c.myNCUT.User.find_one({"openid": openid}) is not None:
            # 如果会话已经存在直接返回那个token
            old = DB.c.myNCUT.Session.find_one({"openid": openid})
            if old is not None:
                return old["token"]
            token = uuid.uuid1().hex
            DB.c.myNCUT.Session.insert({
                "token": token,
                "openid": openid,
                "createTime": datetime.datetime.utcnow()
            })
            return token
        else:
            return None
