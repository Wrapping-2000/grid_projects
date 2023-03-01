from io import BytesIO

from flask import request
from flask_login import login_required

from . import project
from .project_targets import ProjectTargets, ProjectOperationEffect
from app.utils.return_code import ReturnMessage, ErrorMessage, error_handler
from app.project_evaluation.manager import ProjectManager
from app.project_evaluation.manager import ProjectComponentManager
from app.project_evaluation.manager import ProjectDetailManager
from app.project_evaluation.manager import TargetManager
from app.project_evaluation.utils import ContrastFiledParam, PROJECT_CLASSIFICATION, PROJECT_VOLTAGE_LEVEL
from app.project_evaluation.utils.data_parser import DataParser
from app.project_evaluation.utils.task_pool import TaskPool


@project.route('/aggregation_filed', methods=['GET'])
@error_handler
@login_required
def aggregation():
    """ 获取项目属性voltage_level、classification
    ---
    tags:
    - "project"
    produces:
      - "application/json"
    definitions:
      AggregationResponse:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            $ref: "#/definitions/Aggregation"
      Aggregation:
        type: object
        properties:
          voltage_level:
            type: array
            items:
              type: integer
          classification:
            type: array
            items:
              type: string
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/AggregationResponse"
    """
    result = {
        "voltage_level": PROJECT_VOLTAGE_LEVEL,
        "classification": PROJECT_CLASSIFICATION
    }
    return ReturnMessage.build_success(result)


@project.route('/list', methods=['GET'])
@error_handler
@login_required
def project_list():
    """获取项目类表
    ---
    tags:
    - "project"
    produces:
      - "application/json"
    parameters:
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
      - name: project_name
        required: false
        type: string
        in: query
      - name: wbs_code
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
    definitions:
      ListResponse:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: object
            properties:
              projects:
                $ref: "#/definitions/Projects"
              total:
                type: integer
      Projects:
        type: object
        properties:
          projects:
            type: array
            items:
              $ref: "#/definitions/Project"
      Project:
        type: object
        properties:
          name:
            type: string
          wbs_code:
            type: string
          voltage_level:
            type: integer
          classification:
            type: string
          operation_year:
            type: integer
          company:
            type: string
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/ListResponse"
    """

    try:
        limit = request.args.get("limit", 10)
        skip = request.args.get("skip", 0)
        limit = int(limit)
        skip = int(skip)

        query_raw = {}
        project_name = request.args.get("project_name")
        if project_name:
            query_raw["name"] = {"$regex": project_name.strip()}
        wbs_code = request.args.get("wbs_code")
        if wbs_code:
            query_raw["wbs_code"] = wbs_code.strip()
        classification = request.args.get("classification")
        if classification:
            query_raw["classification"] = classification.strip()
        company = request.args.get("company")
        if company:
            query_raw["company"] = {"$regex": company.strip()}
        operation_year = request.args.get("operation_year")
        if operation_year:
            query_raw["operation_year"] = int(operation_year)
        voltage_level = request.args.get("voltage_level")
        if voltage_level:
            query_raw["voltage_level"] = int(voltage_level)

    except Exception as e:
        return ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, e, 400)

    result = {
        "total": ProjectManager.get_project_count(query_raw),
        "projects": [ProjectManager.to_list_item(p) for p in
                     ProjectManager.get_project_list(query_raw, limit=limit, skip=skip)]
    }

    return ReturnMessage.build_success(result)


@project.route('/<wbs_code>', methods=['DELETE'])
@error_handler
@login_required
def delete_project(wbs_code):
    """ 删除项目及评价信息
    ---
    tags:
    - "project"
    produces:
      - "application/json"
    parameters:
      - name: wbs_code
        required: true
        type: string
        in: path
    definitions:
      DeleteResponse:
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
          $ref: "#/definitions/DeleteResponse"
    """
    if not wbs_code:
        return ErrorMessage.INVALID_WPS_CODE

    ProjectManager.delete_project(wbs_code)
    ProjectComponentManager.delete_project_component(wbs_code)
    ProjectDetailManager.delete_project_detail(wbs_code)
    TargetManager.delete_target(wbs_code)

    return ReturnMessage.SUCCESS


@project.route('/<wbs_code>', methods=['GET'])
@error_handler
@login_required
def get_project_detail(wbs_code):
    """ 获取项目详细信息
    ---
    tags:
    - "project"
    produces:
      - "application/json"
    parameters:
      - name: wbs_code
        required: true
        type: string
        in: path
    definitions:
      DetailResponse:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: object
            properties:
              data_source:
                type: object
              columns:
                type: object
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/DetailResponse"
    """
    if not wbs_code:
        return ErrorMessage.INVALID_WPS_CODE

    p = ProjectManager.get_project(wbs_code)
    if not p:
        return ErrorMessage.PROJECT_NOT_EXIST
    result = {
        "columns": ProjectManager.detail_columns,
        "data_source": ProjectManager.to_project_detail(p) if p else {}
    }

    return ReturnMessage.build_success(result)


@project.route('/target/operation_effect/primary_index', methods=['GET'])
@error_handler
@login_required
def get_operation_effect_primary_index():
    """ 获取项目运行效果指标类型
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    definitions:
      OperationEffectPrimaryIndex:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: array
            items:
              type: integer
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/OperationEffectPrimaryIndex"
    """
    return ReturnMessage.build_success(ProjectOperationEffect.name)


@project.route('/target/<wbs_code>/construction_process/<contrast_filed>', methods=['GET'])
@error_handler
@login_required
def get_construction_process(wbs_code, contrast_filed):
    """ 获取项目建设过程信息
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: wbs_code
        required: true
        type: string
        in: path
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
      ConstructionProcess:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: object
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/ConstructionProcess"
    """
    if not wbs_code:
        return ErrorMessage.INVALID_WPS_CODE
    if contrast_filed not in ContrastFiledParam.values:
        return ErrorMessage.INVALID_CONTRAST_FILED

    result = ProjectTargets.get_construction_process_view(wbs_code, contrast_filed)
    return ReturnMessage.build_success(result)


@project.route('/target/<wbs_code>/operation_effect/<primary_index>/<contrast_filed>', methods=['GET'])
@error_handler
@login_required
def get_operation_effect(wbs_code, primary_index, contrast_filed):
    """ 获取项目运行效果信息
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: wbs_code
        required: true
        type: string
        in: path
      - name: primary_index
        required: true
        type: string
        in: path
        enum:
          - transformer_efficiency
          - line_efficiency
          - running_loss
          - safety_benefit
          - electricity_benefit
      - name: contrast_filed
        required: true
        type: string
        in: path
        enum:
          - classification
          - company
          - operation_year
          - voltage_level
      - name: year
        required: false
        type: integer
        in: query
    definitions:
      OperationEffect:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: object
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/OperationEffect"
    """
    if not wbs_code:
        return ErrorMessage.INVALID_WPS_CODE
    if contrast_filed not in ContrastFiledParam.values:
        return ErrorMessage.INVALID_CONTRAST_FILED
    if primary_index not in ProjectOperationEffect.value.keys():
        return ErrorMessage.INVALID_PRIMARY_INDEX
    year = request.args.get("year")
    if year and not year.isdecimal():
        return ErrorMessage.INVALID_YEAR_PARAM

    result = ProjectTargets.get_operation_effect_view(wbs_code, primary_index, contrast_filed, year)

    return ReturnMessage.build_success(result)


@project.route('/target/<wbs_code>/financial_benefits/<contrast_filed>', methods=['GET'])
@error_handler
@login_required
def get_financial_benefits(wbs_code, contrast_filed):
    """ 项目投资管控
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: wbs_code
        required: true
        type: string
        in: path
      - name: contrast_filed
        required: true
        type: string
        in: path
        enum:
          - classification
          - voltage_level
          - company
          - operation_year
      - name: year
        required: false
        type: integer
        in: query
    definitions:
      OperationEffect:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
          data:
            type: object
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/OperationEffect"
    """
    if not wbs_code:
        return ErrorMessage.INVALID_WPS_CODE
    if contrast_filed not in ContrastFiledParam.values:
        return ErrorMessage.INVALID_CONTRAST_FILED
    year = request.args.get("year")
    if year and not year.isdecimal():
        return ErrorMessage.INVALID_YEAR_PARAM

    result = ProjectTargets.get_financial_benefits_view(wbs_code, contrast_filed, year)
    return ReturnMessage.build_success(result)


@project.route('/history_project', methods=['POST'])
@error_handler
@login_required
def upload_history_project():
    """ 上传历史项目
        历史项目模板地址:template/更新历史项目模板.xlsx
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: "file"
        in: "formData"
        description: "file to upload"
        required: true
        type: "file"
    definitions:
      uploadHistoryProject:
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
          $ref: "#/definitions/uploadHistoryProject"
    """
    file = request.files['file']
    data_parser = DataParser()
    bytes_file = BytesIO(file.read())

    data_parser.check_old_project_format(bytes_file)
    wbs_code_list = DataParser().parse_old_project(bytes_file)
    for wbs_code in wbs_code_list:
        TaskPool.add_calculation_and_evaluation_job(wbs_code)
    return ReturnMessage.SUCCESS


@project.route('/new_project', methods=['POST'])
@error_handler
@login_required
def upload_new_project():
    """ 上传新项目
        新项目模板地址:template/新增项目模板.xlsx
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: "file"
        in: "formData"
        description: "file to upload"
        required: true
        type: "file"
    definitions:
      uploadNewProject:
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
          $ref: "#/definitions/uploadNewProject"
    """
    file = request.files['file']

    data_parser = DataParser()  # TODO 例单模式还有修改一下其他staticmethod方法
    bytes_file = BytesIO(file.read())

    data_parser.check_new_project_format(bytes_file)
    wbs_code_list = data_parser.parse_new_project(bytes_file)
    for wbs_code in wbs_code_list:
        TaskPool.add_calculation_and_evaluation_job(wbs_code)
    return ReturnMessage.SUCCESS


@project.route('/<wbs_code>', methods=['PUT'])
@error_handler
def update_project(wbs_code):
    """ 更新项目详细信息
    ---
    tags:
    - "project"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: wbs_code
        required: true
        type: string
        in: path
      - name: data
        required: true
        in: body
        schema:
          $ref: "#/definitions/UpdateData"
    definitions:
      UpdateData:
        type: object
      UpdateResponse:
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
          $ref: "#/definitions/UpdateResponse"
    """
    if not wbs_code:
        return ErrorMessage.INVALID_WPS_CODE
    if "wbs_code" in request.json:
        return ErrorMessage.INVALID_UPDATE_PARAM_WPS_CODE

    p = ProjectManager.get_project(wbs_code)
    if not p:
        return ErrorMessage.PROJECT_NOT_EXIST

    for attr in request.json:
        if attr not in ProjectManager.detail_columns:
            continue
        p[attr] = request.json[attr]
    p.generate_company()
    p.validate()
    p.save()

    return ReturnMessage.SUCCESS
