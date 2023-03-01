from app.project_evaluation.manager.models import Project


class ProjectManager:

    @staticmethod
    def add_project(name, wbs_code, voltage_level, classification, operation_year, plan_year,
                    company_province, company_city, company_county, energy_type, channel_type,
                    budget, capacitance, wire_length, transmission_capacity):
        p = ProjectManager.get_project(wbs_code)
        if not p:
            p = Project(wbs_code=wbs_code.strip())
        params = {
            "name": "".join(name.split()),
            "voltage_level": int(voltage_level),
            "classification": classification.strip(),
            "operation_year": int(operation_year),
            "plan_year": int(plan_year),
            "company_province": company_province.strip() if company_province else None,
            "company_city": company_city.strip() if company_city else None,
            "company_county": company_county.strip() if company_county else None,
            "energy_type": energy_type.strip() if energy_type else None,
            "channel_type": channel_type.strip() if channel_type else None,
            "budget": float(budget) if budget else None,
            "capacitance": float(capacitance) if capacitance else None,
            "wire_length": float(wire_length) if wire_length else None,
            "transmission_capacity": float(transmission_capacity) if transmission_capacity else None
        }
        for name, value in params.items():
            p[name] = value
        p.generate_company()
        p.validate()
        p.save()

    @staticmethod
    def get_project(wbs_code):
        return Project.objects(wbs_code=wbs_code).first()

    @staticmethod
    def delete_project(wbs_code):
        Project.objects(wbs_code=wbs_code).delete()

    @staticmethod
    def get_project_list_all():
        return Project.objects()

    @staticmethod
    def get_project_list(query_raw=None, limit=10, skip=0):
        if query_raw:
            return Project.objects(__raw__=query_raw)[skip:skip+limit].order_by("-operation_year")

        return Project.objects()[skip:skip+limit].order_by("-operation_year")

    @staticmethod
    def get_project_count(query_raw=None):
        if query_raw:
            return Project.objects(__raw__=query_raw).count()

        return Project.objects().count()

    @staticmethod
    def get_distinct_value(name):
        return Project.objects().distinct(name)

    @staticmethod
    def get_voltage_level_list():
        return ProjectManager.get_distinct_value("voltage_level")

    @staticmethod
    def get_operation_year_list():
        return ProjectManager.get_distinct_value("operation_year")

    @staticmethod
    def get_classification_list():
        return ProjectManager.get_distinct_value("classification")

    @staticmethod
    def to_project_detail(project):
        result = {
            "project_name": project.name,
            "wbs_code": project.wbs_code,
            "voltage_level": project.voltage_level,
            "classification": project.classification,
            "operation_year": project.operation_year,
            "plan_year": project.plan_year,
            "company_province": project.company_province,
            "company_city": project.company_city,
            "company_county": project.company_county,
            "energy_type": project.energy_type,
            "channel_type": project.channel_type,
            "budget": project.budget,
            "capacitance": project.capacitance,
            "wire_length": project.wire_length,
            "transmission_capacity": project.transmission_capacity
        }

        return result

    @staticmethod
    def to_list_item(project):
        result = {
            "project_name": project.name,
            "wbs_code": project.wbs_code,
            "voltage_level": project.voltage_level,
            "classification": project.classification,
            "operation_year": project.operation_year,
            "company": project.company
        }

        return result

    detail_columns = {
        "project_name": "项目名称",
        "wbs_code": "WBS编码",
        "voltage_level": "电压等级（KV）",
        "classification": "工程分类",
        "operation_year": "实际投运年",
        "plan_year": "规划投运年",
        "company_province": "所属省公司",
        "company_city": "所属市公司",
        "company_county": "所属县公司",
        "energy_type": "“保障电源送出”和“服务新能源”项目电源类型",
        "channel_type": "“加强输电通道类”项目的输电通道类型",
        "budget": "决算投资（含税）（万元）",
        "capacitance": "新增变电容量（MVA）",
        "wire_length": "新增线路长度（公里）",
        "transmission_capacity": "新增输电能力（MW）"
    }
