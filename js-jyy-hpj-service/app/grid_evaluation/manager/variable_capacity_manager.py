from app.grid_evaluation.manager.models import VariableCapacity
from app.grid_evaluation.utils.indicator_utils import VARIABLE_CAPACITY, VARIABLE_CAPACITY_YEAR_GROW_RATE
from app.grid_evaluation.utils.indicator_utils import VARIABLE_CAPACITY_YEAR_AVERAGE_RATE, NET_DEVELOP_SPEED
from app.grid_evaluation.utils.indicator_utils import FLEXIBLE_INTELLIGENT


class VariableCapacityManager:
    @staticmethod
    def get_variable_capacity_list_from_name(name):
        return VariableCapacity.objects(name=name).order_by('date')

    @staticmethod
    def get_variable_capacity_list_from_name_down(name):
        return VariableCapacity.objects(name=name).order_by('-date')

    @staticmethod
    def get_variable_capacity_year_grow_rate(name):
        object1 = VariableCapacityManager.get_variable_capacity_list_from_name_down(name)
        count = object1.count(name) - 1
        list_year_rate = []
        a = 0
        while a < count:
            rate = round((object1[a].amount - object1[a + 1].amount) / object1[a + 1].amount, 4)*100
            list_year_rate.append(
                {'time': object1[a].date,
                 'value': float(format(rate, '.2f'))}
            )
            a += 1
        return list_year_rate

    @staticmethod
    def get_variable_capacity_average_year_grow_rate(name):
        object1 = VariableCapacityManager.get_variable_capacity_list_from_name_down(name)
        count = object1.count(name)
        list_average_rate = []
        start_power = object1[count - 1].amount
        final_power = object1[0].amount
        average_rate = round(pow(final_power / start_power, 1 / count) - 1, 4)*100
        for obj in object1:
            list_average_rate.append(
                {'time': obj.date,
                 'value': float(format(average_rate, '.2f'))}
            )
        return list_average_rate

    @staticmethod
    def get_variable_capacity_single_from_name():
        ret1 = []
        ret2 = []
        params = {'name1': '交流10kV',
                  'name2': '交流20kV',
                  'name3': '交流35kV',
                  'name4': '交流66kV',
                  'name5': '交流110kV',
                  'name6': '交流220kV',
                  'name7': '交流330kV',
                  'name8': '交流500kV',
                  'name9': '交流600V',
                  'name10': '交流1000V（含1140V）'
                  }
        for name in params.keys():
            for obj in VariableCapacityManager.get_variable_capacity_list_from_name_down(params.get(name)):
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.amount, 2)
                })
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_DEVELOP_SPEED,
                         'indicator': params.get(name) + '-' + VARIABLE_CAPACITY,
                         'resultList': ret2})
            ret2 = []

        return ret1

    @staticmethod
    def get_variable_capacity_year_grow_from_name():
        ret1 = []
        ret2 = []
        params ={'name1': '交流10kV',
                 'name2': '交流20kV',
                 'name3': '交流35kV',
                 'name4': '交流66kV',
                 'name5': '交流110kV',
                 'name6': '交流220kV',
                 'name7': '交流330kV',
                 'name8': '交流500kV',
                 'name9': '交流600V',
                 'name10': '交流1000V（含1140V）'
                 }

        for name in params.keys():

            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_DEVELOP_SPEED,
                         'indicator': VARIABLE_CAPACITY_YEAR_GROW_RATE + '-' + params.get(name),
                         'resultList': VariableCapacityManager.get_variable_capacity_year_grow_rate(params.get(name))})
        ret2.append(ret1)
        return ret2

    @staticmethod
    def get_variable_capacity_average_year_grow_from_name():
        ret1 = []
        ret2 = []
        params = {'name1': '交流10kV',
                  'name2': '交流20kV',
                  'name3': '交流35kV',
                  'name4': '交流66kV',
                  'name5': '交流110kV',
                  'name6': '交流220kV',
                  'name7': '交流330kV',
                  'name8': '交流500kV',
                  'name9': '交流600V',
                  'name10': '交流1000V（含1140V）'
                  }

        for name in params.keys():
            ret1.append({'database': FLEXIBLE_INTELLIGENT,
                         'type': NET_DEVELOP_SPEED,
                         'indicator': VARIABLE_CAPACITY_YEAR_AVERAGE_RATE + '-' + params.get(name),
                         'resultList': VariableCapacityManager.get_variable_capacity_average_year_grow_rate(params.get(name))})
        ret2.append(ret1)
        return ret2


if __name__=='__main__':
   pass