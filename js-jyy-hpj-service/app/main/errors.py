from app.utils.return_code import ErrorMessage
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return ErrorMessage.PAGE_NOT_FOUND


@main.app_errorhandler(500)
def internal_server_error(e):
    return ErrorMessage.INTERNAL_SERVER_ERROR
