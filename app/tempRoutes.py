from app import app
from flask import render_template,send_file, request
from werkzeug.utils import secure_filename
from app.modules.login import *
from app.modules.SL_2019 import *

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
    data['msgs']=app.DB.SL_takeMsg(30)
    data['same_name_school'],data['same_name_college'],data['city']=app.DB.SL_same_city(userInfo['userid'])
    data['book']=library(userInfo['userid'])
    data['userid']=userInfo['userid']
    data['wenyi']=app.DB.SL_wenyi_url()
    return render_template("2019SchoolLife.html", data=data)
    # return render_template("test.html",data=json.dumps(data))

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
    userInfo = app.DB.getUserInfo(openid)
    data = SchoolLife(userInfo['userid']).getData()
    data['name'] = userInfo['userInfo']['name']
    data['count'] = app.DB.SL_countPlus(userInfo['userid'])
    data['sex'] = userInfo['userInfo']['sex']
    data['msgs'] = app.DB.SL_takeMsg(30)
    data['same_name_school'], data['same_name_college'], data['city'] = app.DB.SL_same_city(userInfo['userid'])
    data['book'] = library(userInfo['userid'])
    data['userid'] = userInfo['userid']
    data['wenyi']=app.DB.SL_wenyi_url()
    return render_template("2019SchoolLife.html", data=data)

@app.route("/schoollifemsg")
def schoolLifeMsg():
    msg=request.args.get("msg")
    userid=request.args.get("userid")
    userInfo=app.DB.getUserInfo(userid=userid)
    app.DB.SL_leaveMsg({
        "msg":msg,
        "userid":userid,
        "img":userInfo['userInfo']['avatar']
    })
    return "success"

@app.route("/wenyi")
def wenyi():
    app.DB.SL_count_wenyi()
    return 'success'


@app.route("/uploadpic",methods=['GET','POST'])
def upload():
    f=request.files['wenyipic']
    f.save('/home/myncut/wenyipic/'+secure_filename(f.filename))
    return 'success'

@app.route("/getfeedback")
def getFeedback():
    '''
    后台临时接口
    获取未回复的反馈列表
    :return:
    '''
    return json.dumps(app.DB.getFeedback())

@app.route("/answerfeedback",methods=['POST'])
def answerFeedback():
    '''
    后台临时接口
    回复反馈内容
    :return:
    '''
    data=request.form
    t='RJWstvx1LBRKumv-CgwK6Y9WGAoR-pOTjDB1BACRuCk'
    f= data['formId']
    o= data['openid']
    rd=data['reqData']
    res=answerFeedback(f, o, t, rd)
    app.DB.answerFeedback(data['formId'])
    if res:
        return "success"
    else:
        return "fail"