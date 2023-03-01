from app.project_evaluation.manager.models import TargetStatus


PROJECT_DEVIATION_RATE = "程序偏差率（%）"
DOCUMENT_COMPLETE_RATE = "支撑文件完整度（%）"
CAPACITANCE_PER_UNIT = "单位变电容量造价水平（万元/MVA）"
WIRE_LENGTH_PER_UNIT = "单位线路长度造价水平（万元/公里）"
CONSTRUCTION_COST = "变电工程单站建场费（万元）"
WIRE_LENGTH_CONSTRUCTION_PER_UNIT = "线路工程单位长度建场费（万元）"
DESIGN_CHANGE_RATE = "设计变更金额比例（%）"
SAVING_RATE = "概算较估算节余率（%）"
SAVING_RATE_FINAL = "决算较概算节余率（%）"
START_TIME_DIFF_RATE = "开工时间差异率（%）"
PRODUCE_TIME_DIFF_RATE = "投产时间差异率（%）"
POWER_SUPPLY_TIME_DIFF = "电源送出工程投产时间与电源投产差异时间（天）"
ELECTRIC_RAILWAY_TIME_DIFF = "电铁供电工程投产时间与电铁投产差异时间（天）"
TRANSFORMER_LOAD_RATE = "主变最大负载率（%）"
TRANSFORMER_AVERAGE_LOAD_RATE = "主变平均负载率（%）"
MAXIMUM_LOAD_POWER_FACTOR = "主变最大负荷功率因数"
INCREASE_POWER_SUPPLY_PER_UNIT = "单位变电容量增供电量（万kWh/MVA）"
MAXIMUM_LOAD_RATE_LINE = "线路最大负载率（%）"
AVERAGE_LOAD_RATE_LINE = "线路平均负载率（%）"
MAXIMUM_LOAD_POWER_FACTOR_LINE = "线路最大负荷功率因数"
INCREASE_POWER_SUPPLY_PER_YEAR = "单位线路长度增输电量（万kWh/公里）"
LOSS_RATE_OF_MAIN_TRANSFORMER = "主变损耗率（%）"
LOSS_RATE_OF_LINE = "线路损耗率（%）"
FORCED_SHUTDOWN_OF_SUBSTATION = "变电强迫停运次数（次）"
FORCED_SHUTDOWN_OF_SUBSTATION_HOUR = "变压器强迫停运时间（小时）"
FORCED_LINE_OUTAGE = "线路强迫停运次数（次）"
FORCED_LINE_OUTAGE_HOUR = "线路强迫停运时间（小时）"
QUALIFIED_RATE_OF_BUS_VOLTAGE = "母线电压合格率（%）"
TIMES_OF_OPERATION_MISTAKE_DEVICE = "继电保护和安稳装置误动、拒动次数（次）"
ASSESSMENT_TIMES_AFFECTING_POWER_QUALITY = "影响电能质量考核次数（次）"
POWER_SUPPLY_OF_PROJECT = "供（输）送电量（万kWh）"
UNIT_CAPACITY = "单位容量电量（万kWh/MVA）"
TRANSMISSION_AND_DISTRIBUTION_ASSETS_OF_UNIT_NEWLY = "单位新增电量输配电资产（元/kWh）"
INTERNAL_RATE_TOTAL_INVESTMENT = "总投资内部收益率（%）"
INTERNAL_RATE_TOTAL_CAPITAL = "资本金内部收益率（%）"
PAYBACK_PERIOD = "投资回收期（年）"
DEBT_SERVICE_COVERAGE_RATIO = "偿债备付率"
INTEREST_PROVISION_RATE = "利息备付率"
COMPLETION_RATE_OF_BREAKEVEN_ELECTRICITY = "盈亏平衡电量完成率（%）"
COMPLETION_RATE_OF_FEASIBILITY_ELECTRICITY = "可研电量完成率（%）"
COMPLETION_RATE_OF_FEASIBILITY_STUDY_BENEFIT = "可研效益完成率（%）"
POWER_TRANSMISSION_DISTRIBUTION_COST = "评价年单位电量输配电成本（元/kWh）"
UNIT_INVESTMENT_POWER_TRANSMISSION_DISTRIBUTION = "单位投资输配电量（kWh/元 ）"


construction_control = {
    "效益指标": {
        "造价控制": [CAPACITANCE_PER_UNIT,
                 WIRE_LENGTH_PER_UNIT,
                 CONSTRUCTION_COST,
                 WIRE_LENGTH_CONSTRUCTION_PER_UNIT,
                 DESIGN_CHANGE_RATE],
        "投资节余": [
            SAVING_RATE,
            SAVING_RATE_FINAL
        ]
    },
    "效率指标": {
        "合规性": [PROJECT_DEVIATION_RATE, DOCUMENT_COMPLETE_RATE],
        "计划执行": [START_TIME_DIFF_RATE, PRODUCE_TIME_DIFF_RATE],
        "配套电网工程投运时序": [POWER_SUPPLY_TIME_DIFF, ELECTRIC_RAILWAY_TIME_DIFF]
    }
}

operation_effect = {
    "效益指标": {
        "电量效益": [POWER_SUPPLY_OF_PROJECT, UNIT_CAPACITY, TRANSMISSION_AND_DISTRIBUTION_ASSETS_OF_UNIT_NEWLY],
        "安全效益": [FORCED_SHUTDOWN_OF_SUBSTATION,
                 FORCED_SHUTDOWN_OF_SUBSTATION_HOUR,
                 FORCED_LINE_OUTAGE,
                 FORCED_LINE_OUTAGE_HOUR,
                 QUALIFIED_RATE_OF_BUS_VOLTAGE,
                 TIMES_OF_OPERATION_MISTAKE_DEVICE,
                 ASSESSMENT_TIMES_AFFECTING_POWER_QUALITY
                 ]
    },
    "效率指标": {
        "变电利用效率": [TRANSFORMER_LOAD_RATE, TRANSFORMER_AVERAGE_LOAD_RATE, MAXIMUM_LOAD_POWER_FACTOR, INCREASE_POWER_SUPPLY_PER_UNIT],
        "输电利用效率": [MAXIMUM_LOAD_RATE_LINE, AVERAGE_LOAD_RATE_LINE, MAXIMUM_LOAD_POWER_FACTOR_LINE, INCREASE_POWER_SUPPLY_PER_YEAR],
        "运行损耗": [LOSS_RATE_OF_MAIN_TRANSFORMER, LOSS_RATE_OF_LINE]
    }
}

investment_control = {
    "效益指标": {
        "盈利能力": [INTERNAL_RATE_TOTAL_INVESTMENT, INTERNAL_RATE_TOTAL_CAPITAL, PAYBACK_PERIOD],
        "偿债能力": [DEBT_SERVICE_COVERAGE_RATIO, INTEREST_PROVISION_RATE],
        "风险控制": [COMPLETION_RATE_OF_BREAKEVEN_ELECTRICITY, COMPLETION_RATE_OF_FEASIBILITY_ELECTRICITY, COMPLETION_RATE_OF_FEASIBILITY_STUDY_BENEFIT]
    },
    "效率指标": {
        "输配电成本": [POWER_TRANSMISSION_DISTRIBUTION_COST],
        "全周期投资输配电量": [UNIT_INVESTMENT_POWER_TRANSMISSION_DISTRIBUTION]
    }
}

target_primary_index = {
    "construction_control": construction_control,
    "operation_effect": operation_effect,
    "investment_control": investment_control
}


RED = "red"
GREEN = "green"

NORMAL_STATUS = TargetStatus(GREEN, "正常")
ABNORMAL_STATUS = TargetStatus(RED, "异常")
DESIGN_NOT_CHANGE_STATUS = TargetStatus(GREEN, "无设计变更")
DESIGN_CHANGE_STATUS = TargetStatus(RED, "有设计变更")


HEAVY_LOAD_STATUS = TargetStatus(RED, "重载")
LIGHT_LOAD_STATUS = TargetStatus(RED, "轻载")
REASONABLE_STATUS = TargetStatus(GREEN, "合理")


PROJECT_PRE_TIME_STATUS = TargetStatus(GREEN, "工程超前投产")
PROJECT_ON_TIME_STATUS = TargetStatus(GREEN, "工程与电源投产时间一致")
PROJECT_POST_TIME_STATUS = TargetStatus(RED, "工程滞后投产")
REASONABLE_CAPACITY_OF_MAIN_TRANSFORMER = TargetStatus(GREEN, "主变容量选择合理")
UNREASONABLE_CAPACITY_OF_MAIN_TRANSFORMER = TargetStatus(RED, "主变容量选择不合理")
LOW_VOLTAGE = TargetStatus(RED, "电压较低")
QUALIFIED_VOLTAGE = TargetStatus(GREEN, "电压合格")
GOOD_VOLTAGE = TargetStatus(GREEN, "电压良好")
ELECTRICITY_RAISE = TargetStatus(RED, "电量上升")
ELECTRICITY_DECLINE = TargetStatus(RED, "电量下降")
ELECTRICITY_UNCHANGED = TargetStatus(RED, "电量不变")
CAPITAL_RECOVERY = TargetStatus(GREEN, "资金已回收")
CAPITAL_NOT_RECOVERY = TargetStatus(RED, "资金尚未回收")
ELECTRICITY_UNBALANCE = TargetStatus(GREEN, "未达到盈亏平衡电量")
ELECTRICITY_BALANCE = TargetStatus(GREEN, "达到盈亏平衡电量")
REACH_FEASIBILITY_ELECTRICITY = TargetStatus(GREEN, "达到可研电量")
NOT_REACH_FEASIBILITY_ELECTRICITY = TargetStatus(GREEN, "未达到可研电量")


target_status = {
    PROJECT_DEVIATION_RATE: {
        "rule": "程序偏差率应为0",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 1
    },
    DOCUMENT_COMPLETE_RATE: {
        "rule": "支撑文件完整度应为100%",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 1
    },
    CAPACITANCE_PER_UNIT: {
        "rule": "与均值对比",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 2
    },
    WIRE_LENGTH_PER_UNIT: {
        "rule": "与均值对比",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 2
    },
    CONSTRUCTION_COST: {
        "rule": "与均值对比",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 2
    },
    WIRE_LENGTH_CONSTRUCTION_PER_UNIT: {
        "rule": "与均值对比",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 2
    },
    DESIGN_CHANGE_RATE: {
        "rule": "设计变更金额比例越小越好",
        "status": [DESIGN_CHANGE_STATUS, DESIGN_NOT_CHANGE_STATUS],
        "show_type": 1
    },
    SAVING_RATE: {
        "rule": '概算较估算节余率宜不超过20%；概算较估算节余率小于0%为概算超估算',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 3,
        "boundary": [(0, 10), (10, 20), (20, 30), (30, "Infinity")]
    },
    SAVING_RATE_FINAL: {
        "rule": '决算较估算节余率宜不超过20%；决算较估算节余率小于0%为概算超估算',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 3,
        "boundary": [(0, 10), (10, 20), (20, 30), (30, "Infinity")]
    },
    START_TIME_DIFF_RATE: {
        "show_type": 1
    },
    PRODUCE_TIME_DIFF_RATE: {
        "show_type": 1
    },
    POWER_SUPPLY_TIME_DIFF: {
        "rule": '若指标值＜0，送出工程超前投产, 若指标值=0，送出工程与电源投产时间一致,若指标值＞0，送出工程滞后投产',
        "status": [PROJECT_PRE_TIME_STATUS, PROJECT_ON_TIME_STATUS, PROJECT_POST_TIME_STATUS],
        "show_type": 1
    },
    ELECTRIC_RAILWAY_TIME_DIFF: {
        "rule": '若指标值＜0，送出工程超前投产, 若指标值=0，送出工程与电源投产时间一致,若指标值＞0，送出工程滞后投产',
        "status": [PROJECT_PRE_TIME_STATUS, PROJECT_ON_TIME_STATUS, PROJECT_POST_TIME_STATUS],
        "show_type": 1
    },
    TRANSFORMER_LOAD_RATE: {
        "rule": "投运三年后，主变最大负载率高于25%说明实现规划目标；投运五年后，主变最大负载率高于40%说明实现规划目标",
        "status": [REASONABLE_CAPACITY_OF_MAIN_TRANSFORMER, UNREASONABLE_CAPACITY_OF_MAIN_TRANSFORMER],
        "continuous": True,
        "component": True,
        "show_type": 2
    },
    TRANSFORMER_AVERAGE_LOAD_RATE: {
        "rule": "变压器投运三年后，主变平均负载率大于等于50%为重载；主变平均负载率小于等于25%为轻载；主变平均负载率大于25%小于50%为合理",
        "status": [HEAVY_LOAD_STATUS, LIGHT_LOAD_STATUS, NORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 2
    },
    MAXIMUM_LOAD_POWER_FACTOR: {
        "rule": "主变最大负荷功率因数不低于0.95",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 3,
        "boundary": [(0, 0.95), (0.95, "Infinity")]
    },
    INCREASE_POWER_SUPPLY_PER_UNIT: {
        "continuous": True,
        "show_type": 1
    },
    MAXIMUM_LOAD_RATE_LINE: {
        "rule": '线路最大负载率超过80%为重载；线路最大负载率低于20%为轻载，其余为合理',
        "status": [HEAVY_LOAD_STATUS, LIGHT_LOAD_STATUS, NORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 3,
        "boundary": [(0, 20), (20, 80), (80, "Infinity")]
    },
    AVERAGE_LOAD_RATE_LINE: {
        "rule": "线路平均负载率超过80%为重载；线路平均负载率低于20%为轻载；其余为合理",
        "status": [HEAVY_LOAD_STATUS, LIGHT_LOAD_STATUS, NORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 3,
        "boundary": [(0, 20), (20, 80), (80, "Infinity")]
    },
    MAXIMUM_LOAD_POWER_FACTOR_LINE: {
        "rule": "线路最大负荷功率因数不低于0.95",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 3,
        "boundary": [(0, 0.95), (0.95, "Infinity")]
    },
    INCREASE_POWER_SUPPLY_PER_YEAR: {
        "continuous": True,
        "show_type": 1
    },
    LOSS_RATE_OF_MAIN_TRANSFORMER: {
        "rule": '主变损耗率小于等于同电压等级、同容量变压器平均损耗时，损耗合理',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 2
    },
    LOSS_RATE_OF_LINE: {
        "rule": '线路损耗率大于同电压等级架空线路平均损耗时，损耗严重；线路损耗率小于等于同电压等级架空线路平均损耗时，损耗合理',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 2
    },
    FORCED_SHUTDOWN_OF_SUBSTATION: {
        "rule": '强迫停运次数应为0',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 1
    },
    FORCED_SHUTDOWN_OF_SUBSTATION_HOUR: {
        "rule": "强迫停运次数应为0",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 1
    },
    FORCED_LINE_OUTAGE: {
        "rule": "强迫停运次数应为0",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 1
    },
    FORCED_LINE_OUTAGE_HOUR: {
        "rule": "强迫停运次数应为0",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "component": True,
        "show_type": 1
    },
    QUALIFIED_RATE_OF_BUS_VOLTAGE: {
        "rule": '母线电压合格率超过99.99%时良好； 低于99.95%时偏低；其余为合格',
        "status": [LOW_VOLTAGE, QUALIFIED_VOLTAGE, GOOD_VOLTAGE],
        "continuous": True,
        "show_type": 3,
        "boundary": [(0, 99.95), (99.95, 99.99), (99.99, "Infinity")]
    },
    TIMES_OF_OPERATION_MISTAKE_DEVICE: {
        "rule": '继电保护和安稳装置误动、拒动次数原则上为0',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "show_type": 1
    },
    ASSESSMENT_TIMES_AFFECTING_POWER_QUALITY: {
        "rule": "影响电能质量考核次数数原则上为0",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "continuous": True,
        "show_type": 1
    },
    POWER_SUPPLY_OF_PROJECT: {
        "rule": '当年供（输）送电量高于上一年供（输）电量时，说明电量增长；当年供（输）送电量低于上一年供（输）电量时，说明电量下降',
        "status": [ELECTRICITY_RAISE, ELECTRICITY_DECLINE, ELECTRICITY_UNCHANGED],
        "continuous": True,
        "show_type": 1
    },
    UNIT_CAPACITY: {
        "continuous": True,
        "show_type": 1
    },
    TRANSMISSION_AND_DISTRIBUTION_ASSETS_OF_UNIT_NEWLY: {
        "continuous": True,
        "show_type": 1
    },
    INTERNAL_RATE_TOTAL_INVESTMENT: {
        "rule": '总投资内部收益率大于基准收益率7%时，项目效益良好',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 3,
        "boundary": [("-Infinity", 0), (0, 7), (7, "Infinity")]
    },
    INTERNAL_RATE_TOTAL_CAPITAL: {
        "rule": '资本金内部收益率大于基准收益率9%时，项目效益良好',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 3,
        "boundary": [("-Infinity", 0), (0, 9), (9, "Infinity")]
    },
    PAYBACK_PERIOD: {
        "rule": "投资回收期小于等于投产年，资金已回收；投资回收期大于投产年，资金尚未回收",
        "status": [CAPITAL_RECOVERY, CAPITAL_NOT_RECOVERY],
        "show_type": 3,
        "boundary": [("-Infinity", 0), (0, "Infinity")]
    },
    DEBT_SERVICE_COVERAGE_RATIO: {
        "rule": '偿债备付率不宜低于1.3',
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 1
    },
    INTEREST_PROVISION_RATE: {
        "rule": "利息备付率不宜低于2",
        "status": [NORMAL_STATUS, ABNORMAL_STATUS],
        "show_type": 1
    },
    COMPLETION_RATE_OF_BREAKEVEN_ELECTRICITY: {
        "rule": "盈亏平衡电量完成率超过100%，说明评价年电量达到盈亏平衡电量；盈亏平衡电量完成率低于100%，说明评价年电量未达到盈亏平衡电量",
        "status": [ELECTRICITY_BALANCE, ELECTRICITY_UNBALANCE],
        "show_type": 1,
        "continuous": True
    },
    COMPLETION_RATE_OF_FEASIBILITY_ELECTRICITY: {
        "rule": '可研电量完成率超过100%，说明评价年电量达到可研电量；盈亏平衡电量完成率低于100%，说明评价年电量未达到可研电量',
        "status": [REACH_FEASIBILITY_ELECTRICITY, NOT_REACH_FEASIBILITY_ELECTRICITY],
        "show_type": 1,
        "continuous": True
    },
    COMPLETION_RATE_OF_FEASIBILITY_STUDY_BENEFIT: {
        "show_type": 1,
    },
    POWER_TRANSMISSION_DISTRIBUTION_COST: {
        "continuous": True,
        "show_type": 2
    },
    UNIT_INVESTMENT_POWER_TRANSMISSION_DISTRIBUTION: {
        "show_type": 1
    }
}
