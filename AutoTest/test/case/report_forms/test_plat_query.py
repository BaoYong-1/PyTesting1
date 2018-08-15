# coding:utf-8
from selenium import webdriver
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

sys.path.append('F:\\PyTesting\\AutoTest\\test\\action')
from base_action import BaseAction

log = Log()
get_time = Time()
today = get_time.today
t_date = get_time.t_date
Yestoday = get_time.yestoday
last_month1 = get_time.last_month_start
last_month2 = get_time.last_month_end


class Test_Plat(unittest.TestCase):
    ''' 平台查岗报表查询测试'''

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
        pages = driver.find_element_by_xpath("//*[@class='easierui_gps_bottom_fillet']/ul").find_elements_by_tag_name(
            "li")
        t = len(pages)
        # print(t)
        # if t - 6 <= 7:
        for i in range(t - 6):
            driver.find_element_by_xpath(
                "//*[@class='main_table']//tr//div/div[3]/table//tr//div//li[" + str(i + 3) + "]").click()
            time.sleep(3)
            cls.load_Table(i)
            print("获取报表第" + str(i + 1) + "页数据成功！")

    def load_Table(cls, page):
        '''获取报表页面数据'''
        # 创建工作簿
        driver = cls.driver
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建工作表
        sheet = wbk.add_sheet('Web_data', cell_overwrite_ok=True)
        excel = r"F:\PyTesting\AutoTest\log\excel\Plat_Query.xls"
        # 查找页面数据，xpath为报表数据的路径
        table_rows = driver.find_element_by_xpath(
            "//table[starts-with(@id, 'EaserUI_EditorTable_Body_')]").find_elements_by_tag_name('tr')
        # print(table_rows)
        row = 11
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
        test.Click("id", "gps_main_menu_report_s_p")
        test.wait(5)
        test.Click("id", "id401013")
        test.wait(5)
        test.get_windows_img('查岗报表跳转成功')
        report_name = test.Get_text("xpath", "//*[@class='main_table']//li[2]/span[2]")
        try:
            cls.assertEqual(report_name, '平台查岗报表1')
        except Exception:
            print("找不到报表标题：", report_name)
        log.info("跳转到平台查岗报表查询界面")

    def test_3get_dbdata(cls):
        '''获取数据库中上月数据'''
        sql1 = "select z.v_plat_id,u.v_plat_name,z.d_time,z.v_info_content,z.v_ans_content,z.d_ans_time,h.v_user_name from PLAT_POST_QUERY z,GPS_PLAT u,GPS_USER h " \
               "where h.v_user_id=z.v_user_id and z.v_plat_id=u.v_plat_id and z.d_time between " \
               "to_date('" + last_month1 + " 00:00:01', 'yyyy-mm-dd hh24:mi:ss') and to_date('" + last_month2 + " 23:59:59', 'yyyy-mm-dd hh24:mi:ss')"

        scrpath = "F:\\PyTesting\\AutoTest\\log\\excel\\"  # 指定的保存目录
        export(sql1, scrpath + 'Plat_L_DB.xlsx')
        log.info("获取数据库上月数据")

    def test_4last_month(cls):
        '''查询系统上月数据'''
        driver = cls.driver
        test = BaseAction(driver)
        test.Click("xpath", "//*[@id='platCheck_searchHeader']//td[1]/span[2]/span")
        test.Click("id", "EasierUI_SELECT_platCheck_container1")
        test.Click("xpath", "//*[@id='EasierUI_SELECT_platCheck_container1']//li[5]")
        test.Click("id", "platCheck_submit")
        log.info("查询上月数据")
        test.wait(5)
        cls.switch_page()
        log.info("验证数据")
        excel = "F:\\PyTesting\\AutoTest\\log\\excel\\Plat_Query.xls"
        excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\Plat_L_DB.xlsx"
        try:
            cls.assertTrue(test_read_excel(3, excel, excel1, "Plat_L_Result.xlsx"))
            log.info("数据查询成功！")
        except AssertionError as e:
            log.info("数据查询失败,页面数据和系统数据不一致！")
            raise

    # def test_5Yestoday(cls):   #     '''查询昨日数据'''
    #     driver = cls.driver
    #     test = BaseAction(driver)
    #     #test.Click("xpath","//*[@id='warnData_searchHeader']/table/tbody/tr/td[1]")
    #     test.Click("id","EasierUI_SELECT_warnData_container2")
    #     test.Click("xpath","//*[@title='昨天']")
    #     test.Click("id","staticData_submit")
    #     test.wait(5)
    #     log.info("查询昨天数据")
    #     cls.switch_page()
    #     log.info("验证数据")
    #     excel = "F:\\PyTesting\\AutoTest\\log\\excel\\History_TARG.xls"
    #     excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\History_Yes_DB.xlsx"
    #     try:
    #         cls.assertTrue(test_read_excel(0,excel, excel1, "Yes_Result.xlsx"))
    #         print("数据查询成功！")
    #     except AssertionError as e:
    #         print("数据查询失败！")

    def test_6login_out(cls):
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
