# coding=utf-8
from selenium.webdriver.common.by import By
import sys

sys.path.append('F:\\PyTesting\\AutoTest\\test\\page')
from BasePage import BasePage


# 继承BasePage类
class ReportPage(BasePage):
    ToolBar_id = (By.ID, 'gps_toolbar_leftbutton_div_w')
    QueryButton_id = (By.ID, 'gps_main_menu_report_s_p')
    Warn_report_id = (By.ID, 'id201286')

    # 操作
    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    # 打开网页
    def click_toolbar(self):
        self.find_element(*self.ToolBar_id).click()

    def click_QueryButtonr(self):
        self.find_element(*self.QueryButton_id).click()

    def click_QueryButtonr(self):
        self.find_element(*self.Warn_report_id).click()
