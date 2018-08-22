# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from xlutils3.copy import copy  # 将xlrd.Book转为xlwt.workbook，在原有的excel基础上进行修改，添加等。
import xlwt  # 写入excel（新建）
import xlrd  # 读取excel
import os
import time
import cx_Oracle
import unittest
from openpyxl import Workbook
import sys

sys.path.append('F:\\PyTesting\\AutoTest\\public')
from Logger import Log
from Time import Time
from Login_c import login
from GetVerifyCode import get_code
from Data_Comp import test_read_excel
from Get_DB_Data import export, execute
from ConfigParser import ReadConfigFile
from Excel import Excel

sys.path.append('F:\\PyTesting\\AutoTest\\test\\action')
from base_action import BaseAction

log = Log()
get_time = Time()
today = get_time.today
t_date = get_time.t_date
Yestoday = get_time.yestoday
last_month1 = get_time.last_month_start
last_month2 = get_time.last_month_end


class Test_Mile(unittest.TestCase):
    ''' 车辆行驶里程及油耗报表查询测试'''

    @classmethod
    def setUpClass(cls):
        log.info("开始测试")
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        read = ReadConfigFile("TestUrl")
        item_list = read.get_config_value()
        url = item_list[0][1]
        cls.driver.get(url)
        log.info("打开浏览器")
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        log.info("结束测试")
        cls.driver.quit()

    def setUp(self):
        print("开始单个测试用例")

    def tearDown(self):
        print("结束单个测试用例")

    def switch_page(cls):
        '''分页跳转,获取前端页面数据'''
        driver = cls.driver
        # 分页
        pages = driver.find_element_by_xpath("//*[@class='easierui_gps_bottom_fillet']/ul").find_elements_by_tag_name(
            "li")
        t = len(pages)
        # print(t)
        # if t - 6 <= 7:
        for i in range(t - 6):
            # 循环点击页码
            driver.find_element_by_xpath("//*[@class='easierui_gps_bottom_fillet']/ul/li[" + str(i + 3) + "]").click()
            time.sleep(3)
            # 保存每页的数据
            cls.load_Table(i)
            print("获取报表第" + str(i + 1) + "页数据成功！")

    def load_Table(cls, page):
        '''获取报表页面数据'''
        # 创建工作簿
        driver = cls.driver
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建工作表
        sheet = wbk.add_sheet('Web_data', cell_overwrite_ok=True)
        excel = r"F:\PyTesting\AutoTest\log\excel\Mile_single.xls"
        # 查找页面数据，xpath为报表数据的路径
        table_rows = driver.find_element_by_xpath(
            "//table[starts-with(@id, 'EaserUI_EditorTable_Body_')]").find_elements_by_tag_name('tr')
        # print(table_rows)
        row = 21
        for i, tr in enumerate(table_rows):  # enumerate()是python的内置函数.enumerate多用于在for循环中得到计数
            # 获取页面table中的标题
            if i == 0 and page == 0:
                table_cols1 = tr.find_elements_by_tag_name('td')
                for j, tc in enumerate(table_cols1):
                    sheet.write(i, j, tc.text)
                    wbk.save(excel)
            # 获取页面table中的数据，进行拼接
            else:
                table_cols2 = tr.find_elements_by_tag_name('td')
                for j, tc in enumerate(table_cols2):
                    # 老的工作簿，打开excel
                    oldWb = xlrd.open_workbook(excel, formatting_info=True)
                    # 新的工作簿,复制老的工作簿
                    newWb = copy(oldWb)
                    # 新的工作表
                    newWs = newWb.get_sheet(0)
                    newWs.write(i + page * row, j, tc.text)
                    os.remove(excel)
                    newWb.save(excel)

    def test_1login(cls):
        '''用户登录'''
        driver = cls.driver
        CodeText = get_code(driver)
        login(driver, 'baoyong123', 'asdf1234', CodeText)
        time.sleep(5)
        log.info("用户登录")

    def test_2skip(cls):
        '''跳转到报表查询界面'''
        driver = cls.driver
        test = BaseAction(driver)
        test.Click("id", "gps_toolbar_leftbutton_div_w")
        # 点击报表查询按钮
        test.Click("id", "gps_main_menu_report_s_p")
        test.wait(5)
        # 点击单车里程油耗报表按钮
        test.Click("id", "id401010")
        test.wait(5)

    def test_3select(cls):
        '''选择查询车辆和时间'''
        driver = cls.driver
        test = BaseAction(driver)
        # 点击搜索框
        test.Click("xpath", "//*[@id='oil_radio_tree_content']/div[1]/input")
        # 输入要查询的车辆车牌号信息
        test.Input("xpath", "//*[@id='oil_radio_tree_content']/div[1]/input", "济宁00001")
        # 点击查询按钮
        test.Click("xpath", "//*[@id='oil_radio_tree_content']/div[1]/a")
        test.Wait(3)
        # 选中要查询的车辆
        test.Click("xpath",
                   "//*[@class='checkboxcontent']/span[@id='20180131171228000000000000008188-jquery-extend-ui-radio']/span[2]")
        # 点击返回框
        test.wait(3)
        test.Click("xpath", "//*[@id='oil_radio_tree_content']/div[4]")
        # 点击下一步
        test.wait(2)
        test.Click("xpath", "//*[@id='tyre_next_setting']")
        report_name = test.Get_text("xpath", "//*[@id='rnavigation']/li[2]/span[2]")
        try:
            cls.assertEqual(report_name, '单车行驶里程及油耗报表')
            log.info("跳转到单车行驶里程及油耗报表查询界面")
        except AssertionError as e:
            test.get_windows_img('单车行驶里程及油耗报表')
            print("找不到报表标题：", report_name)
            raise
        test.scrollLow("id", "turnPageButton")  # 滑动到页面底部
        test.Wait(2)
        cls.switch_page()

    def test_7login_out(cls):
        '''退出登录'''
        driver = cls.driver
        driver.find_element_by_id("gps_main_quit_span_w").click()
        time.sleep(2)
        driver.find_element_by_xpath("//body//div//div//div//button/span[./text()='确定']").click()
        log.info("退出登录！")


if __name__ == '__main__':
    unittest.main()
    # t=Test_history()
    # t.insert_db()
    # suite = unittest.TestSuite()
    # suite.addTest(Test_history("test_1login"))
    #
    # suite.addTest(Test_history("test_2skip"))
    #
    # suite.addTest(Test_history("test_3switch_page"))
    #
    # suite.addTest(Test_history("test_6login_out"))
    # unittest.TextTestRunner().run(suite)
