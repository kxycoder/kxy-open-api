import logging
import os
from kxy.framework.base_config import BaseConfig


class Config(BaseConfig):
    AppName = 'kxy.open.api'
    SystemCode = 'CRM'
    '''应用名称'''
    LOG_LEVEL = logging.INFO
    '''日志级别'''
    ENV_NAME = 'test'
    '''环境名称'''
    # Redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT=6379
    REDIS_PASSWORD=None
    REDIS_DB=1
    # 假设JWT的密钥和算法
    JWT_SECRET_KEY = "We8!@rdXls&_s=+%"
    JWT_ALGORITHM = "HS256"
    wx_appid=''
    wx_secret=''
    AUTH_URL=''
    AutoAddModel = False
    ignor_auth=1
    WXTOKEN_ASYNC_URL = ''
    UPLOAD_FILEPATH='uploadfiles'
    BussinessLog = False
    ACCESS_TOKEN_EXPIRE_SECONDES=24*60*60*30
    SSO_URL=''
    BackEndPrefix = 'admin-api'

class DevConfig(Config):
    mysql_url = 'mysql+aiomysql://myfriend:123456@192.168.15.172:3306/kxy-open?autocommit=False'
    # normal_mysql_url = 'mysql+pymysql://myfriend:123456@192.168.15.172:3306/ant_demo?autocommit=True'
    AUTH_URL = ''
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT=6379
    REDIS_PASSWORD=None
    LOG_LEVEL = logging.DEBUG
    ENV_NAME = 'dev'
    WXTOKEN_ASYNC_URL=''
    AutoAddModel = True
    Cloud_AccessKey = ''
    Cloud_AccessSecret = ''
    COS_BucketName = 'myfriend'
    COS_Region = 'ap-guangzhou'

    
class DevContainerConfig(Config):
    LOG_LEVEL = logging.DEBUG
    
class TestConfig(Config):
    LOG_LEVEL = logging.DEBUG
    ENV_NAME = 'test'
class ProductionConfig(Config):
    LOG_LEVEL = logging.INFO
    ENV_NAME = 'production'
    mysql_url = 'mysql+aiomysql://myfriend:123456@192.168.15.172:3306/kxy-open?autocommit=False'
    
env = os.environ.get("WORK_ENV")
print("WORK_ENV:", env)
if env == 'dev':
    print('use DevConfig()')
    config = DevConfig()
elif env == 'test':
    print('use TestConfig()')
    config = TestConfig()
elif env=='production':
    print('use ProductionConfig()')
    config = ProductionConfig()
elif env=='dev-container':
    print('use DevContainerConfig()')
    config = DevContainerConfig()
else:
    print('use DevConfig()')
    config = DevConfig()
config.env_first()