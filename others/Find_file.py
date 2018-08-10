# coding:utf-8
import unittest
from selenium import webdriver
import sys

sys.path.append('F:\\PyTesting\\AutoTest\\public')
from GetVerifyCode import get_code
from ConfigParser import ReadConfigFile
import time
import cx_Oracle
from Get_DB_Data import export
import time, datetime

global scrpath, begin_time, end_time
scrpath = 'F:\\PyTesting\\AutoTest\\log\\excel\\'  # 指定的保存目录
read = ReadConfigFile("SQL")
item_list = read.get_config_value()
begin_time = item_list[0][1]
end_time = item_list[1][1]


def test_004():
    '''测B10004'''
    print(begin_time)
    user = 'baoyong123'
    sql004 = "select * from OPERATING_COMMAND_MSG t where t.v_equipment_id='0000013100000004' and t.v_text_send like '%疲劳%' and t.d_time between to_date('" + begin_time + "','yyyy-mm-dd hh24:mi:ss') and to_date('2018/06/22 23:59:59','yyyy-mm-dd hh24:mi:ss')"

    sql = "select t.v_user_name from GPS_USER t where t.v_user_account='%s'" % user
    export(sql004, scrpath + '测B10004.xlsx')


if __name__ == "__main__":
    test_004()
