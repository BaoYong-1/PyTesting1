# coding:utf-8
import xlrd
import xlwt

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

    # 写入数据
    def write_cell_data(self, row, col, value):
        data = xlwt.Workbook(encoding='utf-8', style_compression=0)
        tables = data.add_sheet('test', cell_overwrite_ok=True)
        tables.write(row, col, value)
        data.save(self.file_name)


if __name__ == '__main__':
    excel1 = 'F:\\PyTesting\\AutoTest\\log\\excel\\Mile_Y_DB.xlsx'
    opexcel = Excel(excel1, 0)
    print(opexcel.get_rows())
    print(opexcel.get_cols())
    print(opexcel.get_cell_value(1, 4))
    print(opexcel.get_rows_data(0))
    print(opexcel.get_cols_data(1))
    # opexcel.write_cell_data(2,4,'15')

    # 获取数据库中的总计里程和时长
    excel2 = "F:\\PyTesting\\AutoTest\\log\\excel\\Mile_Y_DB.xlsx"
    excel_db = Excel(excel2, 0)
    row1 = excel_db.get_rows()
    col1 = excel_db.get_cols()
    sum_mile1 = 0.0
    sum_time1 = 0.0
    for x in range(1, row1):
        sum_time1 = float(excel_db.get_cell_value(row1 - x, 4)) + sum_time1
        sum_mile1 = float(excel_db.get_cell_value(row1 - x, 5)) + sum_mile1
    print("数据库中行驶总时间：", sum_time1)
    print("数据库中行驶总里程：", sum_mile1)
    sum_time = '15秒'
    print("行驶总时间：", float(sum_time.split('秒')[0]))

# # encoding=utf-8
# from openpyxl import Workbook
# from openpyxl import load_workbook
# from openpyxl.styles import Border, Side, Font
# import xlrd
# import xlwt
# class Excel(object):
#
#     def __init__(self):
#         self.font = Font(color=None)
#         self.colorDict = {'red': 'FFFF3030', 'green': 'FF008B00'}
#         self.wb = xlrd.open_workbook(test_path)
#         self.ws = self.wb
#
#     def rename(self, new_name):
#         # 给表格重命名
#         self.ws.title = new_name
#         self.wb.save(test_path)
#
#     def GetSheetName(self):
#         # 获取所有表格名称
#         return self.wb.get_sheet_names()
#
#     def GetSheetByName(self, sheet_name):
#         # 通过表格名称获取表格
#         self.ws = self.wb.get_sheet_by_name(sheet_name)
#         return self.ws
#
#     def GetCurrentSheetName(self):
#         # 获取当前表格名称
#         return self.ws.title
#
#     def GetCellContent(self, row_num, col_num):
#         # 获取单元格内容
#         return self.ws.cell(row=row_num, column=col_num).value
#
#     def WriteCellContent(self, row_num, col_num, content):
#         # 往指定的单元格里面写入内容
#         self.ws.cell(row=row_num, column=col_num).value = content
#         self.wb.save(test_path)
#
#     def GetMaxRow(self):
#         # 获取最大行号
#         return self.ws.max_row
#
#     def GetMaxColumn(self):
#         # 获取最大列号
#         return self.ws.max_column
#
#
# if __name__ == "__main__":
#     test_path = "F:\\PyTesting\\AutoTest\\log\\excel\\Mile.xls"
#     excel = Excel()
#     n = excel.GetMaxRow()
#     print(n)
