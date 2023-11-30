# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 交易数量
def order_count(stock: str, count: int):
    return order_volume(symbol=stock, volume=count, order_type=OrderType_Market, side=OrderSide_Buy,
                        position_effect=PositionEffect_Open)


# 交易到特定数量
def order_target_count(stock: str, count: int):
    return order_target_volume(symbol=stock, volume=count, order_type=OrderType_Market,
                               position_side=PositionSide_Long)
