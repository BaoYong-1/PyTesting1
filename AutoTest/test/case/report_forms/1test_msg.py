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
from Data_Comp import *
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


class Test_MSG(unittest.TestCase):
    ''' 下发报文报表查询测试'''

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
            driver.find_element_by_xpath(
                "//*[@class='main_table']//tr//div/div[3]/table//tr//div//li[" + str(i + 3) + "]").click()
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
        excel = r"F:\PyTesting\AutoTest\log\excel\MSG.xls"
        # 查找页面数据，xpath为报表数据的路径
        table_rows = driver.find_element_by_xpath(
            "//table[starts-with(@id, 'EaserUI_EditorTable_Body_')]").find_elements_by_tag_name(
            'tr')
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
        del_row(excel, excel)

    def test_1login(cls):
        '''用户登录'''
        driver = cls.driver
        CodeText = get_code(driver)
        login(driver, 'baoyong123', 'asdf1234', CodeText)
        time.sleep(5)
        log.info("用户登录")

    # def test_2skip(cls):
    #     '''跳转到下发报文界面'''
    #     driver = cls.driver
    #     test = BaseAction(driver)
    #     #打开车辆监控我的车队
    #     test.Click("id","gps_toolbar_leftbutton_button_w")
    #     #输入框输入搜索车辆名称
    #     test.Input("id","gps_main_lefttree_searchtext_text","济宁00001")
    #     #点击搜索按钮
    #     test.Click("id", "gps_main_lefttree_searchtext_searchbutton_a")
    #     test.Wait(2)
    #     # 点击车辆进行定位
    #     test.Click("xpath", "//*[@id='gps_leftmenu_carlist_div_w']//a[2]")
    #     #点击车辆图标
    #     test.Click("xpath", "//*[@id='gps_carpoint_济宁00001_div']/div[2]")
    #     # 点击下发报文按钮
    #     test.Click("id", "gps_map_cardialog_sendmessage_div_w")
    #     report_name = test.Get_text("xpath", "//*[@id='ui-id-2']")
    #     try:
    #         cls.assertEqual(report_name,"济宁00001"+"  "+"下发报文设置")
    #         log.info("跳转到下发报文界面")
    #     except AssertionError as e:
    #         test.get_windows_img('下发报文界面')
    #         print("找不到报表标题：", report_name)
    #         raise

    # def test_3send_msg(cls):
    #     '''发送报文'''
    #     driver = cls.driver
    #     test = BaseAction(driver)
    #     #勾选led
    #     test.Wait(2)
    #     test.Click("xpath", "//*[@id='gps_map_sendmessage_dialog_w']/div[1]/span[1]/ul/li/span")
    #     test.Wait(2)
    #     #自定义报文
    #     test.Click("xpath", "// *[@id='gps_map_sendmessage_diymessage_radio_w-jquery-extend-ui-radio']/span[1]")
    #     test.Wait(2)
    #     #输入报文内容
    #     test.Input("id","gps_map_sendmessage_txtmessage_textarea_w","测试下发报文00001")
    #     test.Wait(2)
    #     #点击发送
    #     test.Click("id", "gps_map_sendmessage_dialog_send_button_w")
    #     test.Wait(2)
    #     log.info("发送LED类型报文")
    #
    #     # 下发TTS报文
    #     test.Click("xpath", "//*[@id='gps_carpoint_济宁00001_div']/div[2]")
    #     test.Click("id", "gps_map_cardialog_sendmessage_div_w")
    #     test.Wait(2)
    #     test.Click("xpath", "//*[@id='gps_map_sendmessage_dialog_w']/div[1]/span[2]/ul/li/span")
    #     test.Wait(2)
    #     test.Click("xpath", "// *[@id='gps_map_sendmessage_diymessage_radio_w-jquery-extend-ui-radio']/span[1]")
    #     test.Wait(2)
    #     test.Input("id","gps_map_sendmessage_txtmessage_textarea_w","测试下发报文00002")
    #     test.Wait(2)
    #     test.Click("id", "gps_map_sendmessage_dialog_send_button_w")
    #     test.Wait(2)
    #     log.info("发送TTS类型报文")
    #
    #     # 下发终端类型报文
    #     test.Click("xpath", "//*[@id='gps_carpoint_济宁00001_div']/div[2]")
    #     test.Click("id", "gps_map_cardialog_sendmessage_div_w")
    #     test.Wait(2)
    #     test.Click("xpath", "//*[@id='gps_map_sendmessage_dialog_w']/div[1]/span[3]/ul/li/span")
    #     test.Wait(2)
    #     test.Click("xpath", "// *[@id='gps_map_sendmessage_diymessage_radio_w-jquery-extend-ui-radio']/span[1]")
    #     test.Wait(2)
    #     test.Input("id","gps_map_sendmessage_txtmessage_textarea_w","测试下发报文00003")
    #     test.Wait(2)
    #     test.Click("id", "gps_map_sendmessage_dialog_send_button_w")
    #     test.Wait(2)
    #     log.info("发送终端显示类型报文")

    def test_4getdata(cls):
        '''跳转到报表查询界面,获取页面数据'''
        driver = cls.driver
        test = BaseAction(driver)
        test.Click("id", "gps_toolbar_leftbutton_div_w")
        test.Click("id", "gps_main_menu_report_s_p")
        test.wait(5)
        test.Click("id", "id202694")
        test.wait(5)
        cls.switch_page()

    def test_5get_dbdata(cls):
        '''获取数据库中数据'''
        sql1 = "select t.d_time as 群发录入时间,h.v_user_account as 群发录入工号,t.v_text_send as 群发内容 from OPERATING_COMMAND_MSG t,GPS_USER h where t.v_user_id=h.v_user_id and " \
               "t.d_time between to_date('" + t_date + " 00:00:00', 'yyyy-mm-dd hh24:mi:ss') and to_date('" + t_date + " 23:59:59', 'yyyy-mm-dd hh24:mi:ss')"
        scrpath = "F:\\PyTesting\\AutoTest\\log\\excel\\"  # 指定的保存目录
        export(sql1, scrpath + 'MSG_T_DB.xlsx')
        log.info("获取数据库今日下发报文信息")

    def test_6datacomp(cls):
        '''验证数据'''
        excel = "F:\\PyTesting\\AutoTest\\log\\excel\\MSG.xls"
        excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\MSG_T_DB.xlsx"
        try:
            cls.assertTrue(test_read_excel(2, excel, excel1, "MSG_Result.xlsx"))
            print("数据查询成功！")
        except AssertionError as e:
            log.info("数据查询失败,页面数据和系统数据不一致！")
            raise

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
