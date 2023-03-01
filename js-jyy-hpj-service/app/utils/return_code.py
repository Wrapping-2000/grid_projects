import json
from functools import wraps
from .MyEncoder import MyEncoder

class ReturnMessage:

    SUCCESS = (json.dumps({"code": "SUCCESS"}, cls=MyEncoder), 200)

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

    NOT_FOUND = "NOT_FOUND"

    INVALID_PARAM = "INVALID_PARAM"

    @staticmethod
    def build_success(data):
        result = {
            "code": "SUCCESS",
            "data": data
        }
        return json.dumps(result, ensure_ascii=False, cls=MyEncoder), 200

    @staticmethod
    def build_error(error_code, error_message, http_code):
        result = {
            "error_code": error_code,
            "error_message": error_message
        }
        return json.dumps(result, ensure_ascii=False, cls=MyEncoder), http_code


class ErrorMessage:

    INVALID_USERNAME_OR_PASSWORD = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM,
                                                             "Invalid user_name or password.", 400)

    INVALID_PARAM = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM,
                                              "Invalid param.", 400)

    INVALID_TARGET_NAME = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM,
                                                    "Invalid target name.", 400)

    INVALID_TARGET_NAME_STATISTICS = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM,
                                                               "Target name can't be counted.", 400)

    INVALID_WPS_CODE = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM,
                                                 "Invalid wps code.", 400)

    INVALID_CONTRAST_FILED = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, "Invalid contrast_filed.", 400)

    INVALID_YEAR_PARAM = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, "Invalid param year.", 400)

    INVALID_PRIMARY_INDEX = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM, "Invalid primary_index.", 400)

    INVALID_UPDATE_PARAM_WPS_CODE = ReturnMessage.build_error(ReturnMessage.INVALID_PARAM,
                                                              "Attribute wps code is not allowed to update.", 400)

    PAGE_NOT_FOUND = ReturnMessage.build_error(ReturnMessage.NOT_FOUND,
                                               "Page not found.", 404)

    INTERNAL_SERVER_ERROR = ReturnMessage.build_error(ReturnMessage.INTERNAL_SERVER_ERROR,
                                                      "Internal server error.", 500)

    PROJECT_NOT_EXIST = ReturnMessage.build_error(ReturnMessage.INTERNAL_SERVER_ERROR,
                                                  "project not exist.", 500)


def error_handler(func):
    """
    return 500 when error comes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return ReturnMessage.build_error(ReturnMessage.INTERNAL_SERVER_ERROR, str(repr(e)), 500)

    return wrapper
