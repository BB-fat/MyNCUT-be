from app import app
from flask import render_template,send_file,make_response,request
from util.login import *
from util.SL_2019 import *

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
    data=SchoolLife(userInfo['userid']).getData()
    data['name']=userInfo['userInfo']['name']
    data['count']=app.DB.SL_countPlus(userInfo['userid'])
    data['sex']=userInfo['userInfo']['sex']
    data['msgs']=app.DB.SL_takeMsg(2)
    data['same_name_school'],data['same_name_college']=app.DB.SL_same_city(userInfo['userid'])
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
    msgs=app.DB.SL_takeMsg(2)
    data={
        'userid':userInfo['userid']
    }
    return render_template("2019SchoolLife.html", data=data)

@app.route("/schoollifemsg")
def schoolLifeMsg():
    msg=request.args.get("msg")
    app.DB.SL_leaveMsg(msg)
    return "success"