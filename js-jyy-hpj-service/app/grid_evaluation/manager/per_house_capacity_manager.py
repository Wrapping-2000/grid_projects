from app.grid_evaluation.utils.percentage_calculate import PercentageCalculate
from app.grid_evaluation.manager.models import HouseNumber
from app.grid_evaluation.manager.models import VariableCapacity
from app.grid_evaluation.utils.indicator_utils import PER_HOUSE_CAPACITY, NET_SIZE
from app.grid_evaluation.utils.indicator_utils import FLEXIBLE_INTELLIGENT


class PerHouseCapacityManager:

    @staticmethod
    def get_house_number_list_from_name(date):
        return HouseNumber.objects(date=date)[0]

    @staticmethod
    def get_variable_capacity_list_from_name(name):
        return VariableCapacity.objects(name=name).order_by('date')

    @staticmethod
    def get_variable_capacity_list_from_name_down(name):
        return VariableCapacity.objects(name=name).order_by('-date')

    @staticmethod
    def get_variable_capacity_list_from_date(date):
        return VariableCapacity.objects(date=date).order_by('date')

    @staticmethod
    def get_variable_capacity_year_grow_rate(name):
        object1 = PerHouseCapacityManager.get_variable_capacity_list_from_name(name)
        count = object1.count(name)
        list_year_rate = []
        while count > 1:
            rate = round((object1[count-1].amount-object1[count-2].amount)/object1[count-2].amount, 2)*100
            list_year_rate.append(
                {object1[count-1].date: float(format(rate, '.2f'))}
            )
            count -= 1
        return list_year_rate

    @staticmethod
    def get_variable_capacity_average_year_grow_rate(name):
        object1 = PerHouseCapacityManager.get_variable_capacity_list_from_name(name)
        count = object1.count(name)
        list_average_rate = []
        start_power = object1[0].amount
        final_power = object1[count-1].amount
        average_rate = round(pow(final_power / start_power, 1 / count)-1, 4)*100
        while count > 1:
            list_average_rate.append(
                {object1[count-1].date: float(format(average_rate, '.2f'))}
            )
            count -= 1
        return list_average_rate

    @staticmethod
    def get_sum_variable_capacity(date):
        objects = PerHouseCapacityManager.get_variable_capacity_list_from_date(date)
        sum = 0
        for obj in objects:
            if '交流10kV' == obj.name:
                sum += obj.amount
            elif '交流20kV' == obj.name:
                sum += obj.amount
            elif '交流35kV' == obj.name:
                sum += obj.amount
            elif '交流66kV' == obj.name:
                sum += obj.amount
            elif '交流110kV' == obj.name:
                sum += obj.amount
            elif '交流220kV' == obj.name:
                sum += obj.amount
            elif '交流330kV' == obj.name:
                sum += obj.amount
            elif '交流500kV' == obj.name:
                sum += obj.amount

        return sum

    @staticmethod
    def get_average_house():
        ret1 = []
        ret2 = []
        params = {'date1': '2021年', 'date2': '2020年', 'date3': '2019年'}
        for param in params:
            sum = PerHouseCapacityManager.get_sum_variable_capacity(params.get(param))
            house = PerHouseCapacityManager.get_house_number_list_from_name(params.get(param))
            ret2.append({
                'time': params.get(param),
                'value': round(sum / house.low_level, 2)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_SIZE,
                     'indicator': PER_HOUSE_CAPACITY,
                     'resultList': ret2})
        ret2 = []
        return ret1


if __name__=='__main__':
    params = {'date1': '2019', 'date2': '2020', 'date3': '2021'}
    print(VariableCapacity.get_average_house(params))






