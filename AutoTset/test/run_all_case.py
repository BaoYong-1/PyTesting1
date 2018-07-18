# coding:utf-8
import unittest
import os
import BSTestRunner
import sys

sys.path.append('F:\\PyTesting\\AutoTset\\public')
from send_email import main2
import time


def createsuit():
    # 创建测试用例集
    testcase = unittest.TestSuite()
    # 判断是否为测试用例，自动加载测试用例到测试套件中
    # case_path = os.path.join(os.getcwd(),'case')
    case_dir = "F:\PyTesting\AutoTset\\test\case\\report_forms"
    # discover方法定义
    print(case_dir)
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test_*.py', top_level_dir=None)
    # discover方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            # 添加用例到testcase
            print(test_case)
            testcase.addTest(test_case)
    return testcase


if __name__ == "__main__":
    # now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # report_path = 'F:\\PyTesting\\AutoTset\\report\\'+now+'Test_result.html'
    report_path = 'F:\\PyTesting\\AutoTset\\report\\Test_result.html'
    fp = open(report_path, "wb")
    runner = BSTestRunner.BSTestRunner(stream=fp, title="自动化测试_测试框架报告", description="用例执行情况：")
    # runner.run(createsuit())
    print(createsuit())
    fp.close()
    # main2()  # from send_email import main2  发送邮件！
