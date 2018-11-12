import os
basedir = os.path.abspath(os.path.dirname(__file__))

#default configuration
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "Letmein256"
    DATABASE_URI = os.getenv('DATABASE_URL')

#DEVELOPMENT CONFIGURATION
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = "postgresql://localhost/store_manager"
    ENV = 'development'

#PRODUCTION CONFIGURATION
class ProductionConfig(BaseConfig):
    DEBUG = False

#TESTING CONFIGURATION
class TestingConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = "postgresql://localhost/test_store_manager"
    ENV = 'development'

app_configuration = {
    "development" : DevelopmentConfig,
    "testing" : TestingConfig
}