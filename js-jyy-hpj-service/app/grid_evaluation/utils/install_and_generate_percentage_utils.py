from app.grid_evaluation.utils.percentage_calculate import PercentageCalculate
from app.grid_evaluation.manager.models import InstallCapacity
from app.grid_evaluation.manager.models import GenerateCapacity


class InstallAndGeneratePercentageUtils:

    @staticmethod
    def get_install_capacity_object_single_percentage(params):
        dict_param = {'total_install': '并网发电装机容量'}
        result = []
        total_install = dict_param.get('total_install')
        for total_install_object in InstallCapacity.objects(name=total_install).order_by('-date'):
            object1 = InstallCapacity.objects(date=total_install_object.date, name=params.get('name'))
            if len(object1) == 0:
                continue
            object = object1[0]
            total_install = total_install_object.amount
            rate = PercentageCalculate.power_generate_percentage(total_install, object.amount)

            result.append({
                "time": object.date,
                "value": float(format(rate, '.2f'))
            })
        return result

    @staticmethod
    def get_generate_power_objects_single_percentage(params):
        dict_param = {'social_power': '全社会用电量'}
        result = []
        social_powers = dict_param.get('social_power')
        for social_power_object in GenerateCapacity.objects(name=social_powers).order_by('-date'):
            object = GenerateCapacity.objects(date=social_power_object.date, name=params.get('name'))[0]
            social_power = social_power_object.amount
            result.append({
                "time": object.date,
                "value": PercentageCalculate.power_generate_percentage(social_power, object.amount)
            })
        return result

    @staticmethod
    def get_single_permeability_percentage(params):
        result = []
        total_powers = '总发电量'
        for total_power_object in GenerateCapacity.objects(name=total_powers).order_by('-date'):
            object = GenerateCapacity.objects(date=total_power_object.date, name=params.get('name'))[0]
            total_power = total_power_object.amount
            result.append({
                "time": object.date,
                "value": PercentageCalculate.power_generate_percentage(total_power, object.amount)
            })
        return result