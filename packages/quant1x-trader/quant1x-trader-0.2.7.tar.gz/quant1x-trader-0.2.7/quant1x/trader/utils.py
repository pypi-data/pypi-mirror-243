# coding=utf-8
import os.path
import time
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from xtquant import xtdata
from xtquant.xttype import *

# 执行成功
errno_success = 0
# qmt错误码基数
qmt_errno_base = 1000
# miniQMT 没有找到
errno_miniqmt_not_found = qmt_errno_base + 1
# quant1x.yaml配置文件没找到
errno_config_not_exist = qmt_errno_base + 2
# 连接miniQMT失败
errno_miniqmt_connect_failed = qmt_errno_base + 3
# 非交易日
errno_not_trade_day = qmt_errno_base + 4
# 缺少账户id
errno_not_found_account_id = qmt_errno_base + 5
# 缺少订单路径
errno_not_found_order_path = qmt_errno_base + 6

kFormatFileDate = '%Y%m%d'
kFormatOnlyDate = '%Y-%m-%d'
kFormatTimestamp = '%Y-%m-%d %H:%M:%S'
kTimestamp = '%H:%M:%S'
errBadSymbol = RuntimeError("无法识别的证券代码")


# # 买入持仓率, 资金控制阀值
# position_ratio = 0.5000
# # 买入交易费率
# buy_trade_rete = 0.0250
# # 相对开盘价溢价多少买入
# buy_premium_rate = 0.0200
# # 买入最大金额
# buy_amount_max = 250000.00
#
# # 竞价开始时间 - 卖出
# ask_begin = '09:50:00'
# # 竞价结束时间 - 卖出
# ask_end = '14:59:30'
#
# # 盘中订单 - 开始时间
# TICK_BEGIN = '09:30:00'
# # 盘中订单 - 结束时间
# TICK_END = '14:57:00'
#
# cancel_begin = '09:00:00'
# cancel_end = '15:00:00'


def mkdirs(path: str):
    """
    创建目录
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def touch(filename: str):
    """
    创建一个空文件
    :param filename:
    :return:
    """
    directory = os.path.dirname(filename)
    mkdirs(directory)
    with open(filename, 'w') as done_file:
        pass


def is_nan(n) -> bool:
    """
    判断是否nan或inf
    :param n:
    :return:
    """
    return np.isnan(n) or np.isinf(n)


def price_round(num: float, digits: int = 2) -> float:
    """
    价格四舍五入
    :param num:
    :param digits: 小数点后几位数字
    :return:
    """
    if isinstance(num, float):
        num = str(num)
    x = Decimal(num).quantize((Decimal('0.' + '0' * digits)), rounding=ROUND_HALF_UP)
    return float(x)


def today_is_tradeday() -> bool:
    """
    今天是否交易日
    :param start_time:
    :param end_time:
    :param count:
    :return:
    """
    time_format = '%Y%m%d'
    today = time.strftime(time_format)
    dates = xtdata.get_trading_dates('SH', today, today)
    if len(dates) == 0:
        return False
    date = time.strftime(time_format, time.localtime(dates[0] / 1000))
    return today == date
