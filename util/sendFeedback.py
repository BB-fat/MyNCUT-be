import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from setting import *

from util.mongoClient import *

feedback=mongoClient().ckeckFeedback()

if feedback!=None:
    text = "Halo!there is a new feedback in DB.\nbug:%d\nupdate:%d\nother:%d"(feedback["bug"],feedback["update"],feedback["other"])

    text_plain = MIMEText(text,'plain', 'utf-8')

    msg=MIMEMultipart("mixed")
    msg.attach(text_plain)

    smtp = smtplib.SMTP()

    smtp.connect(FEEDBACK_EMAILHOST,FEEDBACK_EMAILPORT)

    smtp.login(FEEDBACK_EMAILUSER,FEEDBACK_EMAILPASSWORD)

    smtp.send_message(FEEDBACK_EMAIL_FROMADRESS,FEEDBACK_EMAIL_TOADRESS,msg.as_string())




