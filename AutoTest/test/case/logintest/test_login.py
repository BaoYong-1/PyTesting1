# coding:utf-8
import unittest
from selenium import webdriver
import time
import cx_Oracle
import sys
sys.path.append('F:\\PyTesting\\AutoTest\\public')
from GetVerifyCode import get_code
from Excel import Excel
from ConfigParser import ReadConfigFile

# 获取测试数据
login_data = "F:\\PyTesting\\AutoTest\\data\\test_data.xls"
excel = Excel(login_data, 0)
# 用户名list
user = excel.get_cols_data(1)
# 密码list
pwd = excel.get_cols_data(2)
class Test_login(unittest.TestCase):
    ''' 登录测试'''
    @classmethod
    def setUpClass(cls):
        print("开始测试")
    @classmethod
    def tearDownClass(cls):
        print("结束测试")
    def setUp(self):
        print("开始单个测试用例")
        self.dr = webdriver.Chrome()
        self.dr.maximize_window()
        read = ReadConfigFile("TestUrl")
        item_list = read.get_config_value()
        url = item_list[0][1]
        self.dr.get(url)
        time.sleep(5)
    def tearDown(self):
        print("结束单个测试用例")

    # 定义登录方法
    def login(self, username, password, CodeText):
        self.dr.find_element_by_id("txt_username").clear()
        self.dr.find_element_by_id("txt_username").send_keys(username)
        self.dr.find_element_by_id("txt_password").clear()
        self.dr.find_element_by_id("txt_password").send_keys(password)
        self.dr.find_element_by_id("verifycode").clear()
        self.dr.find_element_by_id("verifycode").send_keys(CodeText)
        self.dr.find_element_by_class_name("button").click()
        time.sleep(5)

    def test_01login_user_null(self):
        '''用户名、密码为空'''
        self.login('', '', '')  # 密码为空,验证码为空
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='请输入用户名后继续！']").text
        # 用assertEqual(a,b)方法来断言  a == b
        try:
            self.assertEqual(error_message, '请输入用户名后继续！')
            # 写入测试结果
            excel.write_cell_data(1, 6, 'pass')
            print("用户名、密码为空时点击登录测试通过！")
        except AssertionError as e:
            excel.write_cell_data(1, 6, 'fail')
            self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_user_null.png")
            print("测试失败,提示信息有误！")
            raise

    def test_02login_pwd_null(self):
        '''用户名正确、密码为空'''
        self.login(user[2], '', '')  # 密码为空,验证码为空
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='请输入密码后继续！']").text
        # 用assertEqual(a,b)方法来断言  a == b  请输入密码等于error_message
        try:
            self.assertEqual(error_message, '请输入密码后继续！')
            # 写入测试结果
            excel.write_cell_data(2, 6, 'pass')
            print("用户名正确、密码为空时点击登录测试通过！")
        except AssertionError as e:
            excel.write_cell_data(2, 6, 'fail')
            self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_pwd_null.png")
            print("测试失败,提示信息有误！")
            raise

    def test_03login_code_null(self):
        '''用户名密码正确、验证码为空'''
        self.login(user[3], pwd[3], '')  # 用户名密码正确、验证码为空
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='验证码不能为空']").text
        # 用assertEqual(a,b)方法来断言  a == b
        try:
            self.assertEqual(error_message, '验证码不能为空')
            # 写入测试结果
            excel.write_cell_data(3, 6, 'pass')
            print("用户名、密码正确，验证码为空时点击登录测试通过！")
        except AssertionError as e:
            excel.write_cell_data(3, 6, 'fail')
            self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_user_code_null.png")
            print("测试失败,提示信息有误！")
            raise

    def test_04login_user_error(self):
        '''用户名错误、密码正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login(user[4], pwd[4], CodeText)  # 密码正确，用户名错误,验证码正确
        time.sleep(2)
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='用户名或密码错误，请重新输入！']").text
        # 用assertIn(a,b)方法来断言 a in b
        try:
            self.assertIn('用户名或密码错误，请重新输入！', error_message)
            excel.write_cell_data(4, 6, 'pass')
            print("用户名错误、密码、验证码正确时点击登录测试通过！")
        except AssertionError as e:
            excel.write_cell_data(4, 6, 'fail')
            self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_user_error.png")
            print("测试失败,提示信息有误！")
            raise

    def test_05login_pwd_error(self):
        '''用户名正确、密码不正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login(user[5], pwd[5], CodeText)  # 正确用户名，错误密码
        time.sleep(2)
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='用户名或密码错误，请重新输入！']").text
        # 用assertIn(a,b)方法来断言 a in b
        try:
            self.assertIn('用户名或密码错误，请重新输入！', error_message)
            excel.write_cell_data(5, 6, 'pass')
            print("用户名、验证码正确，密码错误时点击登录测试通过！")
        except AssertionError as e:
            excel.write_cell_data(5, 6, 'fail')
            self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_pwd_error.png")
            print("测试失败,提示信息有误！")
            raise

    def test_06login_code_error(self):
        '''用户名密码正确、验证码错误'''
        self.login(user[6], pwd[6], 'aaaa')  # 用户名密码正确、验证码错误
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='验证码输入有误，请重新输入']").text
        # 用assertEqual(a,b)方法来断言  a == b
        try:
            self.assertEqual(error_message, '验证码输入有误，请重新输入')
            excel.write_cell_data(6, 6, 'pass')
            print("用户名、密码正确，验证码错误时点击登录测试通过！")
        except AssertionError as e:
            excel.write_cell_data(6, 6, 'fail')
            self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_user_code_error.png")
            print("测试失败,提示信息有误！")
            raise

    def test_07login_success(self):
        '''用户名、密码正确、验证码正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login(user[7], pwd[7], CodeText)  # 正确用户名和密码
        time.sleep(10)
        username = self.dr.find_element_by_id("gps_main_username_span_w").text
        conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
        cursor = conn.cursor()
        cursor.execute("select t.v_user_name from GPS_USER t where t.v_user_account='%s'" % user[7])  # 引用定义变量
        rows = cursor.fetchall()  # 得到所有数据集
        for row in rows:
            print('用户姓名：', "%s" % (row[0]))
        try:
            assert username == row[0]
            excel.write_cell_data(7, 6, 'pass')
            print('登录成功！')
        except AssertionError as e:
            excel.write_cell_data(7, 6, 'fail')
            print('登录失败！')
            raise
if __name__ == "__main__":
    unittest.main()
