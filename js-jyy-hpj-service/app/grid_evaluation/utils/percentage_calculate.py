from app.grid_evaluation.manager.models import GenerateCapacity, InstallCapacity


class PercentageCalculate:

    @staticmethod
    def power_generate_percentage(total, type_power_amount):
        ret = round(type_power_amount / total, 4) * 100
        return float(format(ret, '.2f'))

    @staticmethod
    def get_power_sum(date, params):
        sum = 0
        dict_param = {}
        dict_param = params
        object = GenerateCapacity.objects(date=date)
        for name in dict_param.keys():
            for object1 in object(name=dict_param.get(name)):
                if 'social_power' == name:
                    sum = sum + 0
                elif 'date' == name:
                    sum = sum + 0
                else: sum += object1.amount
        return sum

    @staticmethod
    def get_power_sum_percentage(date, params):
        total = GenerateCapacity.objects(date=date, name=params.get('social_power'))[0].amount
        sum = PercentageCalculate.get_power_sum(date, params)
        return PercentageCalculate.power_generate_percentage(total, sum)

    @staticmethod
    def get_install_sum(date, params):
        sum = 0
        dict_param = {}
        dict_param = params
        object = InstallCapacity.objects(date=date)
        for name in dict_param.keys():
            for object1 in object(name=dict_param.get(name)):
                if 'total_install' == name:
                    sum = sum + 0
                elif 'store_install' == name:
                    sum = sum + 0
                elif 'renew_install' == name:
                    sum = sum + 0
                else:
                    sum += object1.amount
        return sum

    @staticmethod
    def get_install_sum_percentage(date, params):
        total = InstallCapacity.objects(date=date, name=params.get('total_install'))[0].amount
        sum = PercentageCalculate.get_power_sum(date, params)
        return PercentageCalculate.power_generate_percentage(total, sum)