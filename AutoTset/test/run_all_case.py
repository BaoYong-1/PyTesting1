# coding:utf-8
import unittest
import os
import HTMLTestRunnerCN
import time
import sys
sys.path.append('F:\\PyTesting\\AutoTset\\public')
from Send_mail import sendMail
from Send_mail import new_file


def createsuit():
    # 创建测试用例集
    testcase = unittest.TestSuite()
    # discover方法定义
    # discover方法筛选出来的用例，循环添加到测试套件中
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test_*.py', top_level_dir=None)
    # 判断是否为测试用例，自动加载测试用例到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            # 添加用例到testcase
            print(test_case)
            testcase.addTest(test_case)
    return testcase

if __name__ == "__main__":
    global case_dir
    case_dir = "F:\\PyTesting\\AutoTset\\test\\case\\report_forms\\"
    now = time.strftime('%Y-%m-%d_%H_%M_%S_')
    report_path = 'F:\\PyTesting\\AutoTset\\report\\'
    filename = report_path + '\\' + now + 'result.html'
    fp = open(filename, "wb")  # 创测试报告的html文件，此时还是个空文件
    # 定义HTMLTestRunner测试报告，stream定义报告所写入的文件；title为报告的标题；description为报告的说明与描述
    runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title="卫星定位平台BS自动化测试报告", description="用例执行情况(详情见附件)：",
                                               tester=u"测试部")
    runner.run(createsuit())  # 运行测试容器中的用例，并将结果写入的报告中
    fp.close()  # 关闭文件流，不关的话生成的报告是空的
    attachment = new_file(report_path)
    f = open(attachment, 'rb')
    mail_body = f.read()
    f.close()
    sendMail(mail_body)
