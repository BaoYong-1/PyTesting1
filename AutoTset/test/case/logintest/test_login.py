# coding:utf-8
import unittest
from selenium import webdriver
import sys
sys.path.append('F:\\PyTesting\\AutoTset\\public')
from GetVerifyCode import get_code
import time
import cx_Oracle


class Test(unittest.TestCase):
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
        self.dr.get('http://192.168.10.110:8080/WebGis/login')
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

    def test_login_success(self):
        '''用户名、密码正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login('baoyong123', 'asdf1234', CodeText)  # 正确用户名和密码
        time.sleep(10)
        username = self.dr.find_element_by_id("gps_main_username_span_w").text
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

    def test_login_pwd_error(self):
        '''用户名正确、密码不正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login('baoyong123', 'asdf1', CodeText)  # 正确用户名，错误密码
        time.sleep(2)
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='用户名或密码错误，请重新输入！']").text
        self.assertIn('用户名或密码错误，请重新输入！', error_message)  # 用assertIn(a,b)方法来断言 a in b  '用户名或密码错误'在error_message里
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTset\\log\\png\\login_pwd_error.png")

    def test_login_pwd_null(self):
        '''用户名正确、密码为空'''
        self.login('baoyong123', '', '')  # 密码为空,验证码为空
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='请输入密码后继续！']").text
        self.assertEqual(error_message, '请输入密码后继续！')  # 用assertEqual(a,b)方法来断言  a == b  请输入密码等于error_message
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTset\\log\\png\\login_pwd_null.png")

    def test_login_user_error(self):
        '''用户名错误、密码正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login('baoyong', 'asdf1234', CodeText)  # 密码正确，用户名错误,验证码正确
        time.sleep(2)
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='用户名或密码错误，请重新输入！']").text
        self.assertIn('用户名或密码错误，请重新输入！', error_message)  # 用assertIn(a,b)方法来断言 a in b
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTset\\log\\png\\login_user_error.png")

    def test_login_user_null(self):
        '''用户名为空、密码正确'''
        driver = self.dr
        CodeText = get_code(driver)
        self.login('', 'asdf1234', CodeText)  # 用户名为空，密码正确,验证码正确
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='请输入用户名后继续！']").text
        self.assertEqual(error_message, '请输入用户名后继续！')  # 用assertEqual(a,b)方法来断言  a == b
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTset\\log\\png\\login_user_null.png")

    def test_login_code_error(self):
        '''用户名密码正确、验证码错误'''
        driver = self.dr
        self.login('baoyong123', 'asdf1234', 'aaaa')  # 用户名密码正确、验证码错误
        error_message = self.dr.find_element_by_xpath("//body//div//div[./text()='验证码输入有误，请重新输入！']").text
        self.assertEqual(error_message, '验证码输入有误，请重新输入！')  # 用assertEqual(a,b)方法来断言  a == b
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTset\\log\\png\\login_user_code_error.png")

if __name__ == "__main__":
    unittest.main()
