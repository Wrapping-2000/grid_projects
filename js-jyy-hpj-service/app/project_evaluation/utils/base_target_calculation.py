from app.project_evaluation.utils import format_datetime, has_all_datetime, keep_2f
from app.project_evaluation.manager import ProjectComponentManager
from app.project_evaluation.manager import ProjectDetailManager
from app.project_evaluation.manager.models import Target


class BaseTargetCalculation:

    def __init__(self, wbs_code):
        self.wbs_code = wbs_code
        self.project_detail = ProjectDetailManager.get_project_detail_dict(wbs_code)

    def get_year_increase_value(self, year_value_list):
        """

        :param year_value_list: [{'year': '2018', 'value': 1},
        {'year': '2019', 'value': 2},
        {'year': '2020', 'value': 3}]
        :return:
        """
        result = []
        if not isinstance(year_value_list, list) or not len(year_value_list) > 1:
            return result
        sorted_year_value_list = sorted(year_value_list, key=lambda i: i["year"])
        for i in range(1, len(sorted_year_value_list)):
            previous = sorted_year_value_list[i - 1]
            current = sorted_year_value_list[i]

            result.append({"year": current['year'], "value": float(current["value"]) - float(previous["value"])})

        return result

    def time_difference_target(self, name, start_time, end_time):
        data_raw = {}
        data_raw_cal = {}
        target = Target(
            name=name,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )

        for name_raw in [start_time,
                         end_time]:
            data_raw[name_raw] = format_datetime(self.project_detail.get(name_raw))
            data_raw_cal[name_raw] = self.project_detail.get(name_raw)

        if has_all_datetime(data_raw_cal):
            target.value = (data_raw_cal[start_time] - data_raw_cal[end_time]).days

            return target

    def parse_continuous_component_data_cal(self, target, data_cal, func):
        for name, data_cal_raw in data_cal.items():
            for year, value_map in data_cal_raw.items():
                target.component_name = name
                target.value = func(value_map)
                target.year = year

                yield target

    def component_count_target(self, target_name, index_name):
        data_raw = ProjectComponentManager.get_component_target(self.wbs_code, (index_name,))
        target = Target(
            name=target_name,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        data_cal = self.parse_component_continuous(data_raw)
        yield from self.parse_continuous_component_data_cal(target, data_cal, lambda x: x[index_name])

    def component_single_target(self, target_name, index_name):
        data_raw = {}
        target = Target(
            name=target_name,
            wbs_code=self.wbs_code,
            data_raw=data_raw
        )
        for name_raw in [index_name]:
            data_raw[name_raw] = self.project_detail.get(name_raw)

        target.value = keep_2f(data_raw[index_name])
        yield target

    def parse_component_continuous(self, data_raw):
        result = {}

        for target_name, value in data_raw.items():
            if isinstance(value, list):
                for component in value:
                    if "name" in component:
                        name = component["name"]
                        data = component["data"]
                        if isinstance(data, list):
                            component_data_cal = result.setdefault(name, {})
                            for year_data in data:
                                r = component_data_cal.setdefault(year_data["year"], {})
                                r[target_name] = year_data["value"]

        for target_name, value in data_raw.items():
            if isinstance(value, list):
                for component in value:
                    if "name" in component:
                        name = component["name"]
                        data = component["data"]
                        if not isinstance(data, list):
                            if name in result:
                                for year in result[name]:
                                    result[name][year][target_name] = data

        for target_name, value in data_raw.items():
            if not isinstance(value, list):
                for component_name, year_data in result.items():
                    for year, value_map in year_data.items():
                        value_map[target_name] = value

        return result

    def parse_continuous(self, data_raw):
        calculation_data = {}
        for target_name, value in data_raw.items():
            if isinstance(value, list):
                for year_data in value:
                    year = year_data["year"]
                    value = year_data["value"]
                    calculation_data.setdefault(year, {})[target_name] = value

        for target_name, value in data_raw.items():
            if not isinstance(value, list):
                for year, v in calculation_data.items():
                    v[target_name] = value

        return calculation_data

    def parse_continuous_data_cal(self, target, data_cal, func):
        for year, value_map in data_cal.items():
            target.year = year
            target.value = func(value_map)

            yield target
