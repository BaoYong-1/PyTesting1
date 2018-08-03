# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
import sys
sys.path.append('F:\\PyTesting\\AutoTest\\public')
from Logger import Log
from GetVerifyCode import get_code
from Login_c import login
from ConfigParser import ReadConfigFile
import time
import cx_Oracle

log = Log()


class Test_login_out(unittest.TestCase):
    ''' 退出登录测试'''
    def setUp(self):
        log.info("-------登录退出测试开始---------")
        self.dr = webdriver.Chrome()
        log.info("打开浏览器")
        self.dr.maximize_window()
        log.info("最大化浏览器")
        read = ReadConfigFile("TestUrl")
        item_list = read.get_config_value()
        url = item_list[0][1]
        self.dr.get(url)
        time.sleep(5)

    def test_login_out(self):
        u''' 退出登录'''
        driver = self.dr
        CodeText = get_code(driver)
        login(driver, 'baoyong123', 'asdf1234', CodeText)
        log.info("用户登录")
        driver.find_element_by_id("gps_main_quit_span_w").click()
        log.info("点击退出按钮")
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("//body//div//div//div//button/span[./text()='确定']").click()
        log.info("点击确定按钮")
        driver.implicitly_wait(3)
        message = self.dr.find_element_by_xpath("//html//body//div[@class='middle']").text
        self.assertIn('山东广安车联科技股份有限公司', message)
        self.dr.get_screenshot_as_file("F:\\PyTesting\\AutoTest\\log\\png\\login_out.png")
        log.info("退出登录")

    def tearDown(self):
        self.dr.close()
        log.info("-------测试结束----------")


# 从all_test中调用时，可以不要这个
if __name__ == "__main__":
    unittest.main()
