import json
from flask import request
from flask_login import login_required
from . import excel
import numpy as np
from app.utils.return_code import ReturnMessage, ErrorMessage, error_handler
from app.project_excel.manager.excel_manager import ExcelManager


#创建新的一行需要的rowKey
@excel.route('/new_rowkey', methods=['POST'])
@error_handler
@login_required
def final_rowkey():
    try:
        excelName = request.args.get("excelName")
        excel_info = ExcelManager.get_all_excel_info(excel_name=excelName)
        sheets = list(excel_info.keys())
        excel_obj = ExcelManager.create_excel_obj(excelName)
        newrowkey = ''
        for sheet in sheets:
            roukeyinmysql = excel_obj.file[sheet][len(excel_obj.file[sheet]) - 1]['id']
            roukeyinmysql = int(roukeyinmysql.replace(excelName + "_", ""))
            newrowkey = excel_obj + '_' + str(roukeyinmysql)

        result = {
            "result": 200,
            "newrowkey" : newrowkey
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, str(e), 400)

# 点击删除按钮后从数据库删除该行
@excel.route('/del_row', methods=['DELETE'])
@error_handler
@login_required
def del_row():
    try:
        excelName = request.args.get("excelName")
        rowKey = request.args.get("rowKey")
        rowKey = int(rowKey.replace(excelName + "_", ""))

        excel_info = ExcelManager.get_all_excel_info(excel_name=excelName)
        sheets = list(excel_info.keys())

        excel_obj = ExcelManager.create_excel_obj(excelName)
        for sheet in sheets:
            # print(excel_obj.file[sheet][rowKey])
            excel_obj.file[sheet] = np.delete(excel_obj.file[sheet], rowKey)
            # print(excel_obj.file[sheet])
            for i in range(0, len(excel_obj.file[sheet])):
                # print(excel_obj.file[sheet][i])
                excel_obj.file[sheet][i]["id"] = excelName + '_' + str(i)

        excel_obj.validate()
        excel_obj.save()

        result = {
            "result": 200
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, str(e), 400)


# 点击保存按钮后保存该行数据到数据库中
@excel.route('/save_row', methods=['POST'])
@error_handler
@login_required
def save_row():
    try:
        excelName = request.args.get("excelName")   # test
        rowkeystr = request.args.get("rowKey") # test_122
        # columnKey = request.args.get("columnKey")
        newValue = request.args.get("newValue")
        newValue = json.loads(newValue)
        rowkeynum = int(rowkeystr.replace(excelName + "_", "")) # 122
        excel_info = ExcelManager.get_all_excel_info(excel_name=excelName)
        sheets = list(excel_info.keys())
        excel_obj = ExcelManager.create_excel_obj(excelName)

        for sheet in sheets:
            rowkeyindb = excel_obj.file[sheet][len(excel_obj.file[sheet])-1]['id']
            rowkeyindb = int(rowkeyindb.replace(excelName + "_", ""))
            columnKey = list(excel_info[sheet])
            # print(len(columnKey)) # 10

            if rowkeynum <= rowkeyindb:
                for i in range(len(columnKey) - 1):
                    # print(newValue[i])
                    # print("保存原来修改过的数据")
                    excel_obj.file[sheet][rowkeynum][columnKey[i]] = newValue[i]
            else:
                # print("保存新增的数据")
                dict = excel_obj.file[sheet]
                temp = {}
                for i in range(len(columnKey) - 1):
                    temp[columnKey[i]] = newValue[i]
                temp['id'] = rowkeystr
                # print(temp)
                dict.append(temp)
                excel_obj.file[sheet] = dict
                for i in range(0, len(excel_obj.file[sheet])):
                    excel_obj.file[sheet][i]["id"] = excelName + '_' + str(i)
        excel_obj.save()
        result = {
            "result": 200
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, str(e), 400)


# 导入excel后保存excel数据到数据库
@excel.route('/save_excel', methods=['POST'])
@error_handler
@login_required
def save_file():
    try:
        file = request.files["file"]
        excel, sheets = ExcelManager.read_excel(file)
        ExcelManager.save_excel(excel, file.filename, sheets)
        result = {
            "result": 200
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, e, 400)

# 点击左侧excel名称后，获取信息展示到右边
@excel.route('/get_excel', methods=['GET', 'POST'])
@error_handler
@login_required
def get_excel_info():
    try:
        excel_dict = {}
        excel_name = request.args.get("name")
        excel_info = ExcelManager.get_all_excel_info(excel_name=excel_name)
        sheets = list(excel_info.keys())
        for sheet in sheets:
            excel_dict[sheet] = {}
            columns = list(excel_info[sheet])
            # print(columns)
            excel_dict[sheet]["columns"] = columns
            excel_json = excel_info[sheet].to_json(force_ascii=False, orient="columns")
            excel_json = eval(excel_json)
            excel_dict[sheet]["data"] = excel_json
        total = len(excel_dict[sheet]["data"][columns[0]])

        result = {
            "total": total,
            "excel": excel_dict
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, str(e), 400)


@excel.route('/operate', methods=['GET', 'POST'])
@error_handler
@login_required
def get_operate_info():
    try:
        operate_str = request.args.get("operate")
        ExcelManager.get_operation(operate_str)
        result = {
            "result": 200
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, e, 400)


# 获取数据库中的全部excel名称列表
@excel.route('/get_excel_list', methods=['GET'])
@error_handler
@login_required
def get_excel_list():
    try:
        limit = request.args.get("limit", 10)
        skip = request.args.get("skip", 0)
        limit = int(limit)
        skip = int(skip)
        query_raw = {}
        excel_name = request.args.get("excel_name")
        if excel_name:
            query_raw["name"] = {"$regex": excel_name.strip()}

    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, str(e), 400)
    result = {
        "total": ExcelManager.get_excel_count(query_raw),
        "excels": [ExcelManager.to_list_item(p) for p in
                     ExcelManager.get_excel_list(query_raw, limit=limit, skip=skip)]
    }
    return ReturnMessage.build_success(result)


# 删除excel
@excel.route('/<name>', methods=['DELETE'])
@error_handler
@login_required
def delete_project(name):
    try:
        if not name:
            return ErrorMessage.INVALID_WPS_CODE
        ExcelManager.delete_excel(name)
        result = {
            "result": 200
        }
        return ReturnMessage.build_success(result)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, e, 400)