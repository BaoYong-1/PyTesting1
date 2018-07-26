import xlwt
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 设置中文


def export(sql, outputpath):
    conn = cx_Oracle.connect('gpsadmin/gpsadmin_123654@ 192.168.10.110: 1521 / ora11g')  # 连接数据库
    cursor = conn.cursor()
    count = cursor.execute(sql)
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
    scrpath = 'F:\\PyTesting\\AutoTset\\log\\excel\\'  # 指定的保存目录
    export(
        "select p.v_user_account,q.v_targ_name from GPS_USER p,GPS_TARG q where p.v_dept_id=q.v_dept_id and p.v_user_account='baoyong123'",
        scrpath + r'datetest.xlsx')
