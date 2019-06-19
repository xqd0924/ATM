from db import db_handler
from lib import common

logger_user = common.get_logger('User')

def get_userinfo_interface(name):
    user_dic = db_handler.select(name)
    return user_dic

def register(name,pwd,account=15000):
    user_dic = {
        'name': name,
        'password': pwd,
        'locked': False,
        'account': 15000,
        'credit': 15000,
        'bankflow':[],
        }
    db_handler.update(user_dic)
    logger_user.info('%s 注册成功' %name)

def lock_user_interface(name):
    user_dic = get_userinfo_interface(name)
    user_dic['locked'] = True
    db_handler.update(user_dic)
