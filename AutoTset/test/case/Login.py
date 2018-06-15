# coding=utf-8
import time
from pytesseract import *
from selenium import webdriver
from PIL import Image, ImageEnhance
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置中文


def get_code(driver):
    imgelement = driver.find_element_by_id("verifyCodeImg")
    scrpath = 'F:\\PyTesting\\AutoTset\\log'  # 指定的保存目录
    capturename = '\\' + 'verifyCode.png'  # 自定义命名截图
    wholepath = scrpath + capturename
    driver.save_screenshot(wholepath)  # 截取当前网页，该网页有我们需要的验证码
    # 获取验证码x,y轴坐标
    location = imgelement.location
    # 获取验证码的长宽
    size = imgelement.size
    # 写成我们需要截取的位置坐标
    rangle = (
    int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
    # 打开截图
    i = Image.open(wholepath)
    # 使用Image的crop函数，从截图中再次截取我们需要的区域
    imgry = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    capturename1 = '\\' + 'getVerifyCode.png'  # 自定义命名截图
    wholepath1 = scrpath + capturename1
    imgry.save(wholepath1)
    im = Image.open(wholepath1)
    im = im.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(im)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    capturename2 = '\\' + 'newVerifyCode.png'  # 自定义命名截图
    wholepath2 = scrpath + capturename2
    sharp_img.save(wholepath2)
    newVerify = Image.open(wholepath2)
    # 使用image_to_string识别验证码
    CodeText = image_to_string(newVerify).strip()
    # text = image_to_string('newVerifyCode.png').strip()
    print(CodeText)
    return CodeText

def login(driver, user, passwd, CodeText):
    driver.find_element_by_id("txt_username").clear()
    driver.find_element_by_id("txt_username").send_keys(user)
    driver.find_element_by_id("txt_password").clear()
    driver.find_element_by_id("txt_password").send_keys(passwd)
    driver.find_element_by_id("verifycode").clear()
    driver.find_element_by_id("verifycode").send_keys(CodeText)
    driver.find_element_by_class_name("button").click()
    time.sleep(5)
    username = driver.find_element_by_id("gps_main_username_span_w").text
    conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
    cursor = conn.cursor()
    cursor.execute("select t.v_user_name from GPS_USER t where t.v_user_account='%s'" % user)  # 引用定义变量
    rows = cursor.fetchall()  # 得到所有数据集
    for row in rows:
        print("%s" % (row[0]))
    try:
        assert username == row[0]
        print('登录成功！')
    except AssertionError as e:
        print('登录失败！')


def login_out(driver):
    driver.find_element_by_id("gps_main_quit_span_w").click()
    time.sleep(2)
    driver.find_element_by_xpath("//body//div//div//div//button/span[./text()='确定']").click()
    print("退出成功！")


def getData(driver):
    driver.find_element_by_id("gps_toolbar_leftbutton_div_w").click()
    driver.find_element_by_id("gps_main_menu_report_s_p").click()
    time.sleep(2)  # 等待元素加载
    driver.find_element_by_xpath("//*[@id='online']//div[1]//li[2]/a").click()
    time.sleep(2)

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    url = "http://192.168.10.110:8080/WebGis/login"
    driver.get(url)
    CodeText = get_code(driver)
    login(driver, 'baoyong', 'asdf1234', CodeText)
    getData(driver)
    login_out(driver)
    driver.quit()
