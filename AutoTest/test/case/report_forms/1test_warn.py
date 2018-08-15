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
from Login_c import login
from GetVerifyCode import get_code
from Data_Comp import test_read_excel
from Get_DB_Data import export
from ConfigParser import ReadConfigFile

sys.path.append('F:\\PyTesting\\AutoTest\\test\\action')
from base_action import BaseAction


class Test_warn(unittest.TestCase):
    ''' 报警警告报表查询测试'''

    @classmethod
    def setUpClass(cls):
        print("开始测试")
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        read = ReadConfigFile("TestUrl")
        item_list = read.get_config_value()
        url = item_list[0][1]
        cls.driver.get(url)
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        print("结束测试")
        cls.driver.quit()

    # def setUp(self):
    #     # print("开始单个测试用例")
    #     # self.dr = webdriver.Chrome()
    #     # self.dr.maximize_window()
    #     # self.dr.get('http://192.168.10.110:8080/WebGis/login')
    #     # time.sleep(5)
    #
    # def tearDown(self):
    #     print("结束单个测试用例")

    def test_1login(cls):
        '''用户登录'''
        driver = cls.driver
        CodeText = get_code(driver)
        # login(driver, 'baoyong123', 'asdf1234', CodeText)  # 正确用户名和密码
        time.sleep(5)
        test = BaseAction(driver)
        read = ReadConfigFile("Login")
        test.Input("id", "txt_username", "baoyong123")
        test.Input("id", "txt_password", "asdf1234")
        test.Input("id", "verifycode", CodeText)
        test.Click("class_name", "button")
        time.sleep(5)

    def test_2skip(cls):
        '''跳转到报表查询界面'''
        driver = cls.driver
        driver.find_element_by_id("gps_toolbar_leftbutton_div_w").click()
        driver.find_element_by_id("gps_main_menu_report_s_p").click()
        time.sleep(2)  # 等待元素加载
        driver.find_element_by_id("id201286").click()
        time.sleep(2)
        print("页面跳转成功！")

    def test_3switch_page(cls):
        '''分页跳转,获取分页中的所有数据'''
        driver = cls.driver
        pages = driver.find_element_by_xpath(
            "//*[@id='_T201286']/td/div/div[3]/div/div/table/tbody/tr").find_elements_by_tag_name("td")
        t = len(pages)
        # print(t)
        if t - 7 <= 9:
            for i in range(t - 7):
                driver.find_element_by_xpath(
                    "//*[@id='_T201286']/td/div/div[3]/div/div/table/tbody/tr/td[3]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div").click()
                time.sleep(3)
                driver.find_element_by_xpath(
                    "//*[@id='_T201286']/td/div/div[3]/div/div/table/tbody/tr/td[3]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div")
                cls.load_Table(i)
                print("获取报表第" + str(i + 1) + "页数据成功！")
        else:
            for i in range(t - 7):
                driver.find_element_by_xpath(
                    "//*[@id='_T201286']/td/div/div[3]/div/div/table/tbody/tr/td[4]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div").click()
                time.sleep(3)
                driver.find_element_by_xpath(
                    "//*[@id='_T201286']/td/div/div[3]/div/div/table/tbody/tr/td[4]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div")
                cls.load_Table(i)

    def load_Table(cls, page):
        '''获取报表页面数据'''
        # 创建工作簿
        driver = cls.driver
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建工作表
        sheet = wbk.add_sheet('Web_data', cell_overwrite_ok=True)
        excel = r"F:\PyTesting\AutoTest\log\excel\Warn_TARG.xls"
        table_rows = driver.find_element_by_xpath(
            "//*[@id='_T201286']/td/div/div[1]/table").find_elements_by_tag_name('tr')
        row = 20
        for i, tr in enumerate(table_rows):  # enumerate()是python的内置函数.enumerate多用于在for循环中得到计数
            if i == 0 and page == 0:
                table_cols1 = tr.find_elements_by_tag_name('th')
                for j, tc in enumerate(table_cols1):
                    sheet.write(i, j, tc.text)
                    wbk.save(excel)
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

    def test_4get_dbdata(cls):
        '''获取数据库中的数据'''
        sql = "select h.v_targ_id,h.v_targ_name,t.n_warn_type,t.d_warn_date  from GPS_TARG h,WARN_HISTORY t where h.v_targ_id= t.v_targ_id and t.d_warn_date between " \
              "to_date('2018-08-08 00:00:00','yyyy-mm-dd hh24:mi:ss') and to_date('2018-08-08 23:59:59','yyyy-mm-dd hh24:mi:ss')"
        scrpath = "F:\\PyTesting\\AutoTest\\log\\excel\\"  # 指定的保存目录
        export(sql, scrpath + r'WARN_TARG_DB.xlsx')
        print("获取数据库数据成功！")

    def test_5get_dbdata(cls):
        '''报警警告报表数据查询验证'''
        excel = "F:\\PyTesting\\AutoTest\\log\\excel\\Warn_TARG.xls"
        excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\WARN_TARG_DB.xlsx"
        test_read_excel(excel, excel1, "Warn_Result.xlsx")

    def test_6login_out(cls):
        '''退出登录'''
        driver = cls.driver
        driver.find_element_by_id("gps_main_quit_span_w").click()
        time.sleep(2)
        driver.find_element_by_xpath("//body//div//div//div//button/span[./text()='确定']").click()
        print("退出成功！")


if __name__ == '__main__':
    unittest.main()
