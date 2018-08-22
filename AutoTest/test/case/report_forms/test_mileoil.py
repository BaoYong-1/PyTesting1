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
        pages = driver.find_element_by_xpath("//*[@id='_T201414']//div[3]").find_elements_by_tag_name("td")
        t = len(pages)
        # print(t)
        # if t - 6 <= 7:
        for i in range(t - 7):
            # 循环点击页码
            driver.find_element_by_xpath("//*[@id='_T201414']//tbody//div//td[" + str(i + 1) + "]").click()
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
        excel = r"F:\PyTesting\AutoTest\log\excel\Mile.xls"
        # 查找页面数据，xpath为报表数据的路径
        table_rows = driver.find_element_by_xpath("//*[@id='_T201414']/td/div/div[1]/table").find_elements_by_tag_name(
            'tr')
        # print(table_rows)
        row = 20
        for i, tr in enumerate(table_rows):  # enumerate()是python的内置函数.enumerate多用于在for循环中得到计数
            # 获取页面table中的标题
            if i == 0 and page == 0:
                table_cols1 = tr.find_elements_by_tag_name('th')
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
        test.Click("id", "id201414")
        test.wait(5)
        report_name = test.Get_text("xpath", "//*[@id='rnavigation']/li[2]/span[2]")
        try:
            cls.assertEqual(report_name, '车辆行驶里程及油耗报表')
            log.info("跳转到车辆里程油耗报表查询界面")
        except AssertionError as e:
            test.get_windows_img('车辆里程油耗报表跳转')
            print("找不到报表标题：", report_name)
            raise

    def test_3get_dbdata(cls):
        '''获取数据库中数据'''
        sql1 = "select t.d_static_date as 日期,h.v_targ_name as 车牌号,f.v_dept_name as 所属公司,h.v_plat_id as 所属平台,t.v_targ_duration as 行驶时间,t.n_total_mileage as 里程,t.n_refuel as 加油量,t.n_fuel_consumption as 用油量 " \
               "from  BI_TARG_STATIC_D t ,GPS_TARG h,GPS_DEPT f " \
               "where h.v_dept_id=f.v_dept_id and t.v_targ_id=h.v_targ_id and t.d_static_date=to_date('" + Yestoday + "','YYYY-MM_DD')"
        scrpath = "F:\\PyTesting\\AutoTest\\log\\excel\\"  # 指定的保存目录
        export(sql1, scrpath + 'Mile_Y_DB.xlsx')
        log.info("获取数据库昨日数据")

    def test_4yestoday(cls):
        '''查询系统昨日数据'''
        driver = cls.driver
        test = BaseAction(driver)
        # 点击条件选择
        test.Click("xpath", "//*[@id='_R201414']//span[1]/span[2]")
        # 点击时间选择
        test.Click("xpath", "//*[@id='_R201414']//tr[1]/td[6]//div[2]/div")
        # 选中昨天
        test.Click("xpath", "//*[@id='_R201414']//tr[1]/td[6]//div[2]/li[1]")
        # 点击提交按钮
        test.Click("xpath", "//*[@id='_R201414']//div[1]//tr[2]//input")
        test.Wait(3)
        # 滚动到底部
        test.scrollLow("id", "inputPageText201414")  # 滑动到页面底部
        test.Wait(3)
        # 获取分页数据
        cls.switch_page()
        log.info("查询昨日数据,保存到excel")
        # 获取系统中的总计里程和时长
        excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\Mile.xls"
        excel = Excel(excel1, 0)
        row = excel.get_rows()
        col = excel.get_cols()
        sum_time = excel.get_cell_value(row - 1, col - 4)
        sum_mile = excel.get_cell_value(row - 1, col - 3)
        print("行驶总时间：", float(sum_time.split('秒')[0]))
        print("行驶总里程：", sum_mile)
        log.info("获取里程时间数据")

        # 获取数据库中的总计里程和时长
        excel2 = "F:\\PyTesting\\AutoTest\\log\\excel\\Mile_Y_DB.xlsx"
        excel_db = Excel(excel2, 0)
        row1 = excel_db.get_rows()
        col1 = excel_db.get_cols()
        sum_mile1 = 0.0
        sum_time1 = 0.0
        for x in range(1, row1):
            sum_time1 = float(excel_db.get_cell_value(row1 - x, 4)) + sum_time1
            sum_mile1 = float(excel_db.get_cell_value(row1 - x, 5)) + sum_mile1
        print("数据库中行驶总时间：", sum_time1)
        print("数据库中行驶总里程：", sum_mile1)
        log.info("获取数据库中里程时间数据")
        sum_time1 == sum_time and sum_mile1 == sum_mile
        try:
            sum_time1 == sum_time and sum_mile1 == sum_mile
            log.info("数据查询成功！")
        except AssertionError as e:
            log.info("数据查询失败,页面数据和系统数据不一致！")
            raise
        log.info("验证数据")

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
