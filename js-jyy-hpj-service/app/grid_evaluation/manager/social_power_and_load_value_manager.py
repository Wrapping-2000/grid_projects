from math import pow
from app.grid_evaluation.manager.models import SocialPowerAndLoadValue
from app.grid_evaluation.utils.percentage_calculate import PercentageCalculate
from app.grid_evaluation.manager.voltage_level_manager import VoltageLevelManager
from app.grid_evaluation.manager.variable_capacity_manager import VariableCapacityManager
from app.grid_evaluation.utils.indicator_utils import SALE_POWER_YEAR_GROW_RATE, SALE_POWER_YEAR_AVERAGE_RATE
from app.grid_evaluation.utils.indicator_utils import MAX_LOAD, MAX_LOAD_YEAR_GROW_RATE, MAX_LOAD_YEAR_AVERAGE_RATE
from app.grid_evaluation.utils.indicator_utils import SALE_POWER, NET_DEVELOP_SPEED, GAS_POWER, GAS_POWER_RATE
from app.grid_evaluation.utils.indicator_utils import STORE_CAPACITY, NEW_ENERGY_INSTALL, STORE_CAPACITY_RATE
from app.grid_evaluation.utils.indicator_utils import NET_ADJUST_ABILITY, MAX_USE_LOAD, SUM_VARIABLE_CAPACITY
from app.grid_evaluation.utils.indicator_utils import UNIT_VARIABLE_CAPACITY, SUM_LINE_LENGTH, UNIT_LINE_LENGTH
from app.grid_evaluation.utils.indicator_utils import NET_SIZE
from app.grid_evaluation.utils.indicator_utils import FLEXIBLE_INTELLIGENT


class SocialPowerAndLoadValueManager:

    @staticmethod
    def get_social_power_list_from_name(name):
        return SocialPowerAndLoadValue.objects(name=name).order_by('date')

    @staticmethod
    def get_social_power_list_from_name_down(name):
        return SocialPowerAndLoadValue.objects(name=name).order_by('-date')

    @staticmethod
    def get_social_power_list_from_date(date):
        return SocialPowerAndLoadValue.objects(date=date).order_by('date')

    @staticmethod
    def get_social_power_list_from_date_down(date):
        return SocialPowerAndLoadValue.objects(date=date).order_by('-date')

    @staticmethod
    def get_social_power_list_from_date_name(name, date):
        return SocialPowerAndLoadValue.objects(name=name, date=date).order_by('-date')

    @staticmethod
    def get_sale_power_year_grow_rate(name):
        object1 = SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(name)
        count = object1.count(name)-1
        list_year_rate = []
        a = 0
        while a < count:
            rate = round((object1[a].amount - object1[a + 1].amount) / object1[a + 1].amount, 4) * 100
            list_year_rate.append(
                {'time': object1[a].date,
                 'value': float(format(rate, '.2f'))}
            )
            a += 1

        return list_year_rate

    @staticmethod
    def get_sale_power_average_year_grow_rate(name):
        object1 = SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(name)
        count = object1.count(name)
        list_average_rate = []
        start_power = object1[count - 1].amount
        final_power = object1[0].amount
        average_rate = round(pow(final_power / start_power, 1 / count) - 1, 4)*100
        for obj in object1:
            list_average_rate.append(
                {'time': obj.date,
                 'value': float(format(average_rate, '.2f'))})
        return list_average_rate

    @staticmethod
    def get_load_value_single_from_name():

        ret1 = []
        ret2 = []
        name = '统调最大负荷'
        for obj in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(name):
            ret2.append({
                'time': obj.date,
                'value': round(obj.amount, 2)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_DEVELOP_SPEED,
                     'indicator': MAX_LOAD,
                     'resultList': ret2})
        ret2 = []

        return ret1

    @staticmethod
    def get_load_value_year_grow_rate_from_name():

        ret1 = []
        name = '统调最大负荷'
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_DEVELOP_SPEED,
                     'indicator': MAX_LOAD_YEAR_GROW_RATE,
                     'resultList': SocialPowerAndLoadValueManager.get_sale_power_year_grow_rate(name)})

        return ret1

    @staticmethod
    def get_load_value_average_grow_rate_from_name():

        ret1 = []
        name = '统调最大负荷'
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_DEVELOP_SPEED,
                     'indicator': MAX_LOAD_YEAR_AVERAGE_RATE,
                     'resultList': SocialPowerAndLoadValueManager.get_sale_power_average_year_grow_rate(name)})

        return ret1

    @staticmethod
    def get_sale_power_single_from_name():

        ret1 = []
        ret2 = []
        name = '全社会售电量'
        for obj in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(name):
            ret2.append({
                'time': obj.date,
                'value': round(obj.amount, 2)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_DEVELOP_SPEED,
                     'indicator': SALE_POWER,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_sale_power_year_grow_rate_from_name():

        ret1 = []
        name = '全社会售电量'
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_DEVELOP_SPEED,
                     'indicator': SALE_POWER_YEAR_GROW_RATE,
                     'resultList': SocialPowerAndLoadValueManager.get_sale_power_year_grow_rate(name)})

        return ret1

    @staticmethod
    def get_sale_power_average_grow_rate_from_name():

        ret1 = []
        name = '全社会售电量'
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_DEVELOP_SPEED,
                     'indicator': SALE_POWER_YEAR_AVERAGE_RATE,
                     'resultList': SocialPowerAndLoadValueManager.get_sale_power_average_year_grow_rate(name)})
        return ret1

    @staticmethod
    def get_flexible_gas_power_single_detail():
        ret1 = []
        ret2 = []
        params = {'gas_power': '省内天然气电站发电量'}
        total_install1 = params.get('gas_power')
        for total_install_object in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(total_install1):
            objects = SocialPowerAndLoadValueManager.get_social_power_list_from_date_down(total_install_object.date)
            for obj in objects:
                if '省内天然气电站发电量' == obj.name:
                    ret2.append({
                        'time': obj.date,
                        'value': round(obj.amount,2)
                    })
        ret1.append({'database': '灵活智能',
                     'type': NET_ADJUST_ABILITY,
                     'indicator': GAS_POWER,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_flexible_sale_power_single_detail():
        ret1 = []
        ret2 = []
        params = {'sale_power': '全社会售电量'}
        total_install2 = params.get('sale_power')
        for total_install_object in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(total_install2):
            ret2.append({
                'time': total_install_object.date,
                'value': round(total_install_object.amount,2)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_ADJUST_ABILITY,
                     'indicator': SALE_POWER,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_flexible_gas_power_detail():
        ret1 = []
        ret2 = []
        params = {'sale_power': '全社会售电量', 'gas_power': '省内天然气电站发电量'}
        total_install = params.get('sale_power')
        for total_install_object in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(total_install):
            objects = SocialPowerAndLoadValueManager.get_social_power_list_from_date_down(total_install_object.date)
            total_install_amount = total_install_object.amount
            for obj in objects:
                    if '省内天然气电站发电量' == obj.name:
                        natural_power = obj.amount * 1000 * 365 * 24
                        ret2.append({
                            'time': obj.date,
                            'value': PercentageCalculate.power_generate_percentage(total_install_amount, natural_power)
                        })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_ADJUST_ABILITY,
                     'indicator': GAS_POWER_RATE,
                     'resultList': ret2})

        return ret1

    @staticmethod
    def get_store_capacity_single_detail():
        ret1 = []
        ret2 = []
        params = {'store_capacity': '储能容量'}
        new_energy_capacity1 = params.get('store_capacity')
        for new_energy_capacity_object in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(new_energy_capacity1):
            objects = SocialPowerAndLoadValueManager.get_social_power_list_from_date_down(new_energy_capacity_object.date)
            for obj in objects:
                if '储能容量' == obj.name:
                    ret2.append({
                        'time': obj.date,
                        'value': round(obj.amount, 2)
                    })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_ADJUST_ABILITY,
                     'indicator': STORE_CAPACITY,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_new_energy_capacity_single_detail():
        ret1 = []
        ret2 = []
        params = {'new_energy_capacity': '新能源装机容量'}
        new_energy_capacity2 = params.get('new_energy_capacity')
        for new_energy_capacity_object in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(new_energy_capacity2):
            ret2.append({
                'time': new_energy_capacity_object.date,
                'value': round(new_energy_capacity_object.amount,2)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_ADJUST_ABILITY,
                     'indicator': NEW_ENERGY_INSTALL,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def get_new_energy_capacity_rate_detail():
        ret1 = []
        ret2 = []
        params = {'new_energy_capacity': '新能源装机容量'}
        new_energy_capacity = params.get('new_energy_capacity')
        for new_energy_capacity_object in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(new_energy_capacity):
            objects = SocialPowerAndLoadValueManager.get_social_power_list_from_date_down(new_energy_capacity_object.date)
            new_energy_capacity_amount = new_energy_capacity_object.amount
            for obj in objects:
                if '储能容量' == obj.name:
                    store_capacity = obj.amount
                    ret2.append({
                        'time': obj.date,
                        'value': PercentageCalculate.power_generate_percentage(new_energy_capacity_amount,
                                                                               store_capacity)
                    })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_ADJUST_ABILITY,
                     'indicator': STORE_CAPACITY_RATE,
                     'resultList': ret2})

        return ret1

    @staticmethod
    def unit_high_load_single():
        ret1 = []
        ret2 = []
        name = '统调最大负荷'
        for obj in SocialPowerAndLoadValueManager.get_social_power_list_from_name_down(name):
            ret2.append({
                'time': obj.date,
                'value': round(obj.amount, 2)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_SIZE,
                     'indicator': MAX_USE_LOAD,
                     'resultList': ret2})

        return ret1

    @staticmethod
    def unit_variable_capacity_single():
        ret1 = []
        ret2 = []
        params = {'variable_sum': '变电容量之和'}
        for param in params:
            if '变电容量之和' == params.get(param):
                variable_capacitys = VariableCapacityManager.get_variable_capacity_list_from_name_down('交流220kV')
                for variable_capacity in variable_capacitys:
                    date = str(variable_capacity.date)
                    ret2.append({
                        'time': date,
                        'value': variable_capacity.amount
                    })
                ret1.append({'database': FLEXIBLE_INTELLIGENT,
                             'type': NET_SIZE,
                             'indicator': SUM_VARIABLE_CAPACITY,
                             'resultList': ret2})
        return ret1

    @staticmethod
    def unit_variable_load():
        ret1 = []
        ret2 = []
        variable_capacitys = VariableCapacityManager.get_variable_capacity_list_from_name_down('交流220kV')
        for variable_capacity in variable_capacitys:
            date = str(variable_capacity.date)
            load_value = SocialPowerAndLoadValueManager.get_social_power_list_from_date_name('统调最大负荷', date)[0].amount
            ret2.append({
                'time': date,
                'value': PercentageCalculate.power_generate_percentage(variable_capacity.amount, load_value * 1000)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_SIZE,
                     'indicator': UNIT_VARIABLE_CAPACITY,
                     'resultList': ret2})
        return ret1

    @staticmethod
    def unit_length_load_high_load():
        ret1 = []
        ret2 = []
        params = {'high_load': '最高用电负荷'}
        for param in params:
            if '最高用电负荷' == params.get(param):
                voltage_levels = VoltageLevelManager.get_voltage_level_list_from_name_down('交流220kV')
                for voltage_level in voltage_levels:
                    date = str(voltage_level.date)
                    load_value = SocialPowerAndLoadValueManager.get_social_power_list_from_date_name('统调最大负荷', date)[0].amount
                    ret2.append({
                        'time': date,
                        'value': load_value
                    })
                ret1.append({'database': FLEXIBLE_INTELLIGENT,
                             'type': NET_SIZE,
                             'indicator': MAX_USE_LOAD,
                             'resultList': ret2})
        return ret1

    @staticmethod
    def unit_length_load_length_sum():
        ret1 = []
        ret2 = []
        params = {'variable_sum': '线路长度之和'}
        for param in params:
            if '线路长度之和' == params.get(param):
                ret2 = []
                voltage_levels = VoltageLevelManager.get_voltage_level_list_from_name_down('交流220kV')
                for voltage_level in voltage_levels:
                    date = str(voltage_level.date)
                    ret2.append({
                        'time': date,
                        'value': round(voltage_level.length,2)
                    })
                ret1.append({'database': FLEXIBLE_INTELLIGENT,
                             'type': NET_SIZE,
                             'indicator': SUM_LINE_LENGTH,
                             'resultList': ret2})
        return ret1

    @staticmethod
    def unit_length_load():
        ret1 = []
        ret2 = []
        voltage_levels = VoltageLevelManager.get_voltage_level_list_from_name_down('交流220kV')
        for voltage_level in voltage_levels:
            date = str(voltage_level.date)
            load_value = SocialPowerAndLoadValueManager.get_social_power_list_from_date_name('统调最大负荷', date)[0].amount
            ret2.append({
                'time': date,
                'value': PercentageCalculate.power_generate_percentage(voltage_level.length, load_value)
            })
        ret1.append({'database': FLEXIBLE_INTELLIGENT,
                     'type': NET_SIZE,
                     'indicator': UNIT_LINE_LENGTH,
                     'resultList': ret2})
        return ret1


if __name__ == '__main__':
    pass