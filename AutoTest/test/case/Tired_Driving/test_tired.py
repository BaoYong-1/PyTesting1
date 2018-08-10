# _*_ coding:utf-8 _*_
import unittest
from selenium import webdriver
import xlrd
import xlwt
import sys
import re

sys.path.append('F:\\PyTesting\\AutoTest\\public')
from Logger import Log
from GetVerifyCode import get_code
from ConfigParser import ReadConfigFile
import time
import cx_Oracle
from Get_DB_Data import export
from Excel import Excel

global scrpath, begin_time, end_time
scrpath = 'F:\\PyTesting\\AutoTest\\log\\excel\\'  # 指定的保存目录
read = ReadConfigFile("Tired_Test")
item_list = read.get_config_value()
begin_time = item_list[0][1]
end_time = item_list[1][1]
log_file = item_list[2][1]
log = Log()


class Test_tired(unittest.TestCase):
    ''' 疲劳驾驶报警测试'''

    @classmethod
    def setUpClass(cls):
        print("开始测试")

    @classmethod
    def tearDownClass(cls):
        print("结束测试")

    def setUp(self):

        print("开始单个测试用例")

    def tearDown(self):
        print("结束单个测试用例")

    def test_car_004(self):
        '''测B10004（只收到一条疲劳驾驶报警的概率比较大）'''
        sql004 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000004' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')"
        export(sql004, scrpath + '测B10004.xlsx')
        log.info("获取测B10004数据路中疲劳驾驶报警信息")
        excle = xlrd.open_workbook(scrpath + '测B10004.xlsx')
        sheet = excle.sheets()[0]  # 获取第0个表
        n4 = sheet.nrows
        log.info("测B10004数据库中疲劳驾驶报警条数为：" + str(n4 - 1))
        fopen = open(log_file, 'r', encoding='UTF-8')
        count = 0
        for lines in fopen.readlines():  # 按行读取text中的内容
            # lines = lines.replace("\n", "").split(",")
            # if 'aaa' in str(lines) and '2' not in str(lines):
            # 筛选出含有'aaa'并且不含数字2的每一行
            li = re.findall("测B10004 报警类型：2", lines)
            if len(li) > 0:
                count = count + len(li)
                print(lines)
                # print(count)
        fopen.close()
        log.info("测B10004上级平台日志中疲劳驾驶报警条数为：" + str(count))
        self.assertEqual(str(n4 - 1), str(count), "数据库报警信息和上级平台日志中报警信息不一致！")
        log.info("数据库报警信息和上级平台日志中报警信息一致！")

    def test_car_005(self):
        '''测B10005（接收多条疲劳报警的概率比较大）'''
        sql005 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000005' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')"
        export(sql005, scrpath + '测B10005.xlsx')
        log.info("获取测B10005数据路中疲劳驾驶报警信息")
        excle = xlrd.open_workbook(scrpath + '测B10005.xlsx')
        sheet = excle.sheets()[0]  # 获取第0个表
        n5 = sheet.nrows
        log.info("测B10005数据库中疲劳驾驶报警条数为：" + str(n5 - 1))

        fopen = open(log_file, 'r', encoding='UTF-8')
        count = 0
        for lines in fopen.readlines():  # 按行读取text中的内容
            # lines = lines.replace("\n", "").split(",")
            # if 'aaa' in str(lines) and '2' not in str(lines):
            # 筛选出含有'aaa'并且不含数字2的每一行
            li = re.findall("测B10005 报警类型：2", lines)
            if len(li) > 0:
                count = count + len(li)
                print(lines)
                # print(count)
        fopen.close()
        log.info("测B10005上级平台日志中疲劳驾驶报警条数为：" + str(count))
        self.assertEqual(str(n5 - 1), str(count), "数据库报警信息和上级平台日志中报警信息不一致！")
        log.info("数据库报警信息和上级平台日志中报警信息一致！")

    def test_car_006(self):
        '''测B10006（每隔阈值范围接收一条，能收到多条疲劳驾驶报警）'''
        sql006 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000006' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')"
        export(sql006, scrpath + '测B10006.xlsx')
        log.info("获取测B10006数据路中疲劳驾驶报警信息")
        excle = xlrd.open_workbook(scrpath + '测B10006.xlsx')
        sheet = excle.sheets()[0]  # 获取第0个表
        n6 = sheet.nrows
        log.info("测B10006数据库中疲劳驾驶报警条数为：" + str(n6 - 1))

        fopen = open(log_file, 'r', encoding='UTF-8')
        count = 0
        for lines in fopen.readlines():  # 按行读取text中的内容
            # lines = lines.replace("\n", "").split(",")
            # if 'aaa' in str(lines) and '2' not in str(lines):
            # 筛选出含有'aaa'并且不含数字2的每一行
            li = re.findall("测B10006 报警类型：2", lines)
            if len(li) > 0:
                count = count + len(li)
                print(lines)
                # print(count)
        fopen.close()
        log.info("测B10006上级平台日志中疲劳驾驶报警条数为：" + str(count))
        self.assertEqual(str(n6 - 1), str(count), "数据库报警信息和上级平台日志中报警信息不一致！")
        log.info("数据库报警信息和上级平台日志中报警信息一致！")

    def test_car_007(self):
        '''测B10007（只能收到一条疲劳驾驶报警）'''
        sql007 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000007' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')"
        export(sql007, scrpath + '测B10007.xlsx')
        log.info("获取测B10007数据路中疲劳驾驶报警信息")
        excle = xlrd.open_workbook(scrpath + '测B10007.xlsx')
        sheet = excle.sheets()[0]  # 获取第0个表
        n7 = sheet.nrows
        log.info("测B10007数据库中疲劳驾驶报警条数为：" + str(n7 - 1))

        fopen = open(log_file, 'r', encoding='UTF-8')
        count = 0
        for lines in fopen.readlines():  # 按行读取text中的内容
            # lines = lines.replace("\n", "").split(",")
            # if 'aaa' in str(lines) and '2' not in str(lines):
            # 筛选出含有'aaa'并且不含数字2的每一行
            li = re.findall("测B10007 报警类型：2", lines)
            if len(li) > 0:
                count = count + len(li)
                print(lines)
                # print(count)
        fopen.close()
        log.info("测B10007上级平台日志中疲劳驾驶报警条数为：" + str(count))
        self.assertEqual(str(n7 - 1), str(count), "数据库报警信息和上级平台日志中报警信息不一致！")
        log.info("数据库报警信息和上级平台日志中报警信息一致！")

    def test_car_008(self):
        '''测B10008（每隔阈值范围接收一条，能收到多条疲劳驾驶报警）'''
        sql008 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000008' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')"
        export(sql008, scrpath + '测B10008.xlsx')
        log.info("获取测B10008数据路中疲劳驾驶报警信息")
        excle = xlrd.open_workbook(scrpath + '测B10008.xlsx')
        sheet = excle.sheets()[0]  # 获取第0个表
        n8 = sheet.nrows
        log.info("测B10008数据库中疲劳驾驶报警条数为：" + str(n8 - 1))

        fopen = open(log_file, 'r', encoding='UTF-8')
        count = 0
        for lines in fopen.readlines():  # 按行读取text中的内容
            # lines = lines.replace("\n", "").split(",")
            # if 'aaa' in str(lines) and '2' not in str(lines):
            # 筛选出含有'aaa'并且不含数字2的每一行
            li = re.findall("测B10008 报警类型：2", lines)
            if len(li) > 0:
                count = count + len(li)
                print(lines)
                # print(count)
        fopen.close()
        log.info("测B10008上级平台日志中疲劳驾驶报警条数为：" + str(count))
        self.assertEqual(str(n8 - 1), str(count), "数据库报警信息和上级平台日志中报警信息不一致！")
        log.info("数据库报警信息和上级平台日志中报警信息一致！")

    def test_car_009(self):
        '''测B10009（只能收到一条疲劳驾驶报警）'''
        sql009 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000009' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('" + end_time + "','yyyy-mm-dd hh24:mi:ss')"
        export(sql009, scrpath + '测B10009.xlsx')
        log.info("获取测B10009数据路中疲劳驾驶报警信息")
        excle = xlrd.open_workbook(scrpath + '测B10009.xlsx')
        sheet = excle.sheets()[0]  # 获取第0个表
        n9 = sheet.nrows
        log.info("测B10009数据库中疲劳驾驶报警条数为：" + str(n9 - 1))

        fopen = open(log_file, 'r', encoding='UTF-8')
        count = 0
        for lines in fopen.readlines():  # 按行读取text中的内容
            # lines = lines.replace("\n", "").split(",")
            # if 'aaa' in str(lines) and '2' not in str(lines):
            # 筛选出含有'aaa'并且不含数字2的每一行
            li = re.findall("测B10009 报警类型：2", lines)
            if len(li) > 0:
                count = count + len(li)
                print(lines)
                # print(count)
        fopen.close()
        log.info("测B10009上级平台日志中疲劳驾驶报警条数为：" + str(count))
        self.assertEqual(str(n9 - 1), str(count), "数据库报警信息和上级平台日志中报警信息不一致！")
        log.info("数据库报警信息和上级平台日志中报警信息一致！")


if __name__ == "__main__":
    unittest.main()
