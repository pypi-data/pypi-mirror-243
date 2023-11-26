# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 获取所有指数（股票市场、当前有效）
def get_all_index(context):
    normal_index_list = get_symbol_infos(1060, 106001)
    index_list = []
    for index in normal_index_list:
        if index.delisted_date < context.now:
            continue
        index_list.append(index.symbol)

    return index_list


# 获取所有股票（股票市场、当前有效）
def get_all_security(context):
    normal_stocks = get_symbol_infos(1010, 101001)
    stocks = []
    for stock in normal_stocks:
        if stock.delisted_date < context.now:
            continue
        stocks.append(stock.symbol)

    return stocks


# TODO 获取龙虎榜股票列表
# 1. 日常交易
# 日收盘价涨跌幅偏离值达7%：单只股票（基金）涨跌幅-对应分类指数涨跌幅
# 日振幅达15%：股票开盘后的当日最高价和最低价之间的差的绝对值与昨日收盘价的百分比
# 日换手率达20%：当日的日成交量(成交股数)除以该股的流通股本
#
# 深市分主板、中小板、创业板，每个条件各选前5名的上榜。沪市每个条件各选前3名上榜。如果条件相同，则按成交额和成交量选取。
#
# 2. 异常波动
# 连续3个交易日收盘价偏离值累计达到20%(ST和*ST为12%)
# 连续3个交易日累计换手率达到20%、且日均换手率与前5个交易日日均换手率的比值达到30倍
#
# 3. 无价格涨跌幅限制的个股
def get_dragon_tiger_list(context):
    pass
