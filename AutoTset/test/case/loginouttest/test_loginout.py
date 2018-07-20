# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
import sys

sys.path.append('F:\\PyTesting\\AutoTset\\public')
from GetVerifyCode import get_code

sys.path.append('F:\\PyTesting\\AutoTset\\public')
from Login_c import login
import time
import cx_Oracle


class Test_out(unittest.TestCase):

    def setUp(self):
        self.dr = webdriver.Chrome()
        self.dr.maximize_window()
        self.dr.get('http://192.168.10.110:8080/WebGis/login')
        time.sleep(5)

    def test_login_out(self):
        u''' 退出登录'''
        driver = self.dr
        CodeText = get_code(driver)
        login(driver, 'baoyong123', 'asdf1234', CodeText)
        driver.find_element_by_id("gps_main_quit_span_w").click()
        time.sleep(2)
        driver.find_element_by_xpath("//body//div//div//div//button/span[./text()='确定']").click()
        time.sleep(3)
        message = self.dr.find_element_by_xpath("//html//body//div[@class='middle']").text
        self.assertIn('山东广安车联科技股份有限公司', message)
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTset\\log\\png\\login_out.png")
        print("退出成功！")

    def tearDown(self):
        self.dr.close()


# 从all_test中调用时，可以不要这个
if __name__ == "__main__":
    unittest.main()
