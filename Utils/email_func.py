import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "austin.yun365@gmail.com"  # Enter your address

receiver_email_1 = "austinyxh@hotmail.com"
receiver_email_2 = "ee07b238@gmail.com"

password = "19880729Yxh!" #("Type your password and press enter: ")

message = """\
Subject: Hi Yuan, 

Note the email password is currently exposed. Help to hide it when you get a chance. 

Thanks

Crius autotrade terminal

"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email_1, message)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email_2, message)