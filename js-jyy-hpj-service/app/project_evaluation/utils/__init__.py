from datetime import datetime


class ContrastFiledParam:
    VoltageLevel = "voltage_level"
    Classification = "classification"
    Company = "company"
    OperationYear = "operation_year"

    values = (VoltageLevel, Classification, Company, OperationYear)

    cn_name_dict = {
        VoltageLevel: "电压等级",
        Classification: "工程分类",
        OperationYear: "投运年份",
        Company: "所属公司"
    }

    @staticmethod
    def get_cn(value):
        return ContrastFiledParam.cn_name_dict.get(value)


def do_division(dividend, divisor):
    try:
        dividend = float(dividend)
        divisor = float(divisor)
        return keep_2f(dividend / divisor)
    except Exception as e:
        return None


def keep_2f(value):
    try:
        float(value)
    except Exception as e:
        return None

    return float('%.2f' % float(value))


def is_float_able(value):
    try:
        float(value)
    except Exception as e:
        return False

    return True


def average(value_list):
    if not value_list:
        return None
    if not isinstance(value_list, list):
        return value_list

    cal_value_list = list(filter(is_float_able, value_list))
    cal_value_list = [float(i) for i in cal_value_list]

    return keep_2f(sum(cal_value_list) / len(cal_value_list))


def keep_percent(dividend, divisor, dividend_abs=False):
    try:
        dividend = float(dividend)
        if dividend_abs:
            dividend = abs(dividend)
        divisor = float(divisor)
        return keep_2f(dividend * 100 / divisor)
    except Exception as e:
        return None


def format_datetime(t, f_format="%Y/%m/%d"):
    if not isinstance(t, datetime):
        return None
    return t.strftime(f_format)


def has_empty_value(data_raw):
    if not data_raw:
        return True
    for k, v in data_raw.items():
        if not v:
            return True

    return False


def has_all_number(data_raw):
    if not data_raw:
        return False
    for k, v in data_raw.items():
        try:
            float(v)
        except Exception as e:
            return False

    return True


def has_all_datetime(data_raw):
    if not data_raw:
        return False
    for k, v in data_raw.items():
        if not isinstance(v, datetime):
            return False

    return True


def filter_empty_year_data(data_list):
    result = []
    for item in data_list:
        if item.get("year") and item.get("value") is not None:
            result.append(item)

    return result


def combine_year_list(old_value, new_value):
    new_value_map = {}
    if isinstance(old_value, list):
        for item in old_value:
            new_value_map[item["year"]] = item["value"]
    if isinstance(new_value, list):
        for item in new_value:
            new_value_map[item["year"]] = item["value"]
    if new_value_map:
        return [{"year": year, "value": value} for year, value in new_value_map.items()]


PROJECT_CLASSIFICATION = ['优化网架结构', '保障电源送出', '加强输电通道', '服务新能源', '满足用电需求', '电铁供电']


PROJECT_VOLTAGE_LEVEL = [110, 220, 500, 750]

if __name__ == "__main__":
    print(has_all_number({"name": 123}))
