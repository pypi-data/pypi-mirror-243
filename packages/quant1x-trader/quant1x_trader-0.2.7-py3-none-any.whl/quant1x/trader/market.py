# -*- coding: UTF-8 -*-

BadSymbolError = RuntimeError("无法识别的证券代码")

# 市场缩写
MARKET_SHANGHAI = 'SH'  # 上海
MARKET_SHENZHEN = 'SZ'  # 深圳
MARKET_HONGKONG = 'HK'  # 香港

# 市场缩写元组
tup_market = (MARKET_SHANGHAI, MARKET_SHENZHEN)
# 上海交易所证券代码前缀
tup_prefix_shanghai = ('60', '68', '510')
# 深圳交易所证券代码前缀
tup_prefix_shenzhen = ('00', '30')


def get_security_type(symbol: str) -> str:
    """
    获取股票市场标识
    :param symbol:  代码
    :return:
    """
    symbol = symbol.strip()
    code = symbol.upper()
    if code.startswith(tup_market):
        return code[:2].upper()
    elif code.endswith(tup_market):
        return code[:-2].upper()
    elif code.startswith(tup_prefix_shanghai):
        return MARKET_SHANGHAI
    elif code.startswith(tup_prefix_shenzhen):
        return MARKET_SHENZHEN
    raise BadSymbolError


def fix_security_code(symbol: str) -> str:
    """
    调整证券代码
    :param symbol:
    :return:
    """
    security_code = ''
    if len(symbol) == 6:
        flag = get_security_type(symbol)
        security_code = f'{symbol}.{flag}'
    elif len(symbol) == 8 and symbol[:2] in ["sh", "sz", "SH", "SZ"]:
        security_code = symbol[2:] + '.' + symbol[:2].upper()
    else:
        raise BadSymbolError
    return security_code
