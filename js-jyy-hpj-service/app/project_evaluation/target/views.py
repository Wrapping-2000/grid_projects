from . import target
from flask import request
from flask_login import login_required

from app.utils.return_code import ReturnMessage, ErrorMessage, error_handler
from app.project_evaluation.utils.target_utils import target_primary_index, target_status
from app.project_evaluation.manager import TargetAggregateManager, TargetManager
from app.project_evaluation.utils import ContrastFiledParam, PROJECT_CLASSIFICATION, PROJECT_VOLTAGE_LEVEL
from app.project_evaluation.target.target_project import TargetViewsManager


@target.route('/list/<primary_index>', methods=['GET'])
@error_handler
@login_required
def target_list(primary_index):
    """ 获取指标列表
        "show_type 1:列表 2:柱状图/折线图+列表 3:柱状图/饼图+列表"
    ---
    tags:
    - "target"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: primary_index
        required: true
        type: string
        in: path
        enum:
          - construction_control
          - operation_effect
          - investment_control
      - name: search
        required: false
        type: string
        in: query
    definitions:
      Target:
          type: object
      TargetList:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: array
            items:
              $ref: "#/definitions/Target"
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/TargetList"
    """
    secondary_index = target_primary_index.get(primary_index)
    search = request.args.get("search", "").strip()
    if not secondary_index:
        return ErrorMessage.INVALID_PRIMARY_INDEX

    result = {}
    for third_key, third_index in secondary_index.items():
        for k, name_list in third_index.items():
            if search:
                name_list = list(filter(lambda name: search in name, name_list))
            if name_list:
                result.setdefault(third_key, {})[k] = [{"name": name, "show_type": target_status.get(name)["show_type"]}
                                                       for name in name_list]

    return ReturnMessage.build_success(result)


@target.route('/project_list', methods=['GET'])
@error_handler
@login_required
def project_list():
    """ 根据指标值获取项目列表
    ---
    tags:
    - "target"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: name
        required: true
        type: string
        in: query
      - name: project_name
        required: false
        type: string
        in: query
      - name: voltage_level
        required: false
        type: integer
        in: query
      - name: classification
        required: false
        type: string
        in: query
      - name: operation_year
        required: false
        type: integer
        in: query
      - name: company
        required: false
        type: string
        in: query
      - name: contrast_filed
        required: false
        type: string
        in: path
        enum:
          - classification
          - voltage_level
          - company
          - operation_year
      - name: status
        required: false
        type: string
        in: query
      - name: target_year
        required: false
        type: integer
        in: query
      - name: start
        required: false
        type: float
        in: query
      - name: end
        required: false
        type: float
        in: query
      - name: limit
        required: false
        type: integer
        in: query
        default: 10
      - name: skip
        required: false
        type: integer
        in: query
        default: 0
    definitions:
      ProjectList:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/ProjectList"
    """
    try:
        query_raw = {}
        target_name = request.args.get("name", "").strip()
        target_meta = target_status.get(target_name, None)
        if target_meta is None:
            return ErrorMessage.INVALID_TARGET_NAME
        query_raw["name"] = target_name

        project_name = request.args.get("project_name")
        if project_name:
            query_raw["project.name"] = {"$regex": project_name.strip()}

        start = request.args.get("start")
        if start and "Infinity" not in start:
            query_raw.setdefault("value", {})["$gte"] = float(start)
        end = request.args.get("end")
        if end and "Infinity" not in end:
            query_raw.setdefault("value", {})["$lt"] = float(end)

        target_year = request.args.get("target_year")
        if target_year:
            query_raw["year"] = int(target_year)
        company = request.args.get("company")
        if company:
            query_raw["project.company"] = {"$regex": company.strip()}
        classification = request.args.get("classification")
        if classification:
            query_raw["project.classification"] = classification.strip()
        operation_year = request.args.get("operation_year")
        if operation_year:
            query_raw["project.operation_year"] = int(operation_year)
        voltage_level = request.args.get("voltage_level")
        if voltage_level:
            query_raw["project.voltage_level"] = int(voltage_level)
        status = request.args.get("status")
        contrast_filed = request.args.get("contrast_filed", "classification")
        if contrast_filed not in ContrastFiledParam.values:
            return ErrorMessage.INVALID_CONTRAST_FILED
        if status:
            query_raw["status.message"] = status.strip()

        limit = request.args.get("limit", 10)
        skip = request.args.get("skip", 0)
        limit = int(limit)
        skip = int(skip)
    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, e, 400)

    detail_columns = [
        {
            "cn_name": "项目名称",
            "en_name": "project_name",
            "type": "string",
            "order": 1
        },
        {
            "cn_name": "电压等级(KV)",
            "en_name": ContrastFiledParam.VoltageLevel,
            "type": "select",
            "value": PROJECT_VOLTAGE_LEVEL,
            "order": 3
        },
        {
            "cn_name": "工程分类",
            "en_name": ContrastFiledParam.Classification,
            "type": "select",
            "value": PROJECT_CLASSIFICATION,
            "order": 4
        },
        {
            "cn_name": "实际投运年",
            "en_name": ContrastFiledParam.OperationYear,
            "type": "year",
            "order": 5
        },
        {
            "cn_name": "所属公司",
            "en_name": ContrastFiledParam.Company,
            "type": "string",
            "order": 6
        },
        {
            "cn_name": "指标值",
            "en_name": "value",
            "order": 8
        },
    ]

    if target_meta.get("component"):
        detail_columns.append({
            "cn_name": "线路/主变",
            "en_name": "component_name",
            "order": 2
        })
    if target_meta.get("status"):
        detail_columns.append({
            "cn_name": "指标状态",
            "en_name": "status_msg",
            "type": "select",
            "value": [item.message for item in target_meta.get("status")],
            "order": 9
        })
    if target_meta.get("show_type") == 2:
        detail_columns.append({
            "cn_name": "同%s均值" % ContrastFiledParam.get_cn(contrast_filed),
            "en_name": "average",
            "order": 10
        })
    if target_meta.get("continuous"):
        detail_columns.append({
            "cn_name": "指标时间",
            "en_name": "target_year",
            "type": "year",
            "order": 7
        })
        if not query_raw.get("year"):
            query_raw["year"] = TargetManager.get_max_target_year(target_name)

    total, data_source = TargetViewsManager.get_project_list_view(query_raw, contrast_filed, limit=limit, skip=skip)
    result = {
        "total": total,
        "columns": sorted(detail_columns, key=lambda i: i["order"]),
        "data_source": data_source
    }
    return ReturnMessage.build_success(result)


@target.route('/aggregate/<contrast_filed>', methods=['GET'])
@error_handler
@login_required
def aggregate(contrast_filed):
    """ 获取指标聚合结果
        show_type1:  a.支撑文件完整度（%） b.继电保护和安稳装置误动、拒动次数（次） c.变压器强迫停运时间（小时）
        show_type2: 线路损耗率（%）
        show_type3: 母线电压合格率（%）
    ---
    tags:
    - "target"
    produces:
      - "application/json"
    parameters:
      - name: name
        required: true
        type: string
        in: query
      - name: contrast_filed
        required: true
        type: string
        in: path
        enum:
          - classification
          - voltage_level
          - company
          - operation_year
    definitions:
      AggregateResponse:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            $ref: "#/definitions/Aggregate"
      Aggregate:
        type: object
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/AggregateResponse"
    """
    target_name = request.args.get("name")
    target_meta = target_status.get(target_name, None)
    if target_meta is None:
        return ErrorMessage.INVALID_TARGET_NAME
    if contrast_filed not in ContrastFiledParam.values:
        return ErrorMessage.INVALID_CONTRAST_FILED

    is_continuous_value = target_meta.get("continuous", False)
    result = TargetAggregateManager.aggregate(target_name, contrast_filed, is_continuous_value)
    return ReturnMessage.build_success(result)


@target.route('/statistics', methods=['GET'])
@error_handler
@login_required
def statistics():
    """ 指标部分值统计
    ---
    tags:
    - "target"
    produces:
      - "application/json"
    parameters:
      - name: name
        required: true
        type: string
        in: query
      - name: contrast_filed
        required: false
        type: string
        in: query
        enum:
          - classification
          - voltage_level
          - company
          - operation_year
      - name: contrast_value
        required: false
        type: string
        in: query
      - name: target_year
        required: false
        type: integer
        in: query
    definitions:
      Item:
        type: object
      StatisticsResponse:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: array
            items:
              $ref: "#/definitions/Item"
      Aggregate:
        type: object
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/StatisticsResponse"
    """
    query_raw = {}
    target_name = request.args.get("name")
    if target_name:
        query_raw["name"] = target_name.strip()
    target_meta = target_status.get(target_name, None)
    if target_meta is None:
        return ErrorMessage.INVALID_TARGET_NAME
    boundary = target_meta.get("boundary")
    if boundary is None:
        return ErrorMessage.INVALID_TARGET_NAME_STATISTICS

    contrast_filed = request.args.get("contrast_filed")
    contrast_value = request.args.get("contrast_value")
    if contrast_filed and contrast_value:
        if contrast_filed not in ContrastFiledParam.values:
            return ErrorMessage.INVALID_CONTRAST_FILED
        query_raw["project." + contrast_filed] = contrast_value

    target_year = request.args.get("target_year")
    if target_year:
        query_raw["year"] = int(target_year)

    value_list = TargetAggregateManager.get_statistics(query_raw)
    result = TargetViewsManager.get_statistics_view(boundary, value_list)

    return ReturnMessage.build_success(result)
