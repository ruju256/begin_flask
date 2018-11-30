import os
from dotenv  import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')  
# load_dotenv(dotenv_path)


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
    TESTING = False

#TESTING CONFIGURATION
class TestingConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = "postgresql://localhost/test_store_manager"
    ENV = 'development'

app_configuration = {
    "development" : DevelopmentConfig,
    "testing" : TestingConfig,
    "production": ProductionConfig
}