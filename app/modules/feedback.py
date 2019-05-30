import smtplib
from email.mime.text import MIMEText
from setting import *
from app.modules.login import getWxAccess_token
import requests
import json

def sendFeedback(feedback,userid):
    text = '''
    学号：
    %s
    时间：
    %s
    反馈内容：
    %s
    '''%(userid,feedback['time'],feedback['text'])
    msg=MIMEText(text,'plain','utf-8')
    msg['Subject']="我的北方反馈"
    smtp = smtplib.SMTP_SSL(EMAIL_SERVER,EMAIL_PORT)
    smtp.login(EMAIL_USERNAME,EMAIL_PASSWD)
    smtp.sendmail(EMAIL_USERNAME,EMAIL_TO_ADDRESS,msg.as_string())
    smtp.quit()

def answerFeedback(formId,openid,templateId,resData,page="index"):
    '''
    给用户发送反馈信息
    '''
    url='https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token='
    data={
        'touser':openid,
        'template_id':templateId,
        'form_id':formId,
        'data':resData,
        'page':page
    }
    res=requests.post(url+getWxAccess_token(),data=json.dumps(data)).text
    if json.loads(res)['errcode']==0:
        return True
    else:
        return False


if __name__=="__main__":
    t='RJWstvx1LBRKumv-CgwK6Y9WGAoR-pOTjDB1BACRuCk'
    f='85c5dffe8d7b4222bdd8bb8b99ce217d'
    o='o1Glo5BZgdDoVqkuXgKzSw_r4T_M'
    rd={
        'keyword1':{
            'value':"测试"
        },
        'keyword2':{
            'value':'测试'
        }
    }
    answerFeedback(f,o,t,rd)