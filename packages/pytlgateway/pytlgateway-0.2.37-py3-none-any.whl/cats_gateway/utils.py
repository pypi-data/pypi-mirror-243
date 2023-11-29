from datetime import datetime
import sys
import os

#没有融券
def decode_cats_side(side):
    rtn_trade_side = 0
    if side == '1':
        rtn_trade_side = 1
    elif side == '2':
        rtn_trade_side = 2
    elif side == 'A':
        rtn_trade_side = 3
    return rtn_trade_side

#0 new 2 filled 4 canceled 6 part canceled
def decode_cats_status(status):
    new_status = ""
    if status in [0, 1]:
        new_status = 'active'
    elif status == 2:
        new_status = 'filled'
    elif status == 4 or status == 3:
        new_status = 'canceled'
    return new_status

def side_to_target_type(side):
    target_type = ""
    if side in [1,5]:
        target_type = "buy"
    elif side == 2:
        target_type = "sell"
    return target_type

def decode_exchange_id(exchange):
    exchange = 0
    if exchange == 'SH':
        exchange = 101        #EXCHANGE_SSE 
    elif exchange == 'SZ':
        exchange = 102        #EXCHANGE_SZE 
    
    return exchange


def decode_ordtype(order_type:str):
    ord_type = -1
    mapping = {
        'twap': 'TWAP',
        'vwap': 'VWAP',
        'SmartTWAP': 'SmartTWAP',
        'SmartVWAP': 'SmartVWAP'
    }
    ord_type = mapping.get(order_type, -1)
    return ord_type
