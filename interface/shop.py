from db import db_handler
from interface import bank
from lib import common

logger_shop = common.get_logger('shop')

def shopping_interface(name,shopping_cart,cost):
    flag,msg = bank.consume_interface(name,cost)
    if flag:
        user_dic = db_handler.select(name)
        user_dic['shopping_cart'] = shopping_cart
        db_handler.update(user_dic)
        logger_shop.info('%s 购买了商品' %name)
        return True,'购买成功'
    else:
        return False,'购买失败'


def check_shopping_cart_interface(name):
    user_dic = db_handler.select(name)
    # shopping_cart = user_dic['shopping_cart']
    for item in user_dic:
        if item == 'shopping_cart':
            shopping_cart = user_dic['shopping_cart']
            return True,shopping_cart
    else:
        return False,'购物车为空'