import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from setting import *

def sendFeedback(feedback,userid):
    text = '''
    Subject:我的北方反馈
    
    学号：
    %s
    时间：
    %s
    反馈内容：
    %s
    '''%(userid,feedback['time'],feedback['text'])
    text_plain = MIMEText(text,'plain', 'utf-8')
    msg=MIMEMultipart("mixed")
    msg.attach(text_plain)
    smtp = smtplib.SMTP_SSL(EMAIL_SERVER,EMAIL_PORT)
    smtp.login(EMAIL_USERNAME,EMAIL_PASSWD)
    smtp.sendmail(EMAIL_USERNAME,[EMAIL_TO_ADDRESS],msg.as_string())
    smtp.quit()