# import cx_Oracle
# from openpyxl import Workbook
# import os
# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置中文
#
#
# def link_Oracle(wb):
#     create_wb(wb, 'helloDatas.xlsx')
#     ws = wb.create_sheet(title='我是第一个title', index=0)
#     conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
#     cursor = conn.cursor()
#     cursor.execute(
#        )
#     rows = cursor.fetchall()  # 得到所有数据集
#     for field_desc in cursor.description:
#         print(field_desc[0], end=' ,')
#         # print((field_desc[0]))
#     for row in rows:
#         print()
#         print("%s, %s" % (row[0], row[1]))
#     print("Number of rows returned: %d" % cursor.rowcount)
#     list_A_B = []  # list
#     rowcount1 = 1
#     for a in rows:
#         list_A_B.append(a)  # 末尾添加数据
#         rowcount1 = rowcount1 + 1
#     # 读取表字段值
#     db_title = [i[0] for i in cursor.description]
#     # 遍历表字段值
#     print(len(db_title))  # 2
#     for titleNum in range(len(db_title)):
#         A = ws.cell(row=1, column=1)
#         B = ws.cell(row=1, column=2)
#         A.value = db_title[titleNum]
#         B.value = db_title[titleNum]
#     # 读取数据到excel
#     print(rowcount1)
#     for rowNum in range(1, rowcount1):
#         A = ws.cell(row=rowNum + 1, column=1)
#         B = ws.cell(row=rowNum + 1, column=2)
#         # list_A_B索引从0开始，所以-1，list中存的是tuple，后面[0]获取的是tuple中的对应元素
#         A.value = list_A_B[rowNum - 1][0]
#         B.value = list_A_B[rowNum - 1][1]
#     cursor.close()
#     conn.close()
#     wb.save('helloDatas.xlsx')
#
#
# # 创建Excel
# def create_wb(wb, filename):
#     wb.save(filename=filename)
#     print("新建Excel：" + filename + "成功")
#
#
# if __name__ == '__main__':
#     wb = Workbook()
#     link_Oracle(wb)
# coding:utf8

import xlwt
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置中文


def export(sql, outputpath):
    conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
    cursor = conn.cursor()
    count = cursor.execute(sql)
    print(count)
    # 重置游标的位置
    # cursor.scroll(0,mode='absolute')
    # 搜取所有结果
    results = cursor.fetchall()
    # 获取MYSQL里面的数据字段名称
    fields = cursor.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet 1', cell_overwrite_ok=True)
    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])
    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(results) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row - 1][col])
    workbook.save(outputpath)
    print("获取数据库数据成功！")


# 结果测试
if __name__ == "__main__":
    scrpath = 'F:\\PyTesting\\AutoTest\\log\\excel\\'  # 指定的保存目录
    export(
        "select p.v_user_account,q.v_targ_name from GPS_USER p,GPS_TARG q where p.v_dept_id=q.v_dept_id and p.v_user_account='baoyong123'",
        scrpath + r'datetest.xlsx')
