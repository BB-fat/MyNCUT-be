import requests
import json
from setting import *

# at='71808fd2c8c8d88fa7910d6567fce87b'

def getAccess_token():
    data={
        'appid':APPID,
        'appsecret':APPSECRET
    }
    res=requests.get('https://ucpay.ncut.edu.cn/open/api/access/token',params=data)
    return json.loads(res.text)

def getUserInfo(code,access_token):
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

if __name__=="__main__":
    APPID='31b1e992583074382'
    APPSECRET='f5e030ee903dbc29c6e76375253d1ee6'
    print(getUserInfo('228399',at))
    # print(getAccess_token(APPID,APPSECRET))