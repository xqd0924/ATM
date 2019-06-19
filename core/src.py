from interface import user
from lib import common
from interface import bank
from interface import shop

user_data = {
    'name':None,
    'is_auth':False
}
def login():
    if user_data['is_auth'] == True:
        print('用户已登录')
        return
    print('请登录')
    count = 1
    tag = True
    while tag:
        name = input('用户名：').strip()
        # 判断用户是否存在
        user_dic = user.get_userinfo_interface(name)
        while user_dic:
            pwd = input('密码：').strip()
            if count == 3:
                user.lock_user_interface(name)
                print('用户被锁定')
                tag = False
                break
            if user_dic['password'] == pwd and not user_dic['locked']:
                user_data['name'] = name
                user_data['is_auth'] = True
                print('登录成功')
                tag = False
                break
            else:
                count+=1
                print('password error,or locked')
                break
        else:
            print('用户不存在')
            continue
def register():
    if user_data['is_auth'] == True:
        print('用户已登录')
        return
    print('注册')
    while True:
        name = input('请输入用户名：').strip()
        #判断用户是否存在
        if user.get_userinfo_interface(name):
            print('user is exists')
            continue
        else:
            pwd = input('请输入密码：').strip()
            conf_pwd = input('确认密码：').strip()
            if pwd == conf_pwd:
               user.register(name,pwd)
               print('注册成功')
               break
            else:
                print('密码不一致')
                continue

@common.login_auth
def check_balance():
    print('查询余额')
    account = bank.get_account(user_data['name'])
    print('您的余额是：%s元' %account)

@common.login_auth
def transfer():
    print('转账')
    while True:
        to_user = input('请输入收款人姓名(q退出)：').strip()
        if to_user == 'q':break
        if to_user == user_data['name']:
            print('不能给自己转账')
            continue
        to_user_dic = user.get_userinfo_interface(to_user)
        if to_user_dic:
            transfer_account = input('请输入转账金额(q退出)：').strip()
            if transfer_account == 'q':break
            if transfer_account.isdigit():
                transfer_account = float(transfer_account)
                user_account = bank.get_account(user_data['name'])
                if user_account>=transfer_account:
                    bank.transfer_interface(user_data['name'],to_user,transfer_account)
                    print('转账成功')
                    break
                else:
                    print('余额不足')
            else:
                print('请输入数字')
        else:
            print('收款人不存在')

@common.login_auth
def repay():
    print('还款')
    while True:
        account = input('请输入还款金额(q退出)：').strip()
        if account == 'q':break
        if account.isdigit():
            account = float(account)
            bank.repay_interface(user_data['name'],account)
            print('还款成功')
            break
        else:
            print('请输入数字')

@common.login_auth
def withdraw():
    print('提现')
    while True:
        account = input('请输入提现金额(q退出)：').strip()
        if account == 'q':
            break
        if account.isdigit():
            account = float(account)
            user_account = bank.get_account(user_data['name'])
            if user_account>=account*1.05:
                bank.withdraw_interface(user_data['name'],account)
                print('提现成功')
                break
            else:
                print('余额不足')
        else:
            print('请输入数字')


@common.login_auth
def check_records():
    bankflow = bank.check_records_interface(user_data['name'])
    for record in bankflow:
        print(record)

@common.login_auth
def shopping():
    print('购物')
    goods_list = [
        ['coffee',10],
        ['chicken',30],
        ['iphone',8000],
        ['macBook',12000],
        ['car',100000]
    ]
    user_balance = bank.get_account(user_data['name'])
    cost = 0
    shopping_cart = {}
    while True:
        for i,goods in enumerate(goods_list):
            print('%s:%s' %(i,goods))
        buy = input('请输入要购买的商品编号(q退出并付款)：').strip()
        if buy.isdigit():
            buy = int(buy)
            goods_name = goods_list[buy][0]
            goods_price = goods_list[buy][1]
            if user_balance>=goods_price:
                if goods_name not in shopping_cart:
                    shopping_cart[goods_name] = {'price':goods_price,'count':1}
                else:
                    shopping_cart[goods_name]['count']+=1
                user_balance-=goods_price*shopping_cart[goods_name]['count']
                cost+=goods_price*shopping_cart[goods_name]['count']
                print('%s 加入购物车' %goods_name)
            else:
                print('余额不足')
        elif buy == 'q':
            if not shopping_cart:break
            print(shopping_cart)
            confim = input('是否购买(y/n):').strip()
            if confim == 'y':
                flag,msg = shop.shopping_interface(user_data['name'],shopping_cart,cost)
                if flag:
                    print(msg)
                    break

        else:
            print('请输入数字')

@common.login_auth
def check_shopping_cart():
    print('查看购物车')
    flag,msg = shop.check_shopping_cart_interface(user_data['name'])
    if flag:
        print(msg)
    else:
        print(msg)


func_dic = {
    '1':login,
    '2':register,
    '3':check_balance,
    '4':transfer,
    '5':repay,
    '6':withdraw,
    '7':check_records,
    '8':shopping,
    '9':check_shopping_cart
}

def run():
    while True:
        print("""
    欢迎来到购物商城，请选择功能
    0.退出
    1.登录
    2.注册
    3.查询余额
    4.转账
    5.还款
    6.提现
    7.查看流水
    8.购物
    9.查看购物车
              """)
        choice = input('>>>:').strip()
        if choice == '0':break
        if choice not in func_dic:continue
        func_dic[choice]()


