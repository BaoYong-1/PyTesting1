# coding:utf-8
import xlrd
import xlwt
import os
import re  # 正则模块
l_p = []  # 定义两个全局list，分别存储原始和目的需要对比的数据
l_t = []

def test_read_excel(n, wb_p, wb_t, result_name):
    scrpath = 'F:\\PyTesting\\AutoTest\\log\\excel\\'
    wb_pri = xlrd.open_workbook(wb_p)  # 打开原始文件
    wb_tar = xlrd.open_workbook(wb_t)  # 打开目标文件
    wb_result = xlwt.Workbook()  # 新建一个文件，用来保存结果
    sheet_result = wb_result.add_sheet('Como_result', cell_overwrite_ok=True)
    result_i = 0
    result_j = 0
    sheet_pri = wb_pri.sheet_by_index(0)
    sheet_tar = wb_tar.sheet_by_index(0)
    # 为什么是取这一列，因为这就是需要对比的数据阿
    l_p = sheet_pri.col_values(n)
    l_t = sheet_tar.col_values(n)

    # 求参数在pri（原始数据）中存在，而在tar（目标）中不存在的
    tmp_pd = list(set(l_p).difference(set(l_t)))
    # 求参数在tar中存在，而在pri中不存在的
    tmp_td = list(set(l_t).difference(set(l_p)))

    if result_i < result_j:
        result_i = result_j
    else:
        result_j = result_i
    sheet_result.write(0, 0, "数据对比结果：")
    for pd_i in tmp_pd:
        result_i = result_i +1
        sheet_result.write(result_i, 0, sheet_pri.name)
        sheet_result.write(result_i, 1, pd_i)
    for td_i in tmp_td:
        result_j = result_j + 1
        sheet_result.write(result_j, 2, sheet_tar.name)
        sheet_result.write(result_j, 3, td_i)

    # 好了，可以去名为result的excel中查看结果了
    wb_result.save(scrpath + result_name)
    excle = xlrd.open_workbook(scrpath + result_name)
    sheet = excle.sheets()[0]  # 获取第0个表
    n = sheet.nrows
    if n > 2:
        # print("页面数据和数据库数据不一致！")
        flag = False
    else:
        # print("页面数据和数据库数据一致！")
        flag = True
    # print(flag)
    return flag


def del_row(excel_dir, new_dir):
    scrpath = 'F:\\PyTesting\\AutoTest\\log\\excel\\'
    data = xlrd.open_workbook(excel_dir)
    nums = len(data.sheets())
    # print("nums:",nums)
    sheet1 = data.sheets()[0]
    # print("sheet1:",sheet1)
    # 获取行数
    nrows = sheet1.nrows
    # print("行数：",nrows)
    # 获取列数
    ncols = sheet1.ncols
    # print("列数：",ncols)
    # 定义空list
    rows_get = []
    # 循环行
    for i in range(nrows):
        # 获取第一列的各行数据
        A0 = sheet1.cell(i, 0).value
        # 去除首位空格
        A0 = A0.strip()
        # print("A0:",A0)
        # 不从第一行开始判断，因为第一行的姓名行我们需要保留，后面不需要，这里选3（根据具体情况而定）吧
        if i < 1:
            # 加入row_get
            rows_get.append(i)
        else:
            # 开始正则部分,规定正则格式，这里是匹配中文字符(因为表中含有continued table1行)
            p = r'[\u4e00-\u9fa5]|\（|\）|[0-9]'
            # 编译
            pattern = re.compile(p)
            # print("pattern:",pattern)
            # 在A0中匹配
            try:
                # 判断A0中是否存在中文字符（这里把英文，空行剔除了）
                ch_first = re.findall(pattern, A0)[
                    0]  # 因为空list不能([0])选择第一个元素,会显示错误（IndexError: list index out of range）
                # print("ch_first:",ch_first)
                # 剔除续表行
                if A0[0:2] == '编号':
                    # print("A0[0:2]:", A0[0:2])
                    pass
                # # 剔除姓名行
                elif A0[0:2] == '群发':
                    pass
                else:
                    rows_get.append(i)
                    # print("rows_get11:", rows_get)
            except:
                continue
        # 已经得到我们所需数据的行标数
    # print("rows_get:",rows_get)
    # 新建工作簿
    excel4 = "F:\\PyTesting\\AutoTest\\log\\excel\\ascii.xls"
    workbook = xlwt.Workbook(excel4)
    # 新建sheet
    sheet_w = workbook.add_sheet('Web_data')
    # 定义初始变量
    wx = 0
    # 循环rows_get
    for x in rows_get:
        for y in range(ncols):
            sheet_w.write(wx, y, sheet1.cell(x, y).value)  # wx,y 是写入sheet的行列标，sheet1.cell(x,y).value是原表我们需要的数据
        wx = wx + 1  # 行数加一，使得写入的sheet 行连续
    # 保存工作簿
    workbook.save(new_dir)


if __name__ == '__main__':
    # excel = "F:\\PyTesting\\AutoTest\\log\\excel\\History_TARG.xls"
    # excel1 = "F:\\PyTesting\\AutoTest\\log\\excel\\History_Yes_DB.xlsx"
    # test_read_excel(0,excel, excel1, "Yes_Result.xlsx")
    excel2 = "F:\\PyTesting\\AutoTest\\log\\excel\\MSG1.xls"
    excel3 = "F:\\PyTesting\\AutoTest\\log\\excel\\MSG2.xls"
    del_row(excel2, excel3)
