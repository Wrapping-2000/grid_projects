from app.grid_evaluation.manager.models import VoltageLevel
from app.grid_evaluation.utils.indicator_utils import LINE_LENGTH, LINE_LENGTH_YEAR_GROW_RATE
from app.grid_evaluation.utils.indicator_utils import LINE_LENGTH_YEAR_AVERAGE_RATE, THIRTY_FIVE_LINE_LENGTH_SUM
from app.grid_evaluation.utils.indicator_utils import THIRTY_FIVE_LINE_NUMS, THIRTY_FIVE_AVERAGE_SINGLE_LINE_LENGTH
from app.grid_evaluation.utils.indicator_utils import HUNDRED_LINE_LENGTH_SUM, HUNDRED_LINE_NUMS
from app.grid_evaluation.utils.indicator_utils import HUNDRED_AVERAGE_SINGLE_LINE_LENGTH, NET_CONNECTIVITY_LINE_NUMS
from app.grid_evaluation.utils.indicator_utils import NET_CONNECTIVITY_SUBSTATION_NUMS, NET_CONNECTIVITY
from app.grid_evaluation.utils.indicator_utils import NET_DEVELOP_SPEED, NET_FRAMEWORK
from app.grid_evaluation.utils.indicator_utils import FLEXIBLE_INTELLIGENT


class VoltageLevelManager:

    @staticmethod
    def get_voltage_level_list_from_name(name):
        return VoltageLevel.objects(name=name).order_by('date')

    @staticmethod
    def get_voltage_level_list_from_name_down(name):
        return VoltageLevel.objects(name=name).order_by('-date')

    @staticmethod
    def get_length_year_grow_rate(name):
        object1 = VoltageLevelManager.get_voltage_level_list_from_name_down(name)
        count = object1.count(name)-1
        list_year_rate = []
        a = 0
        while a < count:
            rate = round((object1[a].length - object1[a + 1].length) / object1[a + 1].length, 4) * 100
            list_year_rate.append(
                {'time': object1[a].date,
                 'value': float(format(rate, '.2f'))}
                 )
            a += 1
        return list_year_rate

    @staticmethod
    def get_length_average_year_grow_rate(name):
        object1 = VoltageLevelManager.get_voltage_level_list_from_name_down(name)
        count = object1.count(name)
        list_average_rate = []
        start_power = object1[count-1].length
        final_power = object1[0].length
        average_rate = round(pow(final_power / start_power, 1 / count)-1, 4)*100
        for obj in object1:
            list_average_rate.append(
                {'time': obj.date,
                 'value': float(format(average_rate, '.2f'))}
                )
        return list_average_rate

    @staticmethod
    def get_length_single_from_name():
        ret1 = []
        ret2 = []
        params = {'name1': '交流35kV', 'name2': '交流110kV', 'name3': '交流220kV', 'name4': '交流500kV'}
        for name in params.keys():
            for obj in VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name)):
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.length, 2)
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_DEVELOP_SPEED,
                         'indicator': LINE_LENGTH+'-' + params.get(name),
                         'resultList': ret2})
            ret2 = []

        return ret1

    @staticmethod
    def get_length_year_grow_from_name():
        ret1 = []
        params = {'name1': '交流35kV', 'name2': '交流110kV', 'name3': '交流220kV', 'name4': '交流500kV'}
        for name in params.keys():
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_DEVELOP_SPEED,
                         'indicator': LINE_LENGTH_YEAR_GROW_RATE + '-' + params.get(name),
                         'resultList': VoltageLevelManager.get_length_year_grow_rate(params.get(name))})

        return ret1

    @staticmethod
    def get_length_average_year_grow_from_name():
        ret1 = []
        params = {'name1': '交流35kV', 'name2': '交流110kV', 'name3': '交流220kV', 'name4': '交流500kV'}
        for name in params.keys():
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_DEVELOP_SPEED,
                         'indicator': LINE_LENGTH_YEAR_AVERAGE_RATE + '-' + params.get(name),
                         'resultList': VoltageLevelManager.get_length_average_year_grow_rate(params.get(name))})
        return ret1

    @staticmethod
    def get_35kv_length():
        ret1 = []
        ret2 = []
        params = {'name1': '交流35kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.length, 2)
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_FRAMEWORK,
                         'indicator': THIRTY_FIVE_LINE_LENGTH_SUM,
                         'resultList': ret2})
            ret2 = []
        return ret1

    @staticmethod
    def get_35kv_nums():
        ret1 = []
        ret2 = []
        params = {'name1': '交流35kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': obj.line_num
                })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_FRAMEWORK,
                     'indicator': THIRTY_FIVE_LINE_NUMS,
                     'resultList': ret2})
        ret2 = []

        return ret1

    @staticmethod
    def get_35kv_average_single_length():
        ret1 = []
        ret2 = []
        params = {'name1': '交流35kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.length/obj.line_num, 2)
                })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_FRAMEWORK,
                     'indicator': THIRTY_FIVE_AVERAGE_SINGLE_LINE_LENGTH,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_110kv_length():
        ret1 = []
        ret2 = []
        params = {'name1': '交流110kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.length, 2)
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_FRAMEWORK,
                         'indicator': HUNDRED_LINE_LENGTH_SUM,
                         'resultList': ret2})
            ret2 = []
        return ret1

    @staticmethod
    def get_110kv_nums():
        ret1 = []
        ret2 = []
        params = {'name1': '交流110kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': obj.line_num
                })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_FRAMEWORK,
                     'indicator': HUNDRED_LINE_NUMS,
                     'resultList': ret2})

        return ret1

    @staticmethod
    def get_110kv_average_single_length():
        ret1 = []
        ret2 = []
        params = {'name1': '交流110kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.length / obj.line_num, 2)
                })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_FRAMEWORK,
                     'indicator': HUNDRED_AVERAGE_SINGLE_LINE_LENGTH,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_connectivity_line_nums():
        ret1 = []
        ret2 = []
        params = {'name1': '交流110kV', 'name2': '交流220kV', 'name3': '交流500kV', 'name4': '交流750kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': obj.line_num
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_FRAMEWORK,
                         'indicator': NET_CONNECTIVITY_LINE_NUMS + '-' + params.get(name),
                         'resultList': ret2})
            ret2 = []

        return ret1

    @staticmethod
    def get_connectivity_substation_nums():
        ret1 = []
        ret2 = []
        params = {'name1': '交流110kV', 'name2': '交流220kV', 'name3': '交流500kV', 'name4': '交流750kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:
                ret2.append({
                    'time': obj.date,
                    'value': obj.substation_num
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_FRAMEWORK,
                         'indicator': NET_CONNECTIVITY_SUBSTATION_NUMS + '-' + params.get(name),
                         'resultList': ret2})
            ret2 = []

        return ret1

    @staticmethod
    def get_connectivity():
        ret1 = []
        ret2 = []
        params = {'name1': '交流110kV', 'name2': '交流220kV', 'name3': '交流500kV', 'name4': '交流750kV'}
        for name in params.keys():
            objects = VoltageLevelManager.get_voltage_level_list_from_name_down(params.get(name))
            for obj in objects:

                ret2.append({
                    'time': obj.date,
                    'value': float(format(round(2*obj.line_num / obj.substation_num, 2), '.2f'))
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_FRAMEWORK,
                         'indicator': NET_CONNECTIVITY + '-' + params.get(name),
                         'resultList': ret2})
            ret2 = []

        return ret1


if __name__ == '__main__':
    pass
