import yagmail
from config.server_config import *

yag_server = None


def init_email_server():
    # 连接服务器
    # 用户名、授权码、服务器地址
    yag_server = yagmail.SMTP(user=EMAIL_ARGS["username"], password=EMAIL_ARGS["authorization_code"],
                              host=EMAIL_ARGS["host"])


def send_email(to, subject, content, attachment=None):
    # 发送对象列表
    email_to = [to, ]
    email_title = subject
    email_content = content
    # 附件列表
    email_attachments = [attachment]

    # 发送邮件
    yag_server.send(email_to, email_title, email_content, email_attachments)
