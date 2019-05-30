# -*- coding: utf-8 -*-
import requests
import json
from setting import *


def getOpenid(code):
    '''
    传入小程序临时登陆凭证code.
    返回openid
    :param code:
    :return:
    '''
    grant_type='authorization_code'
    data={}
    data['appid']=wxAPPID
    data['secret']=wxAPPSECRET
    data['grant_type']=grant_type
    data['js_code']=code
    r=requests.get('https://api.weixin.qq.com/sns/jscode2session',params=data)
    return(json.loads(r.text)['openid'])



def getAccess_token():
    data={
        'appid':yxAPPID,
        'appsecret':yxAPPSECRET
    }
    res=requests.get('https://ucpay.ncut.edu.cn/open/api/access/token',params=data)
    return json.loads(res.text)['d']['access_token']

def getUserInfo(code,access_token):
    '''
    筛选从云校服务器上拿到的数据，返回筛选后的用户信息
    :param code:
    :param access_token:
    '''
    data={
        'code':code,
        'access_token':access_token
    }
    res=requests.get('https://ucpay.ncut.edu.cn/open/user/user/user-by-code',params=data)
    tempInfo=json.loads(res.text)
    userInfo = {}
    userInfo['uid']=tempInfo['d']['uid']
    userInfo['email'] = tempInfo['d']['email']
    userInfo['mobile'] = tempInfo['d']['mobile']
    userInfo['sex'] = tempInfo['d']['sex']
    userInfo['avatar'] = tempInfo['d']['avatar']
    userInfo['userid'] = tempInfo['d']['userid']
    userInfo['name']=tempInfo['d']['name']
    # userInfo['degree']= tempInfo['d']['department']['identity']
    try:
        for value in tempInfo['d']['department']['rolename'].values():
            userInfo['class']=value
    except:
        pass
    return userInfo