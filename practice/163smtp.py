import smtplib
import string

HOST = 'smtp.163.com'
SUBJECT = 'Test email from Python'
FROM = "hawahe@163.com"
TO = 'zhaobohua@pwrd.com'
text = 'Python rules them all!'
BODY = string.join((
    "From: %s" %FROM,
    "To: %s" %TO,
    "Subject: %s" %SUBJECT,
    "",
    text
    ), "\r\n")
server = smtplib.SMTP()
server.connect(HOST,"25")
server.starttls()
server.login("xxx@163.com ","xxxxxx")
server.send(FROM,[TO],BODY)
server.quit