from app import app
from flask import render_template,send_file, request
from app.modules.login import *
import app.modules.feedback as fb

@app.route('/kSyoZqkJwk.txt')
def wxAuth():
    '''
    微信业务域名认证文件
    :return:
    '''
    return send_file('kSyoZqkJwk.txt')

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

@app.route("/wenyi")
def wenyi():
    app.DB.SL_count_wenyi()
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
    rd=json.loads(data['reqData'])
    res=fb.answerFeedback(f, o, t, rd)
    app.DB.answerFeedback(data['formId'])
    if res:
        return "success"
    else:
        return "fail"