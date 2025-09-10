import base64
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

from Checker.lib.log_color import log
from Checker.lib.setting.config import config


def read_last_n_lines(filename, n=20):
    """读取文件的最新n条数据并返回一个数组"""
    if not os.path.exists(filename):
        return []  # 如果文件不存在, 返回空数组

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 读取所有行

    return [line.strip() for line in lines[-n:]]  # 返回最新n条, 去掉换行符


def send_email(subject, body, send_email, title="筛查到异常蓝图!!"):
    # 邮件内容
    # title="智能仪表终端"
    utf8_bytes = title.encode('utf-8')
    base64_encoded = base64.b64encode(utf8_bytes).decode('utf-8')
    final_nickname = f'=?utf-8?b?{base64_encoded}?='
    # 构建邮件
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = final_nickname + ' <1907284584@qq.com>'
    msg['To'] = send_email

    # 发送邮件
    smtp_server = config.smtp_server
    smtp_port = config.smtp_port
    sender_email = config.smtp_sender_email
    password = config.smtp_password  # 在QQ邮箱设置里拿到的码

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, [msg['To']], msg.as_string())
            log.info('邮件发送成功!')
            return True

    except smtplib.SMTPException:  # as smtp_error:
        return None
    except Exception as e:
        log.error(f"发生其他错误: {e}")
        return None


def send():
    if config.smtp_enable:
        log.info("执行发送")
        subject = '[来自CSC 机械动力自动检查]'
        body = '尊敬的腐竹您好, 来自CSC检查到了异常蓝图, 蓝图信息如下: \n'
        resource = read_last_n_lines(r"logs\check.log", n=20)
        for item in resource:
            body = f"{body}+{item}\n"
        body = body + '\n请注意: 这个功能与部分检查仍然处于测试阶段, 针对附魔标签仍会误报, 因此可能会将部分蓝图标记为异常!'
        send_email(subject, body, send_email=config.email_receive)


if __name__ == "__main__":
    send()
