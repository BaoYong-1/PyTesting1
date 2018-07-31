# def calc(*numbers):
#     m = len(numbers)
#     if len(numbers) == 0:
#         raise TypeError
#     m = 1
#     for n in numbers:
#         m = m * n
#     return m
#
#
# print(calc(1, 2, 3,4))
import unittest
import os


def createsuit():
    # 创建测试用例集
    testcase = unittest.TestSuite()
    # discover方法定义
    # discover方法筛选出来的用例，循环添加到测试套件中
    case_path1 = os.path.dirname(__file__)
    print(case_path1)
    case_path = os.path.join(os.getcwd(), "test")
    print(case_path)
    top_dir = "F:\\PyTesting\\"
    case_dir = 'others'
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test_*.py', top_level_dir=None)
    # 判断是否为测试用例，自动加载测试用例到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            # 添加用例到testcase
            print(test_case)
            testcase.addTest(test_case)
    return testcase


if __name__ == "__main__":
    createsuit()
