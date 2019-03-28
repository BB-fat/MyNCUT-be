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
    # data['appid']=wxAPPID
    # data['secret']=wxAPPSECRET
    data['grant_type']=grant_type
    data['js_code']=code
    r=requests.get('https://api.weixin.qq.com/sns/jscode2session?appid='+appid+'&secret='+secret+'&grant_type='+grant_type+'&js_code='+code)
    return(json.loads(r.text)['openid'])



def getAccess_token():
    '''
    获取授权码
    :return:
    '''
    data={
        'appid':yxAPPID,
        'appsecret':yxAPPSECRET
    }
    res=requests.get('https://ucpay.ncut.edu.cn/open/api/access/token',params=data)
    return json.loads(res.text)['b']['access_token']

def getUserInfo(code,access_token):
    '''
    获取用户数据
    :param code:
    :param access_token:
    :return:
    '''
    data={
        'code':code,
        'access_token':access_token
    }
    res=requests.get('https://ucpay.ncut.edu.cn/open/user/user/user-by-code',params=data)
    tempInfo=json.loads(res.text)
    userInfo = {}
    userInfo['name'] = tempInfo["d"]["realname"]
    userInfo['email'] = tempInfo["d"]["email"]
    userInfo['mobile'] = tempInfo["d"]["mobile"]
    userInfo['sex'] = tempInfo["d"]["sex"]
    return userInfo