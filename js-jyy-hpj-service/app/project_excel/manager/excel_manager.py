import math
import re
import numpy as np
import pandas as pd
from .model import Excel
import xlrd
from app.project_excel.utils.operators_utils import *


class ExcelManager:

    @staticmethod
    def add_new_row_in_db(excelName, key, value):
        excel = Excel.objects(name=name).first()
        dict1 = excel["file"]

        excel["file"] = dict1
        excel.validate()
        excel.save()

    @staticmethod
    def create_excel_obj(excelName):
        excel = Excel.objects(name=excelName).first()
        return excel

    @staticmethod
    def read_excel(filepath):
        excel = pd.read_excel(filepath, sheet_name=None)
        sheets = list(excel.keys())
        return excel, sheets

    @staticmethod
    def delete_excel(name):
        Excel.objects(name=name).delete()

    @staticmethod
    def get_excel_count(query_raw=None):
        if query_raw:
            return Excel.objects(__raw__=query_raw).count()

        return Excel.objects().count()

    @staticmethod
    def to_list_item(excel):
        result = {
            "excel_name": excel.name,
            "file": excel.file
        }
        return result

    @staticmethod
    def get_excel_list(query_raw=None, limit=10, skip=0):
        if query_raw:
            return Excel.objects(__raw__=query_raw)[skip:skip + limit]

        return Excel.objects()[skip:skip + limit]

    @staticmethod
    def save_excel(excel_file, excel_name, sheets):
        name = excel_name.replace(".xlsx","").replace(".xls","")
        excel = Excel.objects(name=name).first()
        excel_dict = {}
        if not excel:
            excel = Excel()
        for sheet in sheets:
            excel_sheet = excel_file[sheet]
            excel_sheet = excel_sheet.fillna("None")
            df = excel_sheet.to_dict(orient='records')
            excel_dict[sheet] = df
        for i in range(0, len(excel_dict[sheet])):
            excel_dict[sheet][i]["id"] = name + '_' + str(i);
        excel["name"] = name
        excel["file"] = excel_dict
        excel.validate()
        excel.save()

    @staticmethod
    def get_all_excel_info(excel_name):
        excel = Excel.objects(name=excel_name).first()
        excel_info = excel.file
        sheets = list(excel_info.keys())
        for sheet in sheets:
            excel_info[sheet] = pd.DataFrame(excel_info[sheet])

        return excel_info

    @staticmethod
    def get_operation(operate):
        operate_copy = operate
        if not operate.count('(') == operate.count(')'):
            return "Illegal formats"
        operate = operate.replace(' ', '')
        print("operate is ",operate)
        for label in OPERATES:
            indexs = [m.start() for m in re.finditer(label, operate)]
            if not indexs:
                continue
            for left in indexs:
                right = operate[left:].index(')')
                s = operate[left:left + right+1]
                value, number = ExcelManager.calculate(s, label)
                operate_copy = operate_copy.replace(s, str(value))
        print(operate_copy)
        return

    @staticmethod
    def calculate(operates, label):
        left = operates.index('(')
        right = operates.index(')')
        excel_value = operates[left + 1:right].split(';')
        if label == "SUM":
            print("calculate sum")
            sum, number = ExcelManager.get_sum_data(excel_value)
            return sum, number
        if label == "AVERAGE":
            print("calculate average")
            sum, number = ExcelManager.get_sum_data(excel_value)
            return sum / number, number
        if label == "VAR":
            print("calculate variance")
            var, number = ExcelManager.get_var_data(excel_value)
            return var, number
        if label == "STAND":
            print("calculate standard")
            var, number = ExcelManager.get_var_data(excel_value)
            return math.sqrt(var), number

    @staticmethod
    def get_nub_char(data):
        index = 0
        for i in range(0, len(data)):
            if '0' <= data[i] <= '9':
                index = i
                break
        if index == 0:
            index = len(data)
        col = data[:index]
        row = data[index:]
        # 计算行和列
        if len(col) <= 1:
            col = ord(col)-65
        else:
            x = 0
            for index, value in enumerate(col):
                x = x*26 + (ord(value) - 64)
            col = x
        return col, row

    @staticmethod
    def get_sum_data(excel_value):
        sum = 0
        number = 0
        for excel in excel_value:
            excel = excel.split('.')
            excel_info = ExcelManager.get_all_excel_info(excel_name=excel[0])
            value_info = ExcelManager.get_excel_sheets(excel_info, excel[1], excel[2])
            value, count = ExcelManager.calculate_sum(value_info)
            print("计算的结果: {} ,总共 {} 条有效数据".format(value, count))
            sum += value
            number += count
        return sum, number

    @staticmethod
    def get_var_data(excel_value):
        value_info = None
        sum = 0
        number = 0
        for excel in excel_value:
            excel = excel.split('.')
            excel_info = ExcelManager.get_all_excel_info(excel_name=excel[0])
            value_info = ExcelManager.get_excel_sheets(excel_info, excel[1], excel[2])
            value, count = ExcelManager.calculate_sum(value_info)
            print("计算的结果: {} ,总共 {} 条有效数据".format(value, count))
            sum += value
            number += count
        mean = sum / number
        var, number = ExcelManager.calculate_var(value_info, mean)
        return var, number

    @staticmethod
    def calculate_sum(data):
        count = sum = 0
        for n in data:
            for x in n.flat:
                if type(x) != float :
                    continue
                sum += x
                count += 1
        return sum, count

    @staticmethod
    def calculate_var(data, mean):
        count = sum = 0
        for n in data:
            for x in n.flat:
                if type(x) != float :
                    continue
                sum += math.pow(abs(x-mean), 2)
                count += 1
        return sum / count, count

    @staticmethod
    def get_excel_sheets(excel, sheet_name, row_col=None):
        value_list = []
        excel_sheet = excel[sheet_name]
        left = row_col.index('[')
        right = row_col.index(']')
        row_col = row_col[left + 1:right]
        row_col = row_col.split(',')
        for info in row_col:
            row_col_info = info.split(':')
            value = ExcelManager.get_single_value(excel_sheet, row_col_info)
            value_list.append(value)
        return value_list

    @staticmethod
    def get_single_value(excel_sheet,row_col):
        if len(row_col) == 1:
            col, row = ExcelManager.get_nub_char(row_col[0])
            if row == '':
                col_value = excel_sheet.iloc[0:, [col]]
                col_numpy = np.array(col_value)
                return col_numpy
            else:
                row = int(row)
                value = excel_sheet.iat[row, col]
                value = np.array([value])
                print("value {} , type {}".format(value, type(value)))
                return value
        else:
            col_list = []
            row_list = []
            for info in row_col:
                col, row = ExcelManager.get_nub_char(info)
                col_list.append(col)
                row_list.append(row)
            if row_list.count('') == len(row_list):
                col_value = excel_sheet.iloc[0:, col_list[0]:col_list[1]+1]
                col_numpy = np.array(col_value)
                return col_numpy
            else:
                col_value = excel_sheet.iloc[int(row_list[0]): int(row_list[1])+1, col_list[0]:col_list[1] + 1]
                col_numpy = np.array(col_value)
                return col_numpy