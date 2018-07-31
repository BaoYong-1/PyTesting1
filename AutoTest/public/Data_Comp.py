import xlrd
import xlwt
import os

l_p = []  # 定义两个全局list，分别存储原始和目的需要对比的数据
l_t = []


def test_read_excel():
    scrpath = 'F:\\PyTesting\\AutoTest\\log\\excel\\'
    wb_pri = xlrd.open_workbook(scrpath + 'GPS_TARG.xls')  # 打开原始文件
    wb_tar = xlrd.open_workbook(scrpath + 'GPS_TARG_DB.xlsx')  # 打开目标文件
    wb_result = xlwt.Workbook()  # 新建一个文件，用来保存结果
    sheet_result = wb_result.add_sheet('Como_result', cell_overwrite_ok=True)
    result_i = 0
    result_j = 0
    sheet_pri = wb_pri.sheet_by_index(0)
    sheet_tar = wb_tar.sheet_by_index(0)
    # 为什么是取这一列，因为这就是需要对比的数据阿
    l_p = sheet_pri.col_values(1)
    l_t = sheet_tar.col_values(1)

    # 求参数在pri（原始数据）中存在，而在tar（目标）中不存在的
    tmp_pd = list(set(l_p).difference(set(l_t)))
    # 求参数在tar中存在，而在pri中不存在的
    tmp_td = list(set(l_t).difference(set(l_p)))

    if result_i < result_j:
        result_i = result_j
    else:
        result_j = result_i
    for pd_i in tmp_pd:
        result_i = result_i + 1
        sheet_result.write(result_i, 0, sheet_pri.name)
        sheet_result.write(result_i, 2, pd_i)
    for td_i in tmp_td:
        result_j = result_j + 1
        sheet_result.write(result_j, 1, sheet_tar.name)
        sheet_result.write(result_j, 3, td_i)

    # 好了，可以去名为result的excel中查看结果了
    wb_result.save(scrpath + 'Comp_result.xls')
    excle = xlrd.open_workbook(scrpath + 'Comp_result.xls')
    sheet = excle.sheets()[0]  # 获取第0个表
    n = sheet.nrows
    if n >= 3:
        print("页面数据和数据库数据不一致！")
    else:
        print("页面数据和数据库数据一致！")


if __name__ == '__main__':
    test_read_excel()
