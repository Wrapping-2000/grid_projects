
WATER_POWER = "水电发电量（MW）"
WIND_POWER = "风电发电量（MW）"
SUN_POWER = "光伏发电量（MW）"
BIOMASS_POWER = "生物质能发电量（MW）"
SOCIAL_POWER = "全社会用电量（MW）"
TOTAL_POWER = "总发电量（MW）"
RENEWABLE_POWER_RATE = "可再生能源发电量占比（%）"
WATER_POWER_RATE = "水电发电量占比（%）"
WIND_POWER_RATE = "风电发电量占比（%）"
SUN_POWER_RATE = "光伏发电量占比（%）"
BIOMASS_POWER_RATE = "生物质能发电量占比（%）"

WATER_INSTALL = "水电装机容量（MW）"
WIND_INSTALL = "风电装机容量（MW）"
SUN_INSTALL = "光伏装机容量（MW）"
BIOMASS_INSTALL = "生物质能装机容量（MW）"
TOTAL_INSTALL = "并网发电装机容量（MW）"
RENEWABLE_INSTALL_RATE = "可再生能源接入装机占比（%）"
WATER_INSTALL_RATE = "水电接入装机占比（%）"
WIND_INSTALL_RATE = "风电接入装机占比（%）"
SUN_INSTALL_RATE = "光伏接入装机占比（%）"
BIOMASS_INSTALL_RATE = "生物质能接入装机占比（%）"

CO2_REDUCE = "二氧化碳减排量（万吨）"
SO2_REDUCE = "二氧化硫减排量（万吨）"

WIND_PERMEABILITY = "风电渗透率（%）"
SUN_PERMEABILITY = "光伏渗透率（%）"

SALE_POWER_YEAR_GROW_RATE = "全社会售电量逐年增速（%）"
SALE_POWER_YEAR_AVERAGE_RATE = "全社会售电量年均增长率（%）"

MAX_LOAD = "统调最大负荷（MW）"
MAX_LOAD_YEAR_GROW_RATE = "统调最大负荷逐年增速（%）"
MAX_LOAD_YEAR_AVERAGE_RATE = "统调最大负荷年均增长率（%）"

VARIABLE_CAPACITY = "变配（电）容量（KV.A）"
VARIABLE_CAPACITY_YEAR_GROW_RATE = "变配（电）容量逐年增速（%）"
VARIABLE_CAPACITY_YEAR_AVERAGE_RATE = "变配（电）容量年均增长率（%）"

LINE_LENGTH = "线路长度（km）"
LINE_LENGTH_YEAR_GROW_RATE = "线路长度逐年增速（%）"
LINE_LENGTH_YEAR_AVERAGE_RATE = "线路长度年均增长率（%）"

MAX_USE_LOAD = "最高用电负荷（MW）"
SUM_VARIABLE_CAPACITY = "变电容量之和（KV.A）"
UNIT_VARIABLE_CAPACITY = "单位变电容量支撑用电负荷"

SUM_LINE_LENGTH = "线路长度之和（km）"
UNIT_LINE_LENGTH = "单位线路长度支撑用电负荷"

PER_HOUSE_CAPACITY = "户均配变容量"

NET_CONNECTIVITY_LINE_NUMS = "750、500、220、110千伏电压等级线路条数"
NET_CONNECTIVITY_SUBSTATION_NUMS = "750、500、220、110千伏电压等级变电站个数"
NET_CONNECTIVITY = "750、500、220、110千伏电压等级电网连接度"

HUNDRED_AVERAGE_SINGLE_LINE_LENGTH = "110（66）千伏平均单条线路长度（公里/条）"
HUNDRED_LINE_LENGTH_SUM = "110（66）千伏线路长度合计（公里）"
HUNDRED_LINE_NUMS = "110（66）千伏线路条数（条）"

THIRTY_FIVE_AVERAGE_SINGLE_LINE_LENGTH = "35千伏平均单条线路长度（公里/条）"
THIRTY_FIVE_LINE_LENGTH_SUM = "35千伏线路长度合计（公里）"
THIRTY_FIVE_LINE_NUMS = "35千伏线路条数（条）"

GAS_POWER_RATE = "气电发电量占比（%）"
GAS_POWER = "气电发电量（MW）"
SALE_POWER = "全社会售电量（kw.h）"

STORE_CAPACITY_RATE = "储能配置率（%）"
STORE_CAPACITY = "储能容量（MW）"
NEW_ENERGY_INSTALL = "新能源装机容量（MW）"

RENEWABLE_POWER_INSTALL = "可再生能源接入"
ENV_BENEFIT = "环境效益"
NEW_POWER_PERMEABILITY = "新能源电量渗透率"
NET_DEVELOP_SPEED = "电网发展增速"
NET_SIZE = "电网规模"
NET_FRAMEWORK = "网架结构"
NET_ADJUST_ABILITY = "电网调节能力"

GREEN_CLEAN = "绿色清洁"
FLEXIBLE_INTELLIGENT = "灵活智能"

green_clean = [{"type": "可再生能源接入",
               "indicators":
                   [
                     {"indicator": RENEWABLE_POWER_RATE},
                     {"indicator": WATER_POWER_RATE},
                     {"indicator": WIND_POWER_RATE},
                     {"indicator": SUN_POWER_RATE},
                     {"indicator": BIOMASS_POWER_RATE},
                     {"indicator": RENEWABLE_INSTALL_RATE},
                     {"indicator": WATER_INSTALL_RATE},
                     {"indicator": WIND_INSTALL_RATE},
                     {"indicator": SUN_INSTALL_RATE},
                     {"indicator": BIOMASS_INSTALL_RATE}
                   ]
                },
               {"type": "环境效益",
                "indicators":
                     [
                       {"indicator": CO2_REDUCE},
                       {"indicator": SO2_REDUCE}
                     ]
                },
               {"type": "新能源电量渗透率",
                "indicators":
                    [
                      {"indicator": WIND_PERMEABILITY},
                      {"indicator": SUN_PERMEABILITY}
                    ]
               }]

flexible_intelligent = [{"type": "电网发展增速",
                         "indicators":
                             [
                                 {"indicator": SALE_POWER_YEAR_GROW_RATE},
                                 {"indicator": SALE_POWER_YEAR_GROW_RATE},
                                 {"indicator": MAX_LOAD_YEAR_GROW_RATE},
                                 {"indicator": MAX_LOAD_YEAR_AVERAGE_RATE},
                                 {"indicator": VARIABLE_CAPACITY_YEAR_GROW_RATE},
                                 {"indicator": VARIABLE_CAPACITY_YEAR_AVERAGE_RATE},
                                 {"indicator": LINE_LENGTH_YEAR_GROW_RATE},
                                 {"indicator": LINE_LENGTH_YEAR_AVERAGE_RATE}
                             ]
                         },
                        {"type": "电网规模",
                         "indicators":
                            [
                                {"indicator": UNIT_VARIABLE_CAPACITY},
                                {"indicator": UNIT_LINE_LENGTH},
                                {"indicator": PER_HOUSE_CAPACITY}
                            ]
                         },
                        {"type": "网架结构",
                         "indicators":
                             [
                                 {"indicator": HUNDRED_AVERAGE_SINGLE_LINE_LENGTH},
                                 {"indicator": THIRTY_FIVE_AVERAGE_SINGLE_LINE_LENGTH},
                                 {"indicator": NET_CONNECTIVITY}
                             ]
                         },
                        {
                        "type": "电网调节能力",
                        "indicators":
                             [
                                 {"indicator": GAS_POWER_RATE},
                                 {"indicator": STORE_CAPACITY_RATE}
                             ]
                         }]


type_indicator_renewable_power_rate = [
                                        {"names":
                                            [RENEWABLE_POWER_RATE,
                                             WATER_POWER,
                                             WIND_POWER,
                                             SUN_POWER,
                                             BIOMASS_POWER,
                                             SOCIAL_POWER]}
                                      ]
type_indicator_water_power_rate = [
                                     {"names":
                                         [WATER_POWER_RATE,
                                          WATER_POWER,
                                          SOCIAL_POWER]}
                                  ]
type_indicator_wind_power_rate = [
                                     {"names":
                                         [WIND_POWER_RATE, WIND_POWER, SOCIAL_POWER]}
                                  ]
type_indicator_sun_power_rate = [
                                     {"names":
                                         [SUN_POWER_RATE, SUN_POWER, SOCIAL_POWER]}
                                  ]
type_indicator_biomass_power_rate = [
                                     {"names":
                                         [BIOMASS_POWER_RATE, BIOMASS_POWER, SOCIAL_POWER]}
                                  ]
type_indicator_renewable_install_rate = [
                                        {"names":
                                             [RENEWABLE_INSTALL_RATE,
                                              TOTAL_INSTALL,
                                              WATER_INSTALL,
                                              WIND_INSTALL,
                                              SUN_INSTALL,
                                              BIOMASS_INSTALL]}
                                      ]
type_indicator_water_install_rate = [
                                     {"names":
                                         [WATER_INSTALL_RATE, WATER_INSTALL, TOTAL_INSTALL]}
                                  ]
type_indicator_wind_install_rate = [
                                     {"names":
                                         [WIND_INSTALL_RATE, WIND_INSTALL, TOTAL_INSTALL]}
                                  ]
type_indicator_sun_install_rate = [
                                     {"names":
                                         [SUN_INSTALL_RATE, SUN_INSTALL, TOTAL_INSTALL]}
                                  ]
type_indicator_biomass_install_rate = [
                                     {"names":
                                         [BIOMASS_INSTALL_RATE, BIOMASS_INSTALL, TOTAL_INSTALL]}
                                  ]
type_indicator_reduce_co2 = [
                                     {"names":
                                          [CO2_REDUCE,
                                           WATER_POWER,
                                           WIND_POWER,
                                           SUN_POWER,
                                           BIOMASS_POWER,
                                           ]}
                                  ]
type_indicator_reduce_so2 = [
                                     {"names":
                                          [SO2_REDUCE,
                                           WATER_POWER,
                                           WIND_POWER,
                                           SUN_POWER,
                                           BIOMASS_POWER,
                                           ]}
                                  ]
type_indicator_wind_permeability = [
                                     {"names":
                                          [WIND_PERMEABILITY, WIND_POWER, TOTAL_POWER]}
                                  ]
type_indicator_sun_permeability = [
                                     {"names":
                                          [SUN_PERMEABILITY, SUN_POWER, TOTAL_POWER]}
                                  ]
type_indicator_social_power_year_grow_rate = [
                                          {"names":
                                          [SALE_POWER_YEAR_GROW_RATE ,
                                           SALE_POWER_YEAR_GROW_RATE,
                                           SALE_POWER]}
                                        ]
type_indicator_social_power_year_average_rate = [
                                          {"names":
                                               [SALE_POWER_YEAR_GROW_RATE,
                                                SALE_POWER_YEAR_GROW_RATE,
                                                SALE_POWER]}
                                        ]
type_indicator_max_load_year_grow_rate = [
                                          {"names":
                                          [MAX_LOAD_YEAR_GROW_RATE,
                                           MAX_LOAD_YEAR_AVERAGE_RATE,
                                           MAX_LOAD]}
                                        ]
type_indicator_max_load_year_average_rate = [
                                          {"names":
                                               [MAX_LOAD_YEAR_GROW_RATE,
                                                MAX_LOAD_YEAR_AVERAGE_RATE,
                                                MAX_LOAD]}
                                        ]
type_indicator_variable_capacity_year_grow_rate = [
                                          {"names":
                                               [VARIABLE_CAPACITY_YEAR_GROW_RATE,
                                                VARIABLE_CAPACITY_YEAR_AVERAGE_RATE,
                                                VARIABLE_CAPACITY,
                                                ]}
                                        ]
type_indicator_variable_capacity_year_average_rate = [
                                          {"names":
                                               [VARIABLE_CAPACITY_YEAR_GROW_RATE,
                                                VARIABLE_CAPACITY_YEAR_AVERAGE_RATE,
                                                VARIABLE_CAPACITY,
                                                ]}
                                        ]
type_indicator_line_length_year_grow_rate = [
                                          {"names":
                                               [LINE_LENGTH_YEAR_GROW_RATE,
                                                LINE_LENGTH_YEAR_AVERAGE_RATE,
                                                LINE_LENGTH]}
                                        ]
type_indicator_line_length_year_average_rate = [
                                          {"names":
                                               [LINE_LENGTH_YEAR_GROW_RATE,
                                                LINE_LENGTH_YEAR_AVERAGE_RATE,
                                                LINE_LENGTH]}
                                        ]
type_indicator_unit_variable_capacity = [
                                          {"names":
                                            [UNIT_VARIABLE_CAPACITY,
                                             MAX_USE_LOAD,
                                             SUM_VARIABLE_CAPACITY]}
                                        ]
type_indicator_unit_line_length = [
                                          {"names":
                                            [UNIT_LINE_LENGTH, MAX_USE_LOAD, SUM_LINE_LENGTH]}
                                        ]

type_indicator_per_house_capacity = [
                                          {"names":
                                            [PER_HOUSE_CAPACITY]}
                                        ]
type_indicator_hundred_average_single_line_length = [
                                          {"names":
                                            [HUNDRED_AVERAGE_SINGLE_LINE_LENGTH,
                                             HUNDRED_LINE_LENGTH_SUM,
                                             HUNDRED_LINE_NUMS]}
                                        ]
type_indicator_thirty_five_average_single_line_length = [
                                          {"names":
                                             [THIRTY_FIVE_AVERAGE_SINGLE_LINE_LENGTH,
                                              THIRTY_FIVE_LINE_LENGTH_SUM,
                                              THIRTY_FIVE_LINE_NUMS]}
                                        ]
type_indicator_net_connectivity = [
                                          {"names":
                                               [NET_CONNECTIVITY,
                                                NET_CONNECTIVITY_LINE_NUMS,
                                                NET_CONNECTIVITY_SUBSTATION_NUMS
                                                ]}
                                        ]

type_indicator_gas_power_rate = [
                                    {"names":
                                        [GAS_POWER_RATE, GAS_POWER, SALE_POWER ]}
                                ]
type_indicator_store_capacity_rate = [
                                    {"names":
                                        [STORE_CAPACITY_RATE, STORE_CAPACITY, NEW_ENERGY_INSTALL]}
                                ]