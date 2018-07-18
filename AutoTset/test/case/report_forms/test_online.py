# coding:utf-8
from selenium import webdriver
from xlutils3.copy import copy  # 将xlrd.Book转为xlwt.workbook，在原有的excel基础上进行修改，添加等。
import xlwt  # 写入excel（新建）
import xlrd  # 读取excel
import os
import time
import cx_Oracle
from openpyxl import Workbook
import sys

sys.path.append('F:\\PyTesting\\AutoTset\\public')
from Login_c import login
from GetVerifyCode import get_code
from Data_Comp import test_read_excel
import unittest


class Test_online(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("开始测试")
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get('http://192.168.10.110:8080/WebGis/login')
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
        login(driver, 'baoyong123', 'asdf1234', CodeText)  # 正确用户名和密码
        driver.implicitly_wait(10)  # 隐式等待
        username = driver.find_element_by_id("gps_main_username_span_w").text
        conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
        cursor = conn.cursor()
        cursor.execute("select t.v_user_name from GPS_USER t where t.v_user_account='baoyong123'")  # 引用定义变量
        rows = cursor.fetchall()  # 得到所有数据集
        for row in rows:
            print("%s" % (row[0]))
        try:
            assert username == row[0]
            print('登录成功！')
        except AssertionError as e:
            print('登录失败！')

    def test_2skip(cls):
        '''跳转到报表查询界面'''
        driver = cls.driver
        driver.find_element_by_id("gps_toolbar_leftbutton_div_w").click()
        driver.find_element_by_id("gps_main_menu_report_s_p").click()
        time.sleep(2)  # 等待元素加载
        driver.find_element_by_xpath("//*[@id='online']//div[1]//li[2]/a").click()
        time.sleep(2)

    def test_3switch_page(cls):
        '''分页跳转,获取分页中的所有数据'''
        driver = cls.driver
        pages = driver.find_element_by_xpath(
            "//*[@id='_T202758']/td/div/div[3]/div/div/table/tbody/tr").find_elements_by_tag_name("td")
        t = len(pages)
        # print(t)
        if t - 7 <= 9:
            for i in range(t - 7):
                driver.find_element_by_xpath(
                    "//*[@id='_T202758']/td/div/div[3]/div/div/table/tbody/tr/td[3]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div").click()
                time.sleep(3)
                driver.find_element_by_xpath(
                    "//*[@id='_T202758']/td/div/div[3]/div/div/table/tbody/tr/td[3]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div")
                cls.load_Table(i)
        else:
            for i in range(t - 7):
                driver.find_element_by_xpath(
                    "//*[@id='_T202758']/td/div/div[3]/div/div/table/tbody/tr/td[4]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div").click()
                time.sleep(3)
                driver.find_element_by_xpath(
                    "//*[@id='_T202758']/td/div/div[3]/div/div/table/tbody/tr/td[4]/div/table/tbody/tr/td[" + str(
                        i + 1) + "]/div")
                cls.load_Table(i)

    def load_Table(cls, page):
        '''获取报表页面数据'''
        # 创建工作簿
        driver = cls.driver
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建工作表
        sheet = wbk.add_sheet('Web_data', cell_overwrite_ok=True)
        excel = r"F:\PyTesting\AutoTset\log\excel\GPS_TARG.xls"
        table_rows = driver.find_element_by_xpath(
            "//*[@id='_T202758']/td/div/div[1]/table").find_elements_by_tag_name('tr')
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
        print('获取报表数据成功！')

    def test_4get_dbdata(cls):
        '''获取数据库中的数据'''
        conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
        cursor = conn.cursor()
        count = cursor.execute(
            "select p.v_user_account,q.v_targ_name from GPS_USER p,GPS_TARG q where p.v_dept_id=q.v_dept_id and p.v_user_account='baoyong123'")
        # 重置游标的位置
        # cursor.scroll(0,mode='absolute')
        # 搜取所有结果
        results = cursor.fetchall()

        # 获取oracle里面的数据字段名称
        fields = cursor.description
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('DB_data', cell_overwrite_ok=True)

        # 写上字段信息
        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])

        # 获取并写入数据段信息
        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row - 1][col])
        scrpath = 'F:\\PyTesting\\AutoTset\\log\\excel\\'  # 指定的保存目录
        workbook.save(scrpath + r'GPS_TARG_DB.xlsx')
        cursor.close()
        conn.close()
        print("获取数据库数据成功！")

    def test_5get_dbdata(cls):
        '''上离线报表数据查询验证'''
        test_read_excel()

    def test_6login_out(cls):
        '''退出登录'''
        driver = cls.driver
        driver.find_element_by_id("gps_main_quit_span_w").click()
        time.sleep(2)
        driver.find_element_by_xpath("//body//div//div//div//button/span[./text()='确定']").click()
        print("退出成功！")


if __name__ == '__main__':
    unittest.main()
