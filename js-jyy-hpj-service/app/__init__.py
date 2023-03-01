from flask import Flask
from config import config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flasgger import Swagger


db = MongoEngine()
login_manager = LoginManager()
swagger = Swagger()


def create_app(config_name):
    app = Flask(__name__, static_url_path='', static_folder='front', template_folder='front')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    swagger.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    from app.project_evaluation.project import project as project_blueprint
    app.register_blueprint(project_blueprint, url_prefix='/api/v1/project')

    from app.project_evaluation.target import target as target_blueprint
    app.register_blueprint(target_blueprint, url_prefix='/api/v1/target')

    from app.grid_evaluation.power import comment as comment_blueprint
    app.register_blueprint(comment_blueprint, url_prefix='/api/v1/comment')

    from app.project_excel.power import excel as excel_blueprint
    app.register_blueprint(excel_blueprint, url_prefix='/api/v1/excel')


    return app
