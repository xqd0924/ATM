import time
from db import db_handler
from lib import common

logger_bank = common.get_logger('Bank')

def get_account(name):
    #获取用户余额
    user_dic = db_handler.select(name)
    account = user_dic['account']
    return account

def withdraw_interface(name,account):
    user_dic = db_handler.select(name)
    user_dic['account']-=account*1.05
    user_dic['bankflow'].append('%s 提现 %s' %(time.strftime("%Y-%m-%d %X"),account))
    db_handler.update(user_dic)
    logger_bank.info('%s 提现 %s' %(name,account))

def repay_interface(name,account):
    user_dic = db_handler.select(name)
    user_dic['account']+=account
    user_dic['bankflow'].append('%s 还款：%s' %(time.strftime("%Y-%m-%d %X"),account))
    db_handler.update(user_dic)
    logger_bank.info('%s 还款 %s' % (name, account))

def transfer_interface(from_user,to_user,account):
    from_user_dic = db_handler.select(from_user)
    from_user_dic['account'] -= account
    to_user_dic = db_handler.select(to_user)
    to_user_dic['account']+=account
    from_user_dic['bankflow'].append('%s 转账给%s：%s' % (time.strftime("%Y-%m-%d %X"),to_user,account))
    to_user_dic['bankflow'].append('%s 收到%s：%s' % (time.strftime("%Y-%m-%d %X"),from_user,account))
    db_handler.update(from_user_dic)
    db_handler.update(to_user_dic)
    logger_bank.info('%s 转账 %s %s' % (from_user,to_user,account))

def consume_interface(name,cost):
    user_dic = db_handler.select(name)
    if user_dic['account'] >= cost:
        user_dic['account']-=cost
        user_dic['bankflow'].append('消费 %s' %cost)
        db_handler.update(user_dic)
        return True,'消费成功'
    else:
        return False,'余额不足'

def check_records_interface(name):
    user_dic = db_handler.select(name)
    return user_dic['bankflow']
