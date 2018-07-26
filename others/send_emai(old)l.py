import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase


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


def sendEmail(content, title, from_name, from_address, to_address, serverport, serverip, username, password):
    msg = MIMEMultipart()
    report_path = 'F:\\PyTesting\\AutoTset\\report\\'
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
    # 这里的to_address只用于显示，必须是一个string
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = Header(title, 'utf-8')
    msg['To'] = ','.join(to_address)
    msg['From'] = from_name
    try:
        s = smtplib.SMTP_SSL(serverip, serverport)
        s.login(username, password)
        # 这里的to_address是真正需要发送的到的mail邮箱地址需要的是一个list
        s.sendmail(from_address, to_address, msg.as_string())
        print('%s----发送邮件成功' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(err)


# HEFEN_D = pth.abspath(pth.dirname(__file__))

def main2(newreport):
    TO = ['baoyong@sdgakj.com']  # 可以添加多人的邮件地址
    config = {
        "from": "13678678012@163.com",
        "from_name": '测试部:',
        "to": TO,
        "serverip": "smtp.163.com",
        "serverport": "465",
        "username": "13678678012@163.com",
        "password": "13678678012by"  # 网易邮箱的SMTP授权码
    }
    f = open(newreport, 'rb')
    title = "自动化测试_测试框架报告"
    mail_body = f.read()
    f.close()
    sendEmail(mail_body, title, config['from_name'], config['from'], config['to'], config['serverport'],
              config['serverip'], config['username'], config['password'])
