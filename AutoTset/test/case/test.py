# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from xlutils3.copy import copy
import xlwt
import xlrd
import os
import time

'''
下载牛客网首页 > 在线编程 > 剑指Offer的题目表到excel
读取excel里的值
'''

driver = webdriver.Chrome()
driver.get("https://www.nowcoder.com/")
time.sleep(2)


def switch_window():
    # 获取当前句柄
    h = driver.current_window_handle
    # 跳转到指定页面
    element = driver.find_element_by_xpath("//*[@class='nowcoder-navbar']/li[2]/a")
    ActionChains(driver).move_to_element(element).perform()
    driver.find_element_by_xpath("//*[@class='sub-nav']/li[3]/a").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@class='topic-list clearfix']/li[1]").click()
    # 切换到指定页面
    driver.close()
    all_h = driver.window_handles
    for i in all_h:
        if i != h:
            driver.switch_to.window(i)


def load_Table(page):
    # 创建工作簿
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
    excel = r"F:\PyTesting\AutoTset\log\test.xls"
    table_rows = driver.find_element_by_xpath(
        "//*[@class='module-body offer-body']/table/tbody").find_elements_by_tag_name('tr')
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
    print('save done')


def switch_page():
    pages = driver.find_element_by_xpath("//*[@class='pagination']/ul").find_elements_by_tag_name('li')
    t = len(pages)
    print("t=" + str(t))
    for i in range(t - 4):
        driver.find_element_by_link_text(str(i + 1)).click()
        load_Table(i)


switch_window()
switch_page()
print('done')
