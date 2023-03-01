from app.grid_evaluation.utils.percentage_calculate import PercentageCalculate
from app.grid_evaluation.manager.models import InstallCapacity
from app.grid_evaluation.utils.install_and_generate_percentage_utils import InstallAndGeneratePercentageUtils
from app.grid_evaluation.utils.indicator_utils import RENEWABLE_INSTALL_RATE, WATER_INSTALL_RATE, WIND_INSTALL_RATE
from app.grid_evaluation.utils.indicator_utils import SUN_INSTALL_RATE, BIOMASS_INSTALL_RATE, RENEWABLE_POWER_INSTALL
from app.grid_evaluation.utils.indicator_utils import GREEN_CLEAN


class InstallCapacityManager:

    @staticmethod
    def get_install_list_from_date(year):
        return InstallCapacity.objects(date=year)

    @staticmethod
    def get_install_list_from_name(name):
        return InstallCapacity.objects(name=name).order_by('-date')

    @staticmethod
    def get_install_capacity_sum_percentage():
        params = {'water_install': '水电装机容量',
                  'wind_install': '风电装机容量',
                  'sun_install': '太阳能装机容量',
                  'biomass_install': '生物质能装机容量',
                  'total_install': '并网发电装机容量'}
        dict_param = {}
        dict_param = params
        result = []
        total_install = dict_param.get('total_install')
        for total_install_object in InstallCapacityManager.get_install_list_from_name(total_install):
            total_install = total_install_object.amount
            sum_percentage = PercentageCalculate.power_generate_percentage(total_install, float(
                PercentageCalculate.get_install_sum(total_install_object.date, params)))
            result.append({'time': total_install_object.date,
                           'value': sum_percentage})
        return result

    @staticmethod
    def get_install_capacity_object_single_detail(params):
        ret1 = []
        ret2 = []

        for name in params.keys():
            for obj in InstallCapacityManager.get_install_list_from_name(params.get(name)):
                ret2.append({
                    'time': obj.date,
                    'value': round(obj.amount, 2)
                })
            ret1.append({'database': GREEN_CLEAN,
                         'type': RENEWABLE_POWER_INSTALL,
                         'indicator': params.get(name) + 'MW',
                         'name': params.get(name),
                         'resultList': ret2})
            ret2 = []
        return ret1

    @staticmethod
    def get_install_capacity_object_sum_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': RENEWABLE_INSTALL_RATE,
                     'resultList': InstallCapacityManager.get_install_capacity_sum_percentage()})

        return ret1

    @staticmethod
    def get_install_capacity_object_water_percentage():
        params = {'name': '水电装机容量'}
        return InstallAndGeneratePercentageUtils.get_install_capacity_object_single_percentage(params)

    @staticmethod
    def get_install_capacity_object_water_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': WATER_INSTALL_RATE,
                     'resultList': InstallCapacityManager.get_install_capacity_object_water_percentage()})

        return ret1

    @staticmethod
    def get_install_capacity_object_wind_percentage():
        params = {'name': '风电装机容量'}
        return InstallAndGeneratePercentageUtils.get_install_capacity_object_single_percentage(params)

    @staticmethod
    def get_install_capacity_object_wind_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator':  WIND_INSTALL_RATE,
                     'resultList': InstallCapacityManager.get_install_capacity_object_wind_percentage()})

        return ret1

    @staticmethod
    def get_install_capacity_object_sun_percentage():
        params = {'name': '太阳能装机容量'}
        return InstallAndGeneratePercentageUtils.get_install_capacity_object_single_percentage(params)

    @staticmethod
    def get_install_capacity_object_sun_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': SUN_INSTALL_RATE,
                     'resultList': InstallCapacityManager.get_install_capacity_object_sun_percentage()})

        return ret1

    @staticmethod
    def get_install_capacity_object_biomass_percentage():
        params = {'name': '生物质能装机容量'}
        return InstallAndGeneratePercentageUtils.get_install_capacity_object_single_percentage(params)

    @staticmethod
    def get_install_capacity_object_biomass_detail():
        ret1 = []
        ret1.append({'database': GREEN_CLEAN,
                     'type': RENEWABLE_POWER_INSTALL,
                     'indicator': BIOMASS_INSTALL_RATE,
                     'resultList': InstallCapacityManager.get_install_capacity_object_biomass_percentage()})

        return ret1


if __name__ == '__main__':
    pass
