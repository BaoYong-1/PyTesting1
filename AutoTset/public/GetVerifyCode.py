# coding=utf-8
from pytesseract import *
from selenium import webdriver
from PIL import Image, ImageEnhance
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置中文


def get_code(driver):
    imgelement = driver.find_element_by_id("verifyCodeImg")
    scrpath = 'F:\\PyTesting\\AutoTset\\log\\png'  # 指定的保存目录
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
    i.close()
    im.close()
    newVerify.close()

    print("获取登录验证码：", CodeText)
    return CodeText


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    url = "http://192.168.10.110:8080/WebGis/login"
    driver.get(url)
    CodeText = get_code(driver)
    driver.quit()
