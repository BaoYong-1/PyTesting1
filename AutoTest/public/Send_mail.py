#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr


def new_file(test_dir):
    # 列举test_dir目录下的所有文件，结果以列表形式返回。
    global lists
    lists = os.listdir(test_dir)
    # sort按key的关键字进行排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间
    # 最后对lists元素，按文件修改时间大小从小到大排序。
    lists.sort(key=lambda fn: os.path.getmtime(test_dir + '\\' + fn))
    # 获取最新文件的绝对路径
    file_path = os.path.join(test_dir, lists[-1])
    return file_path


# 格式化邮件地址
def formatAddr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendMail(body):
    smtp_server = 'smtp.163.com'
    from_mail = '13678678012@163.com'
    mail_pass = '13678678012by'
    to_mail = ['534138762@qq.com', 'baoyong@sdgakj.com']
    # 构造一个MIMEMultipart对象代表邮件本身
    msg = MIMEMultipart()
    # Header对中文进行转码
    msg['From'] = formatAddr('测试部 <%s>' % from_mail)
    msg['To'] = ','.join(to_mail)
    msg['Subject'] = Header('卫星定位平台BS自动化测试报告', 'utf-8')
    # plain代表纯文本;html代表网页
    msg.attach(MIMEText(body, _subtype='html', _charset='utf-8'))
    # 二进制方式模式文件
    report_path = 'F:\\PyTesting\\AutoTest\\report\\'
    attachment = new_file(report_path)
    attachment1 = os.path.basename(new_file(report_path))
    with open(attachment, 'rb') as f:
        # MIMEBase表示附件的对象
        mime = MIMEBase('text', 'txt', filename=attachment)
        # filename是显示附件名字
        mime.add_header('Content-Disposition', 'attachment', filename=attachment1)
        # 获取附件内容
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        # 作为附件添加到邮件
        msg.attach(mime)
    try:
        s = smtplib.SMTP()
        s.connect(smtp_server, "25")
        s.login(from_mail, mail_pass)
        s.sendmail(from_mail, to_mail, msg.as_string())  # as_string()把MIMEText对象变成str
        print('%s----发送邮件成功' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        s.quit()
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(err)


if __name__ == "__main__":
    report_path = 'F:\\PyTesting\\AutoTest\\report\\'
    attachment = new_file(report_path)
    f = open(attachment, 'rb')
    mail_body = f.read()
    f.close()
    sendMail(mail_body)
