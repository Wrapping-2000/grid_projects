from collections import OrderedDict
from app.project_evaluation.utils.target_utils import *
from app.project_evaluation.manager import TargetManager
from app.project_evaluation.utils.task_pool import TaskPool


class BaseProjectCategory:
    value = OrderedDict()

    @classmethod
    def contains(cls, name, primary_index=None):
        if primary_index:
            return name in cls.value.get(primary_index, [])

        for primary_index, name_list in cls.value.items():
            if name in name_list:
                return True

        return False

    @classmethod
    def get_index_name(cls, name):
        for primary_index, name_list in cls.value.items():
            if name in name_list:
                return primary_index


class ProjectConstructionProcess(BaseProjectCategory):
    value = OrderedDict({
        # "前期决策": [
        #     "规划一致率（%）",
        #     "可研一致率（%）"
        # ],
        "建设准备": [
            # "初设一致率（%）",
            # "施设一致率（%）",
            # "招标覆盖率（%）",
            # "合同范本应用率（%）",
            # "开工条件落实率（%）",
            PROJECT_DEVIATION_RATE,
            DOCUMENT_COMPLETE_RATE
        ],
        "施工管理": [
            CAPACITANCE_PER_UNIT,
            WIRE_LENGTH_PER_UNIT,
            CONSTRUCTION_COST,
            WIRE_LENGTH_CONSTRUCTION_PER_UNIT,
            DESIGN_CHANGE_RATE,
            SAVING_RATE,
            SAVING_RATE_FINAL,
            START_TIME_DIFF_RATE,
            PRODUCE_TIME_DIFF_RATE,
            POWER_SUPPLY_TIME_DIFF,
            ELECTRIC_RAILWAY_TIME_DIFF
        ]
    })


class ProjectOperationEffect(BaseProjectCategory):
    value = OrderedDict({
        "transformer_efficiency": [
            TRANSFORMER_LOAD_RATE,
            TRANSFORMER_AVERAGE_LOAD_RATE,
            MAXIMUM_LOAD_POWER_FACTOR,
            INCREASE_POWER_SUPPLY_PER_UNIT
        ],
        "line_efficiency": [
            MAXIMUM_LOAD_RATE_LINE,
            AVERAGE_LOAD_RATE_LINE,
            MAXIMUM_LOAD_POWER_FACTOR_LINE,
            INCREASE_POWER_SUPPLY_PER_YEAR
        ],
        "running_loss": [
            LOSS_RATE_OF_MAIN_TRANSFORMER,
            LOSS_RATE_OF_LINE
        ],
        "safety_benefit": [
            FORCED_SHUTDOWN_OF_SUBSTATION,
            FORCED_SHUTDOWN_OF_SUBSTATION_HOUR,
            FORCED_LINE_OUTAGE,
            FORCED_LINE_OUTAGE_HOUR,
            QUALIFIED_RATE_OF_BUS_VOLTAGE,
            TIMES_OF_OPERATION_MISTAKE_DEVICE,
            ASSESSMENT_TIMES_AFFECTING_POWER_QUALITY
        ],
        "electricity_benefit": [
            POWER_SUPPLY_OF_PROJECT,
            UNIT_CAPACITY,
            TRANSMISSION_AND_DISTRIBUTION_ASSETS_OF_UNIT_NEWLY
        ]
    })

    name = [
        {
            "en": "transformer_efficiency",
            "cn": "主变利用效率"
        },
        {
            "cn": "线路利用效率",
            "en": "line_efficiency"
        },
        {
            "en": "running_loss",
            "cn": "运行损耗"
        },
        {
            "cn": "安全效益",
            "en": "safety_benefit"
        },
        {
            "cn": "电量效益",
            "en": "electricity_benefit"
        }
    ]


class ProjectFinancialBenefits(BaseProjectCategory):
    value = OrderedDict({
        "盈利能力": [
            INTERNAL_RATE_TOTAL_INVESTMENT,
            INTERNAL_RATE_TOTAL_CAPITAL,
            PAYBACK_PERIOD
        ],
        "偿债能力": [
            DEBT_SERVICE_COVERAGE_RATIO,
            INTEREST_PROVISION_RATE
        ],
        "风险控制": [
            COMPLETION_RATE_OF_BREAKEVEN_ELECTRICITY,
            COMPLETION_RATE_OF_FEASIBILITY_ELECTRICITY,
            COMPLETION_RATE_OF_FEASIBILITY_STUDY_BENEFIT
        ],
        "输配电成本": [
            POWER_TRANSMISSION_DISTRIBUTION_COST
        ],
        "全周期投资输配电量": [
            UNIT_INVESTMENT_POWER_TRANSMISSION_DISTRIBUTION
        ]
    })


class ProjectTargets:

    @staticmethod
    def get_construction_process_view(wbs_code, project_filed="classification"):
        target_list = TargetManager.get_targets(wbs_code=wbs_code)

        return ProjectTargets.hierarchize_target_list(ProjectConstructionProcess,
                                                      target_list, project_filed)

    @staticmethod
    def get_operation_effect_view(wbs_code, primary_index, project_filed="classification", year=None):
        if not year:
            year = TargetManager.get_max_project_target_year(wbs_code)
        target_list = TargetManager.get_targets(wbs_code=wbs_code, year=year)

        result = ProjectTargets.hierarchize_target_list(ProjectOperationEffect,
                                                        target_list, project_filed, primary_index=primary_index)
        result = result.get(primary_index, [])
        view = {}
        for item in result:
            name = item["name"]
            if "component_name" in item:
                view.setdefault(name, []).append(item)
            else:
                view[name] = item

        return view

    @staticmethod
    def get_financial_benefits_view(wbs_code, project_filed="classification", year=None):
        if not year:
            year = TargetManager.get_max_project_target_year(wbs_code)
        target_list = TargetManager.get_targets(wbs_code=wbs_code, year=year)

        return ProjectTargets.hierarchize_target_list(
            ProjectFinancialBenefits, target_list, project_filed)

    @staticmethod
    def hierarchize_target_list(hierarchy, target_list, project_filed, primary_index=None):
        filtered_target = []
        for target in target_list:
            if hierarchy.contains(target.name, primary_index):
                filtered_target.append(target)

        result = OrderedDict()
        TaskPool.wait_evaluation_target_job_finished(filtered_target, project_filed)
        for target in filtered_target:
            primary_index = hierarchy.get_index_name(target.name)
            target_view = {
                "name": target.name,
                "data_raw": target.data_raw,
                "value": target.value,
                "average": target.average,
                "status": target.status.get("color", None) if target.status else None,
                "status_msg": target.status.get("message", None) if target.status else None,
                "rule": target_status.get(target.name, {}).get("rule", None)
            }
            if target.year is not None:
                target_view["year"] = target.year
            if target.component_name is not None:
                target_view["component_name"] = target.component_name
            if target.value_list:
                target_view["value_list"] = target.value_list
            if target.average_list:
                target_view["average_list"] = target.average_list
            result.setdefault(primary_index, []).append(target_view)

        return result


if __name__ == "__main__":
    print(ProjectOperationEffect.contains(TRANSFORMER_LOAD_RATE, "transformer_efficiency"))
