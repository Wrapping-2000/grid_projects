import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        #"host": "mongodb://root:iflytek.COM@10.40.152.200:27018/post_project?authSource=admin",
        "db": 'post_project',
        "connect": "true"
    }

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        #"host": "mongodb://root:iflytek.COM@10.40.152.200:27018/post_project?authSource=admin",
        "db":'post_project',
        "connect": "true"
    }


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
