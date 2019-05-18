from app import app
from flask import render_template,send_file,make_response,request
from util.login import *


@app.route('/kSyoZqkJwk.txt')
def wxAuth():
    '''
    微信业务域名认证文件
    :return:
    '''
    return send_file('kSyoZqkJwk.txt')

@app.route("/test")
def test():
    return render_template("2019SchoolLife.html")

@app.route("/getauth")
def getAuth():
    '''
    用于给临时后台提供登陆凭证
    :return:
    '''
    return app.DB.getPasswd()

@app.route("/storedata",methods=['POST'])
def storeData():
    tempInfo =request.form
    if tempInfo['type']== 'banner':
        app.DB.setIndexBanner(tempInfo)
    else:
        app.DB.setIndexNotice(tempInfo)
    return "success"

@app.route("/schoollife")
def schoolLife():
    openid = request.args.get('openid')
    userInfo = app.DB.getUserInfo(openid)
    #
    # 请求数据并整理
    #
    data={
        'userid':userInfo['userid']
    }
    return render_template("2019SchoolLife.html", data=data)

@app.route("/schoollifeauth")
def schoolLifeAuth():
    '''
    通过点滴校园认证
    :return:
    '''
    access_token = getAccess_token()
    openid = request.args.get('state')
    code = request.args.get('code')
    userInfo = getUserInfo(code, access_token)
    app.DB.newUser(openid)
    app.DB.setUserInfo(openid, userInfo)
    data={
        'userid':userInfo['userid']
    }
    return render_template("2019SchoolLife.html", data=data)