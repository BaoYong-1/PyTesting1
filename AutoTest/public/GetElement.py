# encoding=utf-8
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getElement(driver, locateType, locateExpression):
    # 获取页面单个元素
    try:
        return WebDriverWait(driver, 10).until(lambda x: x.find_element(locateType, locateExpression))
    except Exception as e:
        raise e


def get_Element(driver, *loc):
    try:
        # 确保元素是可见的。
        # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
        # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
        # 注意：以下入参本身是元组，不需要加*
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(loc))
        return driver.find_element(*loc)
    except:
        print(u"%s 页面中未能找到 %s 元素" % (driver, loc))


def getElements(driver, locateType, locateExpression):
    # 获取页面多个元素
    try:
        wait = WebDriverWait(driver, 10)
        return wait.until(lambda x: x.find_elements(locateType, locateExpression))
    except Exception as e:
        raise e


def getSelectElementWithIndex(driver, index_num):
    # 获取select下拉框元素---index
    select_element = Select(driver.find_element_by_xpath('//select'))
    # 打印已选中的文本
    print(select_element.all_selected_options[0].text)
    return select_element.select_by_index(index_num)


def getSelectElementWithText(driver, text):
    # 获取select下拉框元素----text
    select_element = Select(driver.find_element_by_xpath('//select'))
    # 打印已选中的文本
    print(select_element.all_selected_options[0].text)
    return select_element.select_by_visible_text(text)


def getSelectElementWithValue(driver, value):
    # 获取select下拉框元素---value
    select_element = Select(driver.find_element_by_xpath('select'))
    # 打印已选中的文本
    print(select_element.all_selected_options[0].text)
    return select_element.select_by_value(value)
