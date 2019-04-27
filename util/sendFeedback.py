import smtplib
from pymongo import MongoClient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def ckeckFeedback(client):
    feedback = {"bug": 0, "update": 0, "other": 0}
    panduan = False
    newbugFeedback = client.feedback["bug"].find({"read": False})
    for bug in newbugFeedback:
        feedback["bug"] += 1
        panduan = True
    newupdateFeedback = client.feedback["update"].find({"read": False})
    for upate in newupdateFeedback:
        feedback["update"] += 1
        panduan = True
    newotherFeedback = client.feedback["other"].find({"read": False})
    for other in newotherFeedback:
        feedback["other"] += 1
        panduan = True
    if panduan == True:
        return feedback
    else:
        return None

if "__name__"=="__main__":
    client = MongoClient()
    feedback = ckeckFeedback(client)
    if feedback!=None:
        text = "Halo!there is a new feedback in DB.\nbug:%d\nupdate:%d\nother:%d"(feedback["bug"],feedback["update"],feedback["other"])

        text_plain = MIMEText(text,'plain', 'utf-8')

        msg=MIMEMultipart("mixed")
        msg.attach(text_plain)

        smtp = smtplib.SMTP()

        smtp.connect("smtp.qq.com",587)

        smtp.login('1056871944@qq.com','snjpnnztwsnxbbbf')

        smtp.send_message('1056871944@qq.com','1056871944@qq.com',msg.as_string())




