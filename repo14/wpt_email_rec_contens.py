#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path as path
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.MIMEMultipart import MIMEMultipart
import ConfigParser

#日期获取
today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)
#发送文件获取
hh_file = path.join("/home/ubuntu/bingo/rec_file")
file_name = "rec_courses_" + str(yesterday) + ".xls"
file_path = path.join(hh_file,file_name)

#邮件框架对象msg
msg = MIMEMultipart()
mail_attachments = MIMEText(open(file_path,'rb').read(),'utf-8','utf-8') #邮件附件内容
mail_attachments["Content-type"] = 'application/octet-stream'
mail_attachments["Content-Disposition"] = 'attachment;filename="%s"'%file_name
msg.attach(mail_attachments) #邮件附件

#邮箱数据库连接
cf = ConfigParser.ConfigParser()
cf.read('/data/db.ini')
smtpserver = 'smtp.exmail.qq.com'
username = cf.get('mail','user')
password = cf.get('mail','password')
sender = cf.get('mail','sender')
receiver = ['bwwu@kaikeba.com','binweiwu12@gmail.com']

##邮件主体
subject = u'data_kkb课程推荐0.1'#邮件主题
mail_content = "具体见附件！！"#邮件主体内容
body = MIMEText(mail_content,'html','utf-8')
msg.attach(body) #邮件主体

#邮件发送整理
msg['Subject'] = subject
msg['From'] = sender
smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.set_debuglevel(1)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

