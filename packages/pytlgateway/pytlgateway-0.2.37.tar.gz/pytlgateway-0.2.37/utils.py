import sys
import os
from datetime import datetime

def decode_exchange_id(suffix):
    exchange = 0
    if suffix == 'SH':
        exchange = 101        #EXCHANGE_SSE 
    elif suffix == 'SZ':
        exchange = 102        #EXCHANGE_SZE 
    
    return exchange

def get_log_default_path():
    # python2: linux2, python3: linux
    if sys.platform.startswith("linux") or sys.platform == "darwin":
        dirs = "/shared/log"
    elif sys.platform == "win32":
        dirs = os.path.join(get_windows_first_disk() + "/tmp/linker/log")
    else:
        dirs = '.'

    return dirs


def get_digit_from_env(env_name, default_num):
    num = str(os.environ.get(env_name))
    return int(num) if num.isdigit() else default_num

def get_log_given_path(path):
    dirs = os.path.join(path)
    return path

def get_exchange_from_ticker(ticker:int):
    stock_code = f'{ticker:06d}'
    if stock_code.startswith('00'):
        stock_code += '.SZ'
    elif stock_code.startswith('6'):
        stock_code += '.SH'
    elif stock_code.startswith('5'):
        stock_code += '.SH'
    else:
        stock_code += '.SZ'
    return stock_code

def check_today_index(input_datetime_str):
    input_datetime = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")

    # 获取当前日期的 datetime 对象
    current_datetime = datetime.now()

    # 判断是否在今天
    if input_datetime.date() == current_datetime.date():
        return True

    return False