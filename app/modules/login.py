# -*- coding: utf-8 -*-
import requests
import json
from setting import *


def getWxAccess_token():
    url='https://api.weixin.qq.com/cgi-bin/token'
    data={
        'grant_type':'client_credential',
        'appid':wxAPPID,
        'secret':wxAPPSECRET
    }
    res=requests.get(url,params=data).text
    return json.loads(res)['access_token']


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



def getYxAccess_token():
    '''
    获取云校access_token
    :return:
    '''
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
    userInfo['sex'] = tempInfo['d']['sex']
    userInfo['userid'] = tempInfo['d']['userid']
    userInfo['name']=tempInfo['d']['name']
    return userInfo