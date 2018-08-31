# coding:utf-8
from selenium import webdriver
from xlutils3.copy import copy  # 将xlrd.Book转为xlwt.workbook，在原有的excel基础上进行修改，添加等。
import xlwt  # 写入excel（新建）
import xlrd  # 读取excel
import os
import time
import unittest
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
t_date = get_time.t_date
t_date1 = get_time.t_date1
t_date2 = get_time.t_date2
last_week_start = get_time.last_week_start


class Test_Log(unittest.TestCase):
    ''' 平台用户操作记录报表查询测试'''

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
        # 第一次分页，页数少于5
        pages = driver.find_element_by_xpath("//*[@class='easierui_gps_bottom_fillet']/ul").find_elements_by_tag_name(
            "li")
        t = len(pages)
        # 第二次分页，点击尾页按钮，获取页码总数，页数较多时
        driver.find_element_by_xpath("//*[starts-with(@ id, 'easier_edittable_')]/ li[" + str(t - 2) + "]").click()
        page = driver.find_element_by_xpath("//*[@class='easierui_gps_bottom_fillet']/ul").find_elements_by_tag_name(
            "li")
        t1 = len(page)
        # 倒数，获取最后一页的坐标位置
        last_1 = str(t1 - 4)
        # 倒数，获取“下一页”按钮的坐标位置
        last_2 = str(t1 - 3)
        # 获取最后一页的对象
        last = driver.find_element_by_xpath("//*[starts-with(@ id, 'easier_edittable_')]/ li[" + last_1 + "]")
        # 获取总页码数
        last_page = str(last.text)
        print("总页数：", last_page)
        # 点击首页按钮，返回首页
        driver.find_element_by_xpath("//*[starts-with(@ id, 'easier_edittable_')]/ li[1]").click()
        # 循环点击所有页码
        for i in range(t - 6):
            # 循环点击页码
            driver.find_element_by_xpath(
                "//*[@class='main_table']//tr//div/div[3]/table//tr//div//li[" + str(i + 3) + "]").click()
            time.sleep(2)
            # 保存每页的数据
            cls.load_Table(i)
            print("获取报表第" + str(i + 1) + "页数据成功！")
            if i == 4:
                for i1 in range(5, int(last_page)):
                    driver.find_element_by_xpath(
                        "//*[starts-with(@ id, 'easier_edittable_')]/ li[" + last_2 + "]").click()
                    cls.load_Table(i1)
                    i1 = i1 + 1
                    print("获取报表第" + str(i1) + "页数据成功！")

    def load_Table(cls, page):
        '''获取报表页面数据'''
        # 创建工作簿
        driver = cls.driver
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建工作表
        sheet = wbk.add_sheet('Web_data', cell_overwrite_ok=True)
        excel = r"F:\PyTesting\AutoTest\log\excel\USER_LOG.xls"
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
        # 删除多余行
        del_row(excel, excel)

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
        time.sleep(3)
        test.Click("id", "id600001")
        time.sleep(3)
        test.get_windows_img('跳转成功')
        report_name = test.Get_text("xpath", "//*[@id='rnavigation']/li[2]/span[2]")
        try:
            cls.assertEqual(report_name, '平台用户操作记录报表')
        except AssertionError as e:
            print("找不到报表标题：", report_name)
            raise

    def test_3getdata(cls):
        '''跳转到报表查询界面,获取页面数据'''
        driver = cls.driver
        test = BaseAction(driver)
        # 点击条件选择
        test.Click("xpath", "//*[@id='comptrollerData_searchHeader']//td[1]/span[2]")
        test.Wait(1)
        # 输入要查询的用户
        test.Input("id", "userName", "baoyong123")
        # 点击开始时间控件
        test.Click("xpath", "//*[@id='dataStartTime']")
        test.Wait(1)
        # 执行js,使时间控件可读
        js = 'document.getElementById("dataStartTime").removeAttribute("readonly")'
        js1 = 'document.getElementById("dataEndTime").removeAttribute("readonly")'
        test.Excecute_Script(js)
        test.Excecute_Script(js1)
        # 输入查询开始和结束时间
        test.Input("id", "dataStartTime", t_date2)
        # 点击结束时间控件
        test.Click("xpath", "//*[@id='dataEndTime']")
        test.Input("id", "dataEndTime", t_date1)

        # js_begin = 'document.getElementById("dataStartTime").value="2018-08-20"'
        # js_end = 'document.getElementById("dataEndTime").value="2018-08-27"'
        # test.Excecute_Script(js_begin)
        # test.Excecute_Script(js_end)
        test.Click("id", "comptrollerData_submit")
        log.info("提交")
        test.Wait(3)
        cls.switch_page()

    def test_4get_dbdata(cls):
        '''获取数据库中数据'''
        sql1 = "select t.n_type,e.v_user_account,h.value,t.v_content,t.d_date from PLAT_USER_BEHAVIOR t,GPS_USER e ,GPS_ENUM h  where " \
               "t.n_type=h.key and h.type='BEHAVIOR_TYPE' and t.v_user_id=e.v_user_id  and e.v_user_account='baoyong123' and t.d_date " \
               "between to_date('" + last_week_start + " 00:00:01', 'yyyy-mm-dd hh24:mi:ss') and to_date('" + t_date + " 23:59:59', 'yyyy-mm-dd hh24:mi:ss')"
        scrpath = "F:\\PyTesting\\AutoTest\\log\\excel\\"  # 指定的保存目录
        export(sql1, scrpath + 'USER_LOG_DB.xlsx')
        log.info("获取数据库用户行为日志")

    def test_5datacomp(cls):
        '''验证数据'''
        excel = "F:\\PyTesting\\AutoTest\\log\\excel\\USER_LOG.xls"
        excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\USER_LOG_DB.xlsx"
        try:
            cls.assertTrue(test_read_excel(3, excel, excel1, "USER_LOG_Result.xlsx"))
            print("数据查询成功！")
        except AssertionError as e:
            log.info("数据查询失败,页面数据和系统数据不一致！")
            raise

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
