from selenium import webdriver

del diver_ini():
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
url = "http://192.168.10.110:8080/WebGis/login"
driver.get(url)
