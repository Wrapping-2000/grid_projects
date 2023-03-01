from app.project_evaluation.manager import ProjectManager
from app.project_evaluation.manager import ProjectComponentManager
from app.project_evaluation.manager import TargetManager
from app.project_evaluation.manager.models import Target
from app.project_evaluation.utils.base_target_calculation import BaseTargetCalculation
from app.project_evaluation.utils.target_utils import *
from app.project_evaluation.utils import *


class TargetCalculation(BaseTargetCalculation):
    def cal_project_deviation_rate(self):
        data_raw = {}
        data_raw_cal = {}

        target = Target(
            name=PROJECT_DEVIATION_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        for name_raw in ["可研批复时间", "初设批复时间",
                         "开工时间/计划", "开工时间/实际",
                         "竣工时间/计划", "竣工时间/实际",
                         "投产时间/计划", "投产时间/实际",
                         "结算完成时间", "竣工决算完成时间"]:
            data_raw[name_raw] = format_datetime(self.project_detail.get(name_raw))
            data_raw_cal[name_raw] = self.project_detail.get(name_raw)

        if has_all_datetime(data_raw_cal):
            error_count = 0
            if data_raw["可研批复时间"] < data_raw["初设批复时间"]:
                error_count += 1
            if data_raw["开工时间/计划"] < data_raw["开工时间/实际"]:
                error_count += 1
            if data_raw["竣工时间/计划"] < data_raw["竣工时间/实际"]:
                error_count += 1
            if data_raw["投产时间/计划"] < data_raw["投产时间/实际"]:
                error_count += 1
            if data_raw["结算完成时间"] < data_raw["竣工决算完成时间"]:
                error_count += 1

            target.value = keep_percent(error_count, 8)
            yield target

    def cal_document_complete_rate(self):
        data_raw = {}

        target = Target(
            name=DOCUMENT_COMPLETE_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        for name_raw in ["支持文件信息/可研批复名称", "支持文件信息/核准文件名称",
                         "支持文件信息/初设批复名称", "支持文件信息/结算批复文件名称",
                         "支持文件信息/竣工决算报告名称"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        file_count = 0
        for item in data_raw:
            if data_raw[item]:
                file_count += 1

        target.value = keep_percent(file_count, 5)
        yield target

    def cal_capacitance_per_unit(self):
        data_raw = {}
        target = Target(
            name=CAPACITANCE_PER_UNIT,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        project = ProjectManager.get_project(self.project_detail["wbs_code"])
        data_raw["新增变电容量（MVA）"] = project.capacitance
        data_raw["变电工程/竣工决算（含税）/静态投资（万元）/总额"] = self.project_detail.get(
            "变电工程/竣工决算（含税）/静态投资（万元）/总额")
        target.value = do_division(data_raw["变电工程/竣工决算（含税）/静态投资（万元）/总额"],
                                   data_raw["新增变电容量（MVA）"])

        yield target

    def cal_wire_length_per_unit(self):
        data_raw = {}
        target = Target(
            name=WIRE_LENGTH_PER_UNIT,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        project = ProjectManager.get_project(self.project_detail["wbs_code"])
        data_raw["新增线路长度（公里）"] = project.wire_length
        data_raw["变电工程/竣工决算（含税）/静态投资（万元）/总额"] = self.project_detail.get("变电工程/竣工决算（含税）/静态投资（万元）/总额")
        target.value = do_division(
            data_raw["变电工程/竣工决算（含税）/静态投资（万元）/总额"], data_raw["新增线路长度（公里）"])

        yield target

    def cal_construction_cost(self):
        yield from self.component_single_target(CONSTRUCTION_COST, "变电工程/竣工决算（含税）/静态投资（万元）/其中，建场费")

    def cal_wire_length_construction_per_unit(self):
        data_raw = {}
        target = Target(
            name=WIRE_LENGTH_CONSTRUCTION_PER_UNIT,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        project = ProjectManager.get_project(self.project_detail["wbs_code"])
        data_raw["新增线路长度（公里）"] = project.wire_length
        data_raw["变电工程/竣工决算（含税）/静态投资（万元）/其中，建场费"] = \
            self.project_detail.get("变电工程/竣工决算（含税）/静态投资（万元）/其中，建场费")
        target.value = do_division(
            data_raw["变电工程/竣工决算（含税）/静态投资（万元）/其中，建场费"], data_raw["新增线路长度（公里）"])

        yield target

    def cal_design_change_rate(self):
        data_raw = {}
        target = Target(
            name=DESIGN_CHANGE_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        for name_raw in ["变电工程设计变更及变更设计情况/土建变更/金额（万元）",
                         "变电工程设计变更及变更设计情况/电气变更/金额（万元）",
                         "线路工程设计变更及变更设计情况/架空变更/金额（万元）",
                         "线路工程设计变更及变更设计情况/电缆变更/金额（万元）",
                         "工程整体/竣工决算（含税）/动态投资（万元）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        if has_all_number(data_raw):
            target.value = keep_percent(data_raw["变电工程设计变更及变更设计情况/土建变更/金额（万元）"] +
                                        data_raw["变电工程设计变更及变更设计情况/电气变更/金额（万元）"] +
                                        data_raw["线路工程设计变更及变更设计情况/架空变更/金额（万元）"] +
                                        data_raw["线路工程设计变更及变更设计情况/电缆变更/金额（万元）"],
                                        data_raw["工程整体/竣工决算（含税）/动态投资（万元）"],
                                        dividend_abs=True)

        yield target

    def cal_saving_rate(self):
        data_raw = {}
        target = Target(
            name=SAVING_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        for name_raw in ["工程整体/投资估算/动态投资（万元）",
                         "工程整体/批准概算/动态投资（万元）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)
        if has_all_number(data_raw):
            target.value = keep_percent(
                data_raw["工程整体/投资估算/动态投资（万元）"]-data_raw["工程整体/批准概算/动态投资（万元）"],
                data_raw["工程整体/投资估算/动态投资（万元）"])

        yield target

    def cal_saving_rate_final(self):
        data_raw = {}
        target = Target(
            name=SAVING_RATE_FINAL,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        for name_raw in ["工程整体/竣工决算（含税）/动态投资（万元）",
                         "工程整体/批准概算/动态投资（万元）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)
        if has_all_number(data_raw):
            target.value = keep_percent(
                data_raw["工程整体/批准概算/动态投资（万元）"]-data_raw["工程整体/竣工决算（含税）/动态投资（万元）"],
                data_raw["工程整体/批准概算/动态投资（万元）"])

        yield target

    def cal_start_time_diff_rate(self):
        data_raw = {}
        data_raw_cal = {}
        target = Target(
            name=START_TIME_DIFF_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["开工时间/实际",
                         "开工时间/计划",
                         "竣工时间/实际"]:
            data_raw[name_raw] = format_datetime(self.project_detail.get(name_raw))
            data_raw_cal[name_raw] = self.project_detail.get(name_raw)

        if has_all_datetime(data_raw_cal):
            target.value = keep_percent((data_raw_cal["开工时间/实际"] - data_raw_cal["开工时间/计划"]).days,
                                                (data_raw_cal["竣工时间/实际"] - data_raw_cal["开工时间/实际"]).days)

        yield target

    def cal_produce_time_diff_rate(self):
        data_raw = {}
        data_raw_cal = {}
        target = Target(
            name=PRODUCE_TIME_DIFF_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["投产时间/实际",
                         "投产时间/计划",
                         "开工时间/实际",
                         "竣工时间/实际"]:
            data_raw[name_raw] = format_datetime(self.project_detail.get(name_raw))
            data_raw_cal[name_raw] = self.project_detail.get(name_raw)

        if has_all_datetime(data_raw_cal):
            target.value = keep_percent((data_raw_cal["投产时间/实际"] - data_raw_cal["投产时间/计划"]).days,
                                                (data_raw_cal["竣工时间/实际"] - data_raw_cal["开工时间/实际"]).days)

        yield target

    def cal_power_supply_time_diff(self):
        yield self.time_difference_target(
            POWER_SUPPLY_TIME_DIFF, "投产时间/实际", "电源送出时间/电源实际投运时间")

    def cal_electric_railway_time_diff(self):
        yield self.time_difference_target(
            ELECTRIC_RAILWAY_TIME_DIFF, "投产时间/实际", "电铁投运时间/电铁实际投运时间")

    def cal_transformer_load_rate(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code, ("变电站最大负荷时刻有功功率（MW）",))
        target = Target(
            name=TRANSFORMER_LOAD_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        project = ProjectManager.get_project(self.wbs_code)
        data_raw["新增变电容量（MVA）"] = project.capacitance

        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            return keep_percent(v["变电站最大负荷时刻有功功率（MW）"], v["新增变电容量（MVA）"])

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_transformer_average_load_rate(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("额定容量（MVA）", "下网电量（万kWh）", "上网电量（万kWh）"))
        target = Target(
            name=TRANSFORMER_AVERAGE_LOAD_RATE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["上网电量（万kWh）"])
                b = float(v["下网电量（万kWh）"])
                c = float(v["额定容量（MVA）"])
            except Exception as e:
                return None

            return keep_percent((a + b), c * 8760)

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_maximum_load_power_factor(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("变电站最大负荷时刻有功功率（MW）", "变电站最大负荷时刻无功功率（Mvar）"))
        target = Target(
            name=MAXIMUM_LOAD_POWER_FACTOR,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["变电站最大负荷时刻有功功率（MW）"])
                b = float(v["变电站最大负荷时刻无功功率（Mvar）"])
            except Exception as e:
                return None

            return do_division(a, (a ** 2 + b ** 2) ** 0.5)

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_increase_power_supply_per_unit(self):
        data_raw = {}
        target = Target(
            name=INCREASE_POWER_SUPPLY_PER_UNIT,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        project = ProjectManager.get_project(self.project_detail["wbs_code"])
        data_raw["新增变电容量（MVA）"] = project.capacitance
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_raw["工程供（输）电量/工程供（输）增供电量（万kWh）"] = self.get_year_increase_value(
            data_raw["工程供（输）电量/工程供（输）电量（万kWh）"])

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return do_division(v.get("工程供（输）电量/工程供（输）增供电量（万kWh）"), v.get("新增变电容量（MVA）"))
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_maximum_load_rate_line(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("线路额定容量（MVA）", "线路最大负荷时刻有功功率（MW）"))
        target = Target(
            name=MAXIMUM_LOAD_RATE_LINE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["线路最大负荷时刻有功功率（MW）"])
                b = float(v["线路额定容量（MVA）"])
            except Exception as e:
                return None

            return do_division(a * 100, b)
        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_average_load_rate_line(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("正向输送电量（万kWh）",
                                                                 "反向输送电量（万kWh）",
                                                                 "线路额定容量（MVA）"))
        target = Target(
            name=AVERAGE_LOAD_RATE_LINE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["正向输送电量（万kWh）"])
                b = float(v["反向输送电量（万kWh）"])
                c = float(v["线路额定容量（MVA）"])
            except Exception as e:
                return None

            return do_division(a+b, c*87.6)

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_maximum_load_power_factor_line(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("线路最大负荷时刻有功功率（MW）",
                                                                 "线路最大负荷时刻无功功率（Mvar）"))
        target = Target(
            name=MAXIMUM_LOAD_POWER_FACTOR_LINE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["线路最大负荷时刻有功功率（MW）"])
                b = float(v["线路最大负荷时刻无功功率（Mvar）"])
            except Exception as e:
                return None

            return do_division(a, (a ** 2 + b ** 2) ** 0.5)

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_increase_power_supply_per_year(self):
        data_raw = {}
        target = Target(
            name=INCREASE_POWER_SUPPLY_PER_YEAR,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        project = ProjectManager.get_project(self.project_detail["wbs_code"])
        data_raw["新增线路长度（公里）"] = project.wire_length
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return do_division(v.get("工程供（输）电量/工程供（输）电量（万kWh）"), v.get("新增线路长度（公里）"))
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_loss_rate_of_main_transformer(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("上网电量（万kWh）",
                                                                 "下网电量（万kWh）",
                                                                 "变电损耗电量（万kWh）"))
        target = Target(
            name=LOSS_RATE_OF_MAIN_TRANSFORMER,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["变电损耗电量（万kWh）"])
                b = float(v["上网电量（万kWh）"])
                c = float(v["下网电量（万kWh）"])
            except Exception as e:
                return None

            return do_division(a*100, b+c)

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_loss_rate_of_line(self):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code,
                                                                ("正向输送电量（万kWh）",
                                                                 "反向输送电量（万kWh）",
                                                                 "线路损耗电量（万kWh）"))
        target = Target(
            name=LOSS_RATE_OF_LINE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["线路损耗电量（万kWh）"])
                b = float(v["正向输送电量（万kWh）"])
                c = float(v["反向输送电量（万kWh）"])
            except Exception as e:
                return None

            return do_division(a*100, b+c)

        yield from self.parse_continuous_component_data_cal(target, data_cal, compute)

    def cal_forced_shutdown_of_substation(self):
        yield from self.component_count_target(FORCED_SHUTDOWN_OF_SUBSTATION, "变压器强迫停运次数（次）")

    def cal_forced_shutdown_of_substation_hour(self):
        yield from self.component_count_target(FORCED_SHUTDOWN_OF_SUBSTATION_HOUR, "变压器强迫停运时间（小时）")

    def cal_forced_line_outage(self):
        yield from self.component_count_target(FORCED_LINE_OUTAGE, "线路强迫停运次数（次）")

    def cal_forced_line_outage_hour(self):
        yield from self.component_count_target(FORCED_LINE_OUTAGE_HOUR, "线路强迫停运时间（小时）")

    def cal_qualified_rate_of_bus_voltage(self):
        data_raw = {}
        target = Target(
            name=QUALIFIED_RATE_OF_BUS_VOLTAGE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["母线电压合格率（%）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["母线电压合格率（%）"])
            except Exception as e:
                return None

            return a
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_times_of_operation_mistake_device(self):
        data_raw = {}
        target = Target(
            name=TIMES_OF_OPERATION_MISTAKE_DEVICE,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["继电保护和安稳装置误动、拒动次数（次）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["继电保护和安稳装置误动、拒动次数（次）"])
            except Exception as e:
                return None

            return a
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_assessment_times_affecting_power_quality(self):
        data_raw = {}
        target = Target(
            name=ASSESSMENT_TIMES_AFFECTING_POWER_QUALITY,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["影响电能质量考核次数（次）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["影响电能质量考核次数（次）"])
            except Exception as e:
                return None

            return a
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_power_supply_of_project(self):
        data_raw = {}
        target = Target(
            name=POWER_SUPPLY_OF_PROJECT,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            try:
                a = float(v["工程供（输）电量/工程供（输）电量（万kWh）"])
            except Exception as e:
                return None

            return a
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_unit_capacity(self):
        data_raw = {}
        target = Target(
            name=UNIT_CAPACITY,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        project = ProjectManager.get_project(self.project_detail["wbs_code"])
        data_raw["新增线路长度（公里）"] = project.wire_length
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return do_division(v.get("工程供（输）电量/工程供（输）电量（万kWh）"), v.get("新增线路长度（公里）"))

        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_transmission_and_distribution_assets_of_unit_newly(self):
        data_raw = {}
        target = Target(
            name=TRANSMISSION_AND_DISTRIBUTION_ASSETS_OF_UNIT_NEWLY,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）", "固定资产（万元）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return do_division(v.get("工程供（输）电量/工程供（输）电量（万kWh）"), v.get("固定资产（万元）"))

        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_internal_rate_total_investment(self):
        yield from self.component_single_target(INTERNAL_RATE_TOTAL_INVESTMENT, "方案二/总投资内部收益率（税后）（%）")

    def cal_internal_rate_total_capital(self):
        yield from self.component_single_target(INTERNAL_RATE_TOTAL_CAPITAL, "方案二/资本金内部收益率（税后）（%）")

    def cal_payback_period(self):
        yield from self.component_single_target(PAYBACK_PERIOD, "方案二/静态投资回收期（年）")

    def cal_debt_service_coverage_ratio(self):
        yield from self.component_single_target(DEBT_SERVICE_COVERAGE_RATIO, "方案二/偿债备付率")

    def cal_interest_provision_rate(self):
        yield from self.component_single_target(INTEREST_PROVISION_RATE, "方案二/利息备付率")

    def cal_completion_rate_of_breakeven_electricity(self):
        data_raw = {}
        target = Target(
            name=COMPLETION_RATE_OF_BREAKEVEN_ELECTRICITY,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）", "工程供（输）电量/方案3预测值（万kWh）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)
        data_raw["盈亏平衡电量"] = data_raw["工程供（输）电量/方案3预测值（万kWh）"]
        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return keep_percent(v.get("工程供（输）电量/工程供（输）电量（万kWh）"), v.get("工程供（输）电量/方案3预测值（万kWh）"))
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_completion_rate_of_feasibility_electricity(self):
        data_raw = {}
        target = Target(
            name=COMPLETION_RATE_OF_FEASIBILITY_ELECTRICITY,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）", "工程供（输）电量/方案2预测值（万kWh）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_raw["可研电量"] = None
        if data_raw["工程供（输）电量/方案2预测值（万kWh）"] and len(data_raw["工程供（输）电量/方案2预测值（万kWh）"]) > 5:
            t = sorted(data_raw["工程供（输）电量/方案2预测值（万kWh）"], key=lambda i: i["year"])
            data_raw["可研电量"] = t[5]["value"]
        del data_raw["工程供（输）电量/方案2预测值（万kWh）"]

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return keep_percent(v.get("工程供（输）电量/工程供（输）电量（万kWh）"), v.get("可研电量"))
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_completion_rate_of_feasibility_study_benefit(self):
        data_raw = {}
        target = Target(
            name=COMPLETION_RATE_OF_FEASIBILITY_STUDY_BENEFIT,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["方案一/总投资内部收益率（税后）（%）", "方案二/总投资内部收益率（税后）（%）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        if has_all_number(data_raw):
            a = 2 * min(data_raw["方案一/总投资内部收益率（税后）（%）"], data_raw["方案二/总投资内部收益率（税后）（%）"])
            target.value = keep_percent(data_raw["方案一/总投资内部收益率（税后）（%）"] + a,
                                           data_raw["方案二/总投资内部收益率（税后）（%）"] + a)

        yield target

    def cal_power_transmission_distribution_cost(self):
        data_raw = {}
        target = Target(
            name=POWER_TRANSMISSION_DISTRIBUTION_COST,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["工程供（输）电量/工程供（输）电量（万kWh）", "经营成本（总计）（万元）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        data_cal = self.parse_continuous(data_raw)

        def compute(v):
            return do_division(v.get("经营成本（总计）（万元）"), v.get("工程供（输）电量/工程供（输）电量（万kWh）"))
        yield from self.parse_continuous_data_cal(target, data_cal, compute)

    def cal_unit_investment_power_transmission_distribution(self):
        data_raw = {}
        target = Target(
            name=UNIT_INVESTMENT_POWER_TRANSMISSION_DISTRIBUTION,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in ["工程供（输）电量/方案2预测值（万kWh）", "建设期各年投资（万元）/总投资（动态投资）"]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        if data_raw.get("工程供（输）电量/方案2预测值（万kWh）"):
            total = sum(float(item["value"]) for item in data_raw.get("工程供（输）电量/方案2预测值（万kWh）") if item.get("value"))
            target.value = do_division(total, data_raw["建设期各年投资（万元）/总投资（动态投资）"])

            yield target

    def do_project_target_calculation(self):
        for attr in dir(self):
            if attr.startswith("cal"):
                for target in getattr(self, attr)():
                    if target and target.value is not None:
                        TargetManager.add_target(target)

        # for target in self.cal_completion_rate_of_feasibility_electricity():
        #     if target and target.value is not None:
        #         TargetManager.add_target(target)
