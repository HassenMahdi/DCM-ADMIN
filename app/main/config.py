import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    # MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:Bxia!2020DaaTa1920CAvlmd@a43ea3b57744d43fab0eb7c2ef66e767-760928362.eu-west-1.elb.amazonaws.com:27017/dcm?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false")
    MONGO_URI = "mongodb://root:Bxia2020DaaTa1920CAvlmd@20.74.14.235:27017/dcm?authSource=admin&readPreference=primary&ssl=false"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
