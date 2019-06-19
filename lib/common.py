from core import src
import logging.config
from conf import setting

def login_auth(func):
    def wrapper(*args,**kwargs):
        if not src.user_data['is_auth']:
            src.login()
            return func(*args,**kwargs)
        else:
            return func(*args,**kwargs)
    return wrapper

def get_logger(name):
    logging.config.dictConfig(setting.LOGGING_DIC) #导入上面定义的logging配置
    logger = logging.getLogger(name) #生成一个logger实例
    return logger
