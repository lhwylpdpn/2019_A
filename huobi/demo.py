#!/usr/bin/python
# -*- coding: UTF-8 -*-

from service import HuobiContract
from huobi_config import HuobiConfig
from pprint import pprint
import pandas as pd
#import numpy as np
import time
contract_config = HuobiConfig.contract_config

URL = contract_config["url_prefix_2"]
ACCESS_KEY = contract_config["access_key"]
SECRET_KEY = contract_config["secret_key"]
dm = HuobiContract(URL, ACCESS_KEY, SECRET_KEY)
pd.set_option('display.max_columns', None)
# # 显示所有行
pd.set_option('display.max_rows', None)
""" 获取合约信息 """
#pprint(dm.get_contract_info(contract_code='BTC200327'))

""" 获取合约指数信息 """
#pprint(dm.get_contract_index("BTC"))

""" 获取合约最高限价和最低限价 """
#pprint(dm.get_contract_price_limit(contract_code='BTC200327'))

""" 获取当前可用合约总持仓量 """
#pprint(dm.get_contract_open_interest(contract_code='BTC200327'))
""" 获取K线 """
#pprint(dm.get_contract_kline("BTC_CQ","1min"))
""" 获取tick """
#pprint(dm.get_contract_market_merged("BTC_CQ"))


""" 获取用户账户信息 """
#pprint(dm.get_contract_account_info("BTC"))

""" 获取用户持仓信息 """
#pprint(dm.get_contract_position_info())

""" 合约下单 """
# pprint(dm.send_contract_order(symbol='', contract_type='', contract_code='BTC200327',
#                               client_order_id='', price=9650, volume=1, direction='sell',
#                               offset='open', lever_rate=1, order_price_type='limit'))

""" 撤销订单 """
# pprint(dm.cancel_contract_order(symbol='BTC', order_id='42652161'))
""" 获取当前有效委托 """
#pprint(dm.get_contract_open_orders())

""" 获取历史成交订单 """


def test():
	page_index=1
	res=dm.get_history_orders(symbol='BTC',page_index=str(page_index))
	trades=res['data']['trades']
	while page_index<int(res['data']['total_page']):
		page_index+=1
		res=''
		res=dm.get_history_orders(symbol='BTC',page_index=str(page_index))
		trades+=res['data']['trades']
		print(page_index)

	buy_=[]
	sell=[]
	df=pd.DataFrame.from_dict(trades)
	#df=df[(df['order_id']==656581740190896128)]
	df.eval('本金_BTC=100/trade_price',inplace=True)
	df.eval('手续费比例=trade_fee/本金_BTC',inplace=True)

	df=df.groupby(['direction','offset']).sum()
	print(df)





def shouyiquxian(dis,price):
	price_open=price
	price_close=price-dis
	

	chengben=100/price
	shouyi=100/price_close-100/price_open
	#print(shouyi,chengben)


def xx(dis,price):#计算，如果需要同等收益，那么返回距离变化的因子

	x=price/dis

	n=x/(x-2)

	return n


if __name__ == '__main__':
	
	test()





# {'match_id': 32778211824, 
# 'order_id': 656581740190896128, 
# 'symbol': 'BTC', 
# 'contract_type': 'quarter',
#  'contract_code': 'BTC200327', 
#  'direction': 'buy', 'offset': 'open', 
#  'trade_volume': 1, 'trade_price': 6883, 
#  'trade_turnover': 100, 'trade_fee': -2.905709719599e-06,
#   'offset_profitloss': 0, 
#   'create_date': 1576582935724,
#    'role': 'Maker', 
#    'order_source': 'android', 
#    'order_id_str': 
#    '656581740190896128', 
#    'fee_asset': 'BTC', 
#    'id': '32778211824-656581740190896128-1'}



# 做空收益=100/卖出价格 - 100/买入价格
# 做多收益=（100/买入价格 -100／卖出价格）*手数

#做空成本=100/卖空价格
#做空收益=100/卖出价格 - 100/买入价格
# #做空收益*买入价格*卖出价格=100卖入价格-100卖出价格

# shouyi=100(距离)／（买入价格*（买入价格-距离））
# 买入价格*（买入价格-距离）=距离
# 买入价格平方 =距离（1+买入价格）



#开仓价格/距离=2n/（n-1）


#买入价格 price
#卖出价格 price-dis


















