from app.grid_evaluation.utils.percentage_calculate import PercentageCalculate
from app.grid_evaluation.manager.models import GenerateCapacity
from app.grid_evaluation.utils.install_and_generate_percentage_utils import InstallAndGeneratePercentageUtils
from app.grid_evaluation.utils.indicator_utils import RENEWABLE_POWER_INSTALL, ENV_BENEFIT, NEW_POWER_PERMEABILITY
from app.grid_evaluation.utils.indicator_utils import RENEWABLE_POWER_RATE, WATER_POWER_RATE, WIND_POWER_RATE
from app.grid_evaluation.utils.indicator_utils import SUN_POWER_RATE, BIOMASS_POWER_RATE, CO2_REDUCE, SO2_REDUCE
from app.grid_evaluation.utils.indicator_utils import WIND_PERMEABILITY, SUN_PERMEABILITY
from app.grid_evaluation.utils.indicator_utils import GREEN_CLEAN


class GenerateCapacityManager:

    @staticmethod
    def get_power_list_from_date(year):
        return GenerateCapacity.objects(date=year)

    @staticmethod
    def get_power_list_from_name(name):
        return GenerateCapacity.objects(name=name)

    @staticmethod
    def get_power_list_from_name_down(name):
        return GenerateCapacity.objects(name=name).order_by('-date')

    @staticmethod
    def get_generate_power_object_single_detail(params):
        ret1 = []
        ret2 = []
        for name in params.keys():
            for obj in GenerateCapacityManager.get_power_list_from_name_down(params.get(name)):
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.amount, 2)
                })
            ret1.append({'database': GREEN_CLEAN,
                         'type': RENEWABLE_POWER_INSTALL,
                         'indicator': params.get(name)+'（MW）',
                         'resultList': ret2})
            ret2 = []
        return ret1

    @staticmethod
    def get_generate_power_object_sum_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': RENEWABLE_POWER_RATE,
                     'resultList': GenerateCapacityManager.get_generate_power_sum_percentage()})

        return ret1

    @staticmethod
    def get_generate_power_object_water_percentage():
        params = {'name': '水电发电量'}
        return InstallAndGeneratePercentageUtils.get_generate_power_objects_single_percentage(params)

    @staticmethod
    def get_generate_power_object_water_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': WATER_POWER_RATE,
                     'resultList': GenerateCapacityManager.get_generate_power_object_water_percentage()})

        return ret1

    @staticmethod
    def get_generate_power_object_wind_percentage():
        params = {'name': '风电发电量'}
        return InstallAndGeneratePercentageUtils.get_generate_power_objects_single_percentage(params)

    @staticmethod
    def get_generate_power_object_wind_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': WIND_POWER_RATE,
                     'resultList': GenerateCapacityManager.get_generate_power_object_wind_percentage()})

        return ret1

    @staticmethod
    def get_generate_power_object_sun_percentage():
        params = {'name': '太阳能发电量'}
        return InstallAndGeneratePercentageUtils.get_generate_power_objects_single_percentage(params)

    @staticmethod
    def get_generate_power_object_sun_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': SUN_POWER_RATE,
                     'resultList': GenerateCapacityManager.get_generate_power_object_sun_percentage()})

        return ret1

    @staticmethod
    def get_generate_power_object_biomass_percentage():
        params = {'name': '生物质能发电量'}
        return InstallAndGeneratePercentageUtils.get_generate_power_objects_single_percentage(params)

    @staticmethod
    def get_generate_power_object_biomass_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': BIOMASS_POWER_RATE,
                     'resultList': GenerateCapacityManager.get_generate_power_object_biomass_percentage()})

        return ret1

    @staticmethod
    def power_generate_percentage(social_power, *type_power):
        type_power_sum = 0
        for power in type_power:
            type_power_sum += power
        return round(type_power_sum/social_power, 4)

    @staticmethod
    def get_power_list(year):
        return GenerateCapacity.objects(date=year)

    @staticmethod
    def get_power_sum(date, params):
        sum = 0
        dict_param = {}
        dict_param = params
        object = GenerateCapacity.get_power_list(date)
        for name in dict_param.keys():
            for object1 in object(name=dict_param.get(name)):
                if 'social_power' == name:
                    sum = sum+0
                else: sum += object1.amount
        return sum

    @staticmethod
    def get_generate_power_sum_percentage():
        params = {'water_power': '水电发电量',
                  'wind_power': '风电发电量',
                  'sun_power': '太阳能发电量',
                  'biomass_power': '生物质能发电量',
                  'social_power': '全社会用电量'}
        dict_param = params
        result = []
        social_powers = dict_param.get('social_power')
        for social_power_object in GenerateCapacity.objects(name=social_powers).order_by('-date'):
            social_power = social_power_object.amount
            sum_percentage = PercentageCalculate.power_generate_percentage(social_power, float(
                PercentageCalculate.get_power_sum(social_power_object.date, params)))
            result.append({'time': social_power_object.date,
                           'value': sum_percentage})
        return result

    @staticmethod
    def reduce_co2_sum():
        params = {'water_power': '水电发电量',
                  'wind_power': '风电发电量',
                  'sun_power': '太阳能发电量',
                  'biomass_power': '生物质能发电量',
                 }
        dict_param = params
        result = []
        sun_power = dict_param.get('sun_power')
        for sun_power_object in GenerateCapacityManager.get_power_list_from_name_down(sun_power):
            sum = round(
                    PercentageCalculate.get_power_sum(sun_power_object.date, dict_param) * 365 * 24 * 0.00001 * 0.997, 2)
            result.append({'time': sun_power_object.date,
                           'value': float(format(sum, '.2f'))
                         })
        return result

    @staticmethod
    def get_reduce_co2_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': ENV_BENEFIT,
                     'indicator': CO2_REDUCE,
                     'resultList': GenerateCapacityManager.reduce_co2_sum()})
        return ret1

    @staticmethod
    def reduce_so2_sum():
        params = {'water_power': '水电发电量',
                  'wind_power': '风电发电量',
                  'sun_power': '太阳能发电量',
                  'biomass_power': '生物质能发电量',
                  }
        dict_param = params
        result = []
        sun_power = dict_param.get('sun_power')
        for sun_power_object in GenerateCapacityManager.get_power_list_from_name_down(sun_power):
            sum = round(
                PercentageCalculate.get_power_sum(sun_power_object.date, dict_param) * 365 * 24 * 0.00001 * 0.03, 2)
            result.append({'time': sun_power_object.date,
                           'value': float(format(sum, '.2f'))
                          })
        return result

    @staticmethod
    def get_reduce_so2_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': ENV_BENEFIT,
                     'indicator': SO2_REDUCE,
                     'resultList': GenerateCapacityManager.reduce_so2_sum()})

        return ret1

    @staticmethod
    def get_wind_permeability_percentage():
        params = {'name': '风电发电量'}
        return InstallAndGeneratePercentageUtils.get_single_permeability_percentage(params)

    @staticmethod
    def get_wind_permeability_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': NEW_POWER_PERMEABILITY,
                     'indicator': WIND_PERMEABILITY,
                     'resultList': GenerateCapacityManager.get_wind_permeability_percentage()})

        return ret1

    @staticmethod
    def get_sun_permeability_percentage():
        params = {'name': '太阳能发电量'}
        return InstallAndGeneratePercentageUtils.get_single_permeability_percentage(params)

    @staticmethod
    def get_sun_permeability_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': NEW_POWER_PERMEABILITY,
                     'indicator': SUN_PERMEABILITY,
                     'resultList': GenerateCapacityManager.get_sun_permeability_percentage()})
        return ret1

    @staticmethod
    def get_single_permeability_detail(params):
        ret1 = []
        ret2 = []
        for name in params.keys():
            for obj in GenerateCapacity.objects(name=params.get(name)).order_by('-date'):
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.amount, 2)
                })
            ret1.append({'database': GREEN_CLEAN,
                         'type': NEW_POWER_PERMEABILITY,
                         'indicator': params.get(name)+'（MW）',
                         'resultList': ret2})
            ret2 = []
        return ret1


if __name__ == '__main__':
    pass
