import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# from Common.readdata import ReadData as R
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(ROOT_DIR)
sys.path.append('F:\\PyTesting\\AutoTest\\public')
from GetVerifyCode import get_code
from ConfigParser import ReadConfigFile


class BaseAction(object):
    def __init__(self, driver):
        self.driver = driver
        self.browser_type = None

    # 跳转页面
    def Jumpwebpage(self, page, time_wait=3):
        self.driver.get(self.Getwebpage(page))
        self.driver.maximize_window()

        if isinstance(time_wait, int):
            time.sleep(time_wait)

    def Getwebpage(self, page):
        return R.ReadXmlData("%s.xml" % page, "page", 0, "url")

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()

    # 浏览器后退操作
    def back(self):
        self.driver.back()

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    # 保存图片
    def get_windows_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
        except NameError as e:
            self.get_windows_img()

    def Current_handel(self):
        # 这时切换到新窗口
        all_handles = self.driver.window_handles
        for handle in all_handles:
            self.driver.switch_to.window(handle)

    # 打开浏览器的方法
    def Openbrowser(self, url):
        self.driver.maximize_window()
        self.driver.get(url)

    # 关闭浏览器的方法
    def Closebrowser(self):
        self.driver.quit()

    # 输入内容方法
    def Input(self, type, value, inputvalue):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).send_keys(inputvalue)
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).send_keys(inputvalue)
        elif type == "id":
            self.driver.find_element_by_id(value).send_keys(inputvalue)
        elif type == "name":
            self.driver.find_element_by_name(value).send_keys(inputvalue)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).send_keys(inputvalue)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).send_keys(inputvalue)

    # 鼠标事件方法一
    def Click(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).click()
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).click()
        elif type == "id":
            self.driver.find_element_by_id(value).click()
        elif type == "name":
            self.driver.find_element_by_name(value).click()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).click()
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).click()

    # 鼠标事件方法二
    def Clear(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value).clear()
        elif type == "id":
            self.driver.find_element_by_id(value).clear()
        elif type == "name":
            self.driver.find_element_by_name(value).clear()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).clear()
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value).clear()

    # 验证元素是否存在
    def Check_element(self, type, value):
        if type == "xpath":
            self.driver.find_element_by_xpath(value)
        elif type == "id":
            self.driver.find_element_by_id(value)
        elif type == "name":
            self.driver.find_element_by_name(value)
        elif type == "link_text":
            self.driver.find_element_by_link_text(value)
        elif type == "partial_link_text":
            self.driver.find_element_by_partial_link_text(value)

    # 获取子元素
    def Select_child_elements(self, type, value1, value2):
        if type == "xpath":
            Select(self.driver.find_element_by_xpath(value1)).select_by_visible_text(value2)
        elif type == "id":
            Select(self.driver.find_element_by_id(value1)).select_by_visible_text(value2)
        elif type == "name":
            Select(self.driver.find_element_by_name(value1)).select_by_visible_text(value2)
        elif type == "link_text":
            Select(self.driver.find_element_by_link_text(value1)).select_by_visible_text(value2)
        elif type == "partial_link_text":
            Select(self.driver.find_element_by_partial_link_text(value1)).select_by_visible_text(value2)

    # 获取输入框的值
    def Get_attribute(self, type, value1, value2):
        if type == "xpath":
            Value = self.driver.find_element_by_xpath(value1).get_attribute(value2)
            return Value
        elif type == "name":
            Value = self.driver.find_element_by_name(value1).get_attribute(value2)
            return Value
        elif type == "link_text":
            Value = self.driver.find_element_by_link_text(value1).get_attribute(value2)
            return Value
        elif type == "class_name":
            Value = self.driver.find_element_by_class_name(value1).get_attribute(value2)
            return Value
        elif type == "id":
            Value = self.driver.find_element_by_id(value1).get_attribute(value2)
            return Value

            # 获取下拉框的文本的值

    def Get_text(self, type, value):
        if type == "xpath":
            text = self.driver.find_element_by_xpath(value).text
            return text
        elif type == "name":
            text = self.driver.find_element_by_name(value).text
            return text
        elif type == "link_text":
            text = self.driver.find_element_by_link_text(value).text
            return text
        elif type == "class_name":
            text = self.driver.find_element_by_class_name(value).text
            return text
        elif type == "id":
            text = self.driver.find_element_by_id(value).text
            return text

    # 显性等待时间
    def WebDriverWait(self, MaxTime, Mimtime, value):
        element = self.driver.find_element(By.ID, value)
        WebDriverWait(self.driver, MaxTime, Mimtime).until(EC.presence_of_element_located(element))

    # # 鼠标移动点击机制
    def Move_action(self, type, value):
        if type == "xpath":
            xm = self.driver.find_element_by_xpath(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "id":
            xm = self.driver.find_element_by_id(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "name":
            xm = self.driver.find_element_by_name(value)
            webdriver.ActionChains(self.driver).click(xm).perform()
        elif type == "link_text":
            xm = self.driver.find_element_by_link_text(value)
            webdriver.ActionChains(self.driver).click(xm).perform()

    # 校验按钮是否为选中状态
    def Is_selected(self, type, value):
        if type == "id":
            self.driver.find_element_by_id(value).is_selected()
        elif type == "xpath":
            self.driver.find_element_by_xpath(value).is_selected()
        elif type == "class_name":
            self.driver.find_element_by_class_name(value).is_selected()
        elif type == "name":
            self.driver.find_element_by_name(value).is_selected()
        elif type == "link_text":
            self.driver.find_element_by_link_text(value).is_selected()

# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     test=BaseAction(driver)
#     test.Openbrowser("http://192.168.10.110:8080/WebGis/login")
#     read = ReadConfigFile("Login")
#     item_list = read.get_PageObj_value()
#     user=item_list[0][1]
#     pwd=item_list[1][1]
#     code=item_list[2][1]
#     loginbtn=item_list[3][1]
#     print(user)
#     test.Input(user,"baoyong123")
#     test.Input(pwd,"asdf1234")
#     codetext=get_code(driver)
#     test.Input(code,codetext)
#     test.Click(loginbtn)
#     time.sleep(5)
#     test.Closebrowser()
