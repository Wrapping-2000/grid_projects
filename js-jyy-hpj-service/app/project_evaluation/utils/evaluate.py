from datetime import datetime

from app.project_evaluation.manager import ProjectManager
from app.project_evaluation.manager import TargetAggregateManager
from app.project_evaluation.manager import TargetManager
from app.project_evaluation.manager.models import Target
from app.project_evaluation.utils import keep_2f
from app.project_evaluation.utils.target_utils import *


class Evaluate:

    def __init__(self, wbs_code):
        self.wbs_code = wbs_code

    @staticmethod
    def evaluate_target_aggregate(target_aggregate, project_filed):
        target = Target()
        target.year = target_aggregate.get("year")
        target.value = target_aggregate.get("value")
        target.component_name = target_aggregate.get("component_name")
        target.wbs_code = target_aggregate.get("wbs_code")
        target.name = target_aggregate.get("name")

        Evaluate.evaluate_target(target, project_filed)

        target_aggregate["status"] = target.status
        target_aggregate["average"] = target.average

    @staticmethod
    def evaluate_target(target, project_filed="classification"):
        target_name = target.name
        value = target.value
        target = Evaluate.get_average(target, project_filed)

        if target_name in [PROJECT_DEVIATION_RATE,
                           FORCED_SHUTDOWN_OF_SUBSTATION,
                           FORCED_SHUTDOWN_OF_SUBSTATION_HOUR,
                           FORCED_LINE_OUTAGE,
                           FORCED_LINE_OUTAGE_HOUR,
                           TIMES_OF_OPERATION_MISTAKE_DEVICE,
                           ASSESSMENT_TIMES_AFFECTING_POWER_QUALITY]:
            target.set_status(NORMAL_STATUS) if value == 0 else target.set_status(ABNORMAL_STATUS)
        elif target_name in [DESIGN_CHANGE_RATE]:
            target.set_status(DESIGN_NOT_CHANGE_STATUS) if value == 0 else target.set_status(DESIGN_CHANGE_STATUS)
        elif target_name in [QUALIFIED_RATE_OF_BUS_VOLTAGE]:
            if value >= 99.99:
                target.set_status(GOOD_VOLTAGE)
            elif 99.95 < value < 99.99:
                target.status(QUALIFIED_VOLTAGE)
            else:
                target.set_status(LOW_VOLTAGE)
        elif target_name in [POWER_SUPPLY_OF_PROJECT]:
            previous_value = target.value
            for item in target.value_list:
                if item["year"] == target.year - 1:
                    previous_value = item["value"]
            if previous_value == target.value:
                target.set_status(ELECTRICITY_UNCHANGED)
            elif target.value < previous_value:
                target.set_status(ELECTRICITY_DECLINE)
            else:
                target.set_status(ELECTRICITY_RAISE)

        elif target_name in [INTERNAL_RATE_TOTAL_INVESTMENT]:
            target.set_status(ABNORMAL_STATUS) if value < 7 else target.set_status(NORMAL_STATUS)
        elif target_name in [INTERNAL_RATE_TOTAL_CAPITAL]:
            target.set_status(ABNORMAL_STATUS) if value < 7 else target.set_status(NORMAL_STATUS)
        elif target_name in [PAYBACK_PERIOD]:
            project = ProjectManager.get_project(target.wbs_code)
            current_year = datetime.now().year
            if target.value > (current_year - project.operation_year):
                target.set_status(CAPITAL_NOT_RECOVERY)
            else:
                target.set_status(CAPITAL_RECOVERY)
        elif target_name in [DOCUMENT_COMPLETE_RATE]:
            if value == 100:
                target.set_status(NORMAL_STATUS)
            else:
                target.set_status(ABNORMAL_STATUS)
        elif target_name in [DEBT_SERVICE_COVERAGE_RATIO]:
            target.set_status(ABNORMAL_STATUS) if value > 1.3 else target.set_status(NORMAL_STATUS)
        elif target_name in [INTEREST_PROVISION_RATE]:
            target.set_status(ABNORMAL_STATUS) if value > 2 else target.set_status(NORMAL_STATUS)
        elif target_name in [COMPLETION_RATE_OF_BREAKEVEN_ELECTRICITY]:
            if value < 100:
                target.set_status(ELECTRICITY_UNBALANCE)
            else:
                target.set_status(ELECTRICITY_BALANCE)
        elif target_name in [COMPLETION_RATE_OF_FEASIBILITY_ELECTRICITY]:
            if value < 100:
                target.set_status(NOT_REACH_FEASIBILITY_ELECTRICITY)
            else:
                target.set_status(REACH_FEASIBILITY_ELECTRICITY)
        elif target_name in [SAVING_RATE, SAVING_RATE_FINAL]:
            if value >= 20 or value < 0:
                target.set_status(ABNORMAL_STATUS)
            else:
                target.set_status(NORMAL_STATUS)
        elif target_name in [POWER_SUPPLY_TIME_DIFF, ELECTRIC_RAILWAY_TIME_DIFF]:
            if value < 0:
                target.set_status(PROJECT_PRE_TIME_STATUS)
            elif value == 0:
                target.set_status(PROJECT_ON_TIME_STATUS)
            else:
                target.set_status(PROJECT_POST_TIME_STATUS)

        elif target_name in [CAPACITANCE_PER_UNIT,
                             WIRE_LENGTH_PER_UNIT,
                             CONSTRUCTION_COST,
                             WIRE_LENGTH_CONSTRUCTION_PER_UNIT,
                             LOSS_RATE_OF_MAIN_TRANSFORMER,
                             LOSS_RATE_OF_LINE]:
            if value > target.average:
                target.set_status(ABNORMAL_STATUS)
            else:
                target.set_status(NORMAL_STATUS)
        elif target_name in [TRANSFORMER_LOAD_RATE]:
            project = ProjectManager.get_project(target.wbs_code)
            run_year = datetime.now().year - project.operation_year
            if run_year < 3:
                pass
            elif run_year < 5:
                target.set_status(REASONABLE_CAPACITY_OF_MAIN_TRANSFORMER) \
                    if value >= 25 else target.set_status(UNREASONABLE_CAPACITY_OF_MAIN_TRANSFORMER)
            else:
                target.set_status(REASONABLE_CAPACITY_OF_MAIN_TRANSFORMER) \
                    if value >= 40 else target.set_status(UNREASONABLE_CAPACITY_OF_MAIN_TRANSFORMER)
        elif target_name in [TRANSFORMER_AVERAGE_LOAD_RATE]:
            project = ProjectManager.get_project(target.wbs_code)
            run_year = datetime.now().year - project.operation_year
            if run_year < 3:
                pass
            else:
                if value >= 50:
                    target.set_status(HEAVY_LOAD_STATUS)
                elif value <= 25:
                    target.set_status(LIGHT_LOAD_STATUS)
                else:
                    target.set_status(REASONABLE_STATUS)
        elif target_name in [MAXIMUM_LOAD_POWER_FACTOR, MAXIMUM_LOAD_POWER_FACTOR_LINE]:
            target.set_status(ABNORMAL_STATUS) if value < 0.95 else target.set_status(NORMAL_STATUS)
        elif target_name in [MAXIMUM_LOAD_RATE_LINE, AVERAGE_LOAD_RATE_LINE]:
            if value >= 80:
                target.set_status(HEAVY_LOAD_STATUS)
            elif value <= 20:
                target.set_status(LIGHT_LOAD_STATUS)
            else:
                target.set_status(NORMAL_STATUS)

        return target

    @staticmethod
    def get_average(target, project_filed):
        year = target.year
        component_name = target.component_name
        target_name = target.name
        wbs_code = target.wbs_code
        project = ProjectManager.get_project(wbs_code)
        project_filed = "project." + project_filed
        project_value = eval(project_filed)

        value_list = []
        average_list = []
        if not year:
            average_value = TargetAggregateManager.get_target_average_value(target_name, project_filed, project_value)
        else:
            value_list = TargetAggregateManager.get_target_component_year_value(wbs_code, target_name, component_name)
            average_list = TargetAggregateManager.get_target_year_average_value(
                target_name, project_filed, project_value)
            for item in average_list:
                item["value"] = keep_2f(item["value"])

            average_value = [item["value"] for item in average_list if item["year"] == year][0]

        target.average = keep_2f(average_value)
        target.value_list = value_list
        target.average_list = average_list

        return target

    def do_project_target_evaluate(self):
        for target in TargetManager.get_targets(self.wbs_code):
            if target_status.get(target.name, {}).get("show_type") == 1:
                Evaluate.evaluate_target(target)
                TargetManager.add_target(target)
