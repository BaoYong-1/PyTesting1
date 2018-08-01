import configparser
import os


class ReadConfigFile(object):
    def __init__(self, section, item):  # 初始化函数
        self.section = section
        self.item = item

    # def get_value(self):
    #     root_dir = os.path.dirname(os.path.abspath('.'))  # 获取项目的绝对路径
    #     config = configparser.ConfigParser()   # ConfigParser.py文件名与ConfigParser()需要一致
    #     file_path = root_dir + '\config\config.ini'
    #     config.read(file_path,encoding="utf-8")
    #
    #     section_list = config.sections()
    #     print(section_list)
    #
    #     option_list = config.options('TestReport')
    #     print(option_list)
    #
    #     item_list = config.items('TestReport')
    #     print(item_list)
    #
    #     url = config.get("TestUrl", "url")
    #     print(url)
    #
    #     url1 = config.getint("TestUrl", "url1")
    #     print(url1)
    #
    #     browser = config.get("TestReport","title")
    #     url = config.get("TestUrl", "url")
    #     return(browser, url)
    def get_config_value(self):
        # root_dir = os.path.dirname(os.path.abspath('.'))     # 获取项目的绝对路径
        config_dir = 'F:\PyTesting\AutoTest\config\config.ini'  # 如果需要调用该函数，需要写配置文件的绝对路径
        config = configparser.ConfigParser()  # ConfigParser.py文件名与ConfigParser()需要一致
        config.read(config_dir, encoding="utf-8")
        value = config.get(self.section, self.item)
        item_list = config.items('TestReport')
        print(item_list)
        print(value)
        return value


if __name__ == "__main__":  # 测试函数
    read = ReadConfigFile("TestReport", "title")
    testdata = read.get_config_value()
