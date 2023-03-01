from flask import request
from app.project_evaluation.manager.user_manager import UserManager
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from app.utils.return_code import ReturnMessage, ErrorMessage, error_handler


@auth.route('/register', methods=['POST'])
@error_handler
def register():
    """用户注册
    ---
    tags:
    - "auth"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: body
        required: true
        in: body
        schema:
          $ref: "#/definitions/Register"
    definitions:
      Register:
        type: "object"
        required:
        - "user_name"
        - "password"
        properties:
          user_name:
            type: "string"
          password:
            type: "string"
      Response:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/Response"
      400:
        description: INVALID_PARAM
    """
    user_name = request.json.get("user_name")
    password = request.json.get("password")
    if not user_name:
        return ErrorMessage.INVALID_USERNAME
    if not password:
        return ErrorMessage.INVALID_PASSWORD

    UserManager.add_user(user_name, password)

    return ReturnMessage.SUCCESS


@auth.route('/login', methods=['POST'])
@error_handler
def login():
    """用户登录
    ---
    tags:
    - "auth"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: body
        required: true
        in: body
        schema:
          $ref: "#/definitions/Login"
    definitions:
      Login:
        type: "object"
        required:
        - "user_name"
        - "password"
        properties:
          user_name:
            type: "string"
          password:
            type: "string"
          remember_me:
            type: "boolean"
            default: false
      Response:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/Response"
      400:
        description: INVALID_PARAM
    """
    user_name = request.json.get("user_name")
    password = request.json.get("password")
    remember_me = request.json.get("remember_me", False)
    if not user_name or not password:
        return ErrorMessage.INVALID_USERNAME_OR_PASSWORD

    user = UserManager.get_user(user_name)
    if user is not None and user.verify_password(password):
        login_user(user, remember_me)
        return ReturnMessage.SUCCESS

    return ErrorMessage.INVALID_USERNAME_OR_PASSWORD


@auth.route('/logout', methods=['GET'])
@error_handler
@login_required
def logout():
    """用户登出
    ---
    tags:
    - "auth"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    definitions:
      Response:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/Response"
    """
    logout_user()
    return ReturnMessage.SUCCESS


@auth.route('/current_user', methods=['GET'])
@error_handler
def active_user():
    """获取当前用户
    ---
    tags:
    - "auth"
    consumes:
      - "application/json"
    produces:
      - "application/json"
    definitions:
      Response:
        type: object
        properties:
          code:
            type: string
            enum:
              - "SUCCESS"
        data:
          type: object
          properties:
            user_name:
              type: string
    responses:
      200:
        description: SUCCESS
        schema:
          $ref: "#/definitions/Response"
    """
    user_name = None
    if current_user.is_authenticated:
        user_name = current_user.user_name

    result = {
        "user_name": user_name
    }
    return ReturnMessage.build_success(result)
