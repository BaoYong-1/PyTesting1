# coding:utf-8
import xlrd
import xlwt
from xlutils3.copy import copy

class Excel(object):
    def __init__(self, file_name=None, sheet_id=None):
        self.file_name = file_name
        self.sheet_id = sheet_id

    # 获取某一个单元格的内容
    def get_cell_value(self, row, col):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        cell = tables.cell_value(row, col)
        return cell

    # 获取单元格的行数
    def get_rows(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables.nrows

    # 获取单元格的列数
    def get_cols(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        return tables.ncols

    # 获取整行数据
    def get_rows_data(self, i):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        rows_data = tables.row_values(i)
        return rows_data

    # 获取整列数据
    def get_cols_data(self, i):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[self.sheet_id]
        cols_data = tables.col_values(i)
        return cols_data

    # 写入数据(覆盖)
    # def write_cell_data(self, row, col, value):
    #     data = xlwt.Workbook(encoding='utf-8', style_compression=0)
    #     tables = data.add_sheet('test', cell_overwrite_ok=True)
    #     tables.write(row, col, value)
    #     data.save(self.file_name)

    def write_cell_data(self, row, col, value):
        # 打开文件，并且保留原格式
        self.rbook = xlrd.open_workbook(self.file_name, formatting_info=True)
        # 使用xlutils的copy方法使用打开的excel文档创建一个副本
        self.wbook = copy(self.rbook)
        # 使用get_sheet方法获取副本要操作的sheet
        self.w_sheet = self.wbook.get_sheet(self.sheet_id)
        # 写入数据参数包括行号、列号、和值（其中参数不止这些）
        self.w_sheet.write(row, col, value)
        # 保存
        self.wbook.save(self.file_name)


if __name__ == '__main__':
    excel1 = 'F:\\PyTesting\\AutoTest\\log\\excel\\Mile_Y_DB.xlsx'
    opexcel = Excel(excel1, 0)
    print(opexcel.get_rows())
    print(opexcel.get_cols())
    print(opexcel.get_cell_value(1, 4))
    print(opexcel.get_rows_data(0))
    print(opexcel.get_cols_data(1))
    opexcel.write_cell_data(0, 2, 4, 'pass')

    # # 获取数据库中的总计里程和时长
    # excel2 = "F:\\PyTesting\\AutoTest\\log\\excel\\Mile_Y_DB.xlsx"
    # excel_db = Excel(excel2, 0)
    # row1 = excel_db.get_rows()
    # col1 = excel_db.get_cols()
    # sum_mile1 = 0.0
    # sum_time1 = 0.0
    # for x in range(1, row1):
    #     sum_time1 = float(excel_db.get_cell_value(row1 - x, 4)) + sum_time1
    #     sum_mile1 = float(excel_db.get_cell_value(row1 - x, 5)) + sum_mile1
    # print("数据库中行驶总时间：", sum_time1)
    # print("数据库中行驶总里程：", sum_mile1)
    # sum_time = '15秒'
    # print("行驶总时间：", float(sum_time.split('秒')[0]))
