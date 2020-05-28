#!/usr/bin/python
# -*- coding: UTF-8 -*-

from service import HuobiContract
from huobi_config import HuobiConfig
from pprint import pprint
import pandas as pd
#import numpy as np
import time
import datetime
contract_config = HuobiConfig.contract_config

URL = contract_config["url_prefix_2"]
ACCESS_KEY = contract_config["access_key"]
SECRET_KEY = contract_config["secret_key"]
dm = HuobiContract(URL, ACCESS_KEY, SECRET_KEY)
pd.set_option('display.max_columns', None)
# # 显示所有行
pd.set_option('display.max_rows', None)
global msg_list
import smtplib

from email.mime.text import MIMEText  
msg_list=[]
global trades_list
trades_list=[]
global continue_list
continue_list=[6000,6100,6200,6300,6400,6500,6600]
import copy
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



class trading_auto:
	
	

	def __init__(self, contract_code,dis_,volume_,lever_rate_,len_,flag):
		
		self.order_id={}#save order_id 
		self.contract_code=contract_code
		self.dis_=dis_
		self.volume_=volume_
		self.lever_rate_=lever_rate_
		self.len_=len_
		if flag=='init':


			contract_open_list=[]
			try:
				ask_price=''
				bid_price=''
				res=dm.get_contract_market_merged(symbol='BTC_CQ')#这比较操蛋，如果换季需要调整
				if res['status']=='ok':
					ask_price=res['tick']['ask'][0]
					bid_price=res['tick']['bid'][0]


					for x in range(1,len_+1):
						contract_open_list.append(int((ask_price+bid_price)/2)+dis_*x)
						contract_open_list.append(int((ask_price+bid_price)/2)-dis_*x)
					datetime_=str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
					contract_open_list.reverse()
					print(contract_open_list)
				for r in contract_open_list:
					if r>int((ask_price+bid_price)/2):
						res=[]
						print('init,start,'+str(r),str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
						res=dm.send_contract_order(symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=r, volume=volume_, direction='sell', offset='open',lever_rate=lever_rate_, order_price_type='limit')
						if res['status']=='ok':
							self.order_id[res['data']['order_id']]=res['ts']
						print('init,end,'+str(r),str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
					else:
						res=[]
						print('init,start,'+str(r),str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
						res=dm.send_contract_order(symbol='BTC', contract_type='333',client_order_id='',contract_code=contract_code,price=r, volume=volume_, direction='buy', offset='open',lever_rate=lever_rate_, order_price_type='limit')
						if res['status']=='ok':
							self.order_id[res['data']['order_id']]=res['ts']
						print('init,end,'+str(r),str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
			except Exception as e:
				print(e)
				print('trading deal deal_contract_order error')
				raise e
		else:

			print('you choose not init limit order')

		
	def trading_deal(self):# 获取价格并处理 （挂单、查挂单、查成交，查价格）
		print('trades')
		# 请求order id 的所有内容，获得是否有成交，有成交，就删除orderid 然后开新单
		print('order_time_start',str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
		try:
			for key_ in list(self.order_id.keys()):
				res=dm.get_contract_order_detail('BTC', order_id=key_,order_type='1',created_at=self.order_id[key_])
				if res['status']=='ok':
					init_price=res['data']['price']
					init_direction=res['data']['direction']
					init_offset=res['data']['offset']
					init_volume=res['data']['volume']
					init_trades=res['data']['trades']
					
				if len(init_trades)>0:
					trade_volume=0
					for n in range(0,len(init_trades)):
						trade_volume+=int(init_trades[n]['trade_volume'])
					if trade_volume==self.volume_:#存在分步成交，全成交了再清理
						self.order_id.pop(key_)
						if init_offset=='close' and init_direction=='sell' and init_volume==self.volume_:    #平多，sell-100 开多
										
										res=[]
										res=dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=self.contract_code,price=init_price-self.dis_, volume=self.volume_, direction='buy', offset='open',lever_rate=self.lever_rate_, order_price_type='limit')
										if res['status']=='ok':
											self.order_id[res['data']['order_id']]=res['ts']
										print(res['data'],res['ts'],str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
						if init_offset=='close' and init_direction=='buy' and init_volume==self.volume_:    #平空，buy+100 开空
										res=[]
										res=dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=self.contract_code,price=init_price+self.dis_, volume=self.volume_, direction='sell', offset='open',lever_rate=self.lever_rate_, order_price_type='limit')
										if res['status']=='ok':
											self.order_id[res['data']['order_id']]=res['ts']
										print(res['data'],res['ts'],str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
						if init_offset=='open' and init_direction=='sell' and init_volume==self.volume_:    #开空 ，sell-100 平空 open close 代表平空
										res=[]
										res=dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=self.contract_code,price=init_price-self.dis_, volume=self.volume_, direction='buy', offset='close',lever_rate=self.lever_rate_, order_price_type='limit')
										#dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']-dis_, volume=volume_, direction='buy', offset='open',lever_rate=lever_rate_, order_price_type='limit')
										if res['status']=='ok':
											self.order_id[res['data']['order_id']]=res['ts']
										print(res['data'],res['ts'],str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
						if init_offset=='open' and init_direction=='buy' and init_volume==self.volume_:    #开多，buy+100 平多  # sell close 代表平多
										res=[]
										res=dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=self.contract_code,price=init_price+self.dis_, volume=self.volume_, direction='sell', offset='close',lever_rate=self.lever_rate_, order_price_type='limit')
										if res['status']=='ok':
											self.order_id[res['data']['order_id']]=res['ts']
										#dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']+dis_, volume=volume_, direction='sell', offset='open',lever_rate=lever_rate_, order_price_type='limit')
										print(res['data'],res['ts'],str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))

		except Exception as e:
			print(e)
			print('trading deal init error')
			raise e

	


def LH_get_contract_open_orders(contract_code):

	while 1:
		res=''
		page_index=1
		try:
			res=dm.get_contract_open_orders(symbol='BTC',page_index=str(page_index))
			if res['status']=='ok':
				orders=res['data']['orders']

			while page_index<int(res['data']['total_page']):
				time.sleep(2)
				page_index+=1
				res=''
				res=dm.get_contract_open_orders(symbol='BTC',page_index=str(page_index))
				if res['status']=='ok':
					orders+=res['data']['orders']
				else:
					page_index=page_index-1
			df=pd.DataFrame.from_dict(orders)
			if df.shape[1]>0:
				df=df[(df['contract_code']==str(contract_code))]
			return df # 当前实际挂单
		except Exception as e:
			print(str(e))
			time.sleep(3)
	
def LH_get_history_orders(contract_code):
	while 1:

		res=''
		page_index=1
		try:
			res=dm.get_history_orders(symbol='BTC',page_index=str(page_index))
			if res['status']=='ok':
				#print(res)
				orders=res['data']['trades']
			#while page_index<int(res['data']['total_page']):
			
			#	time.sleep(2)
			#	page_index+=1
			#	res=''
			#	res=dm.get_history_orders(symbol='BTC',page_index=str(page_index))
			#	if res['status']=='ok':
			#		orders+=res['data']['trades']
			#	else:
			#		page_index=page_index-1
			df=pd.DataFrame.from_dict(orders)
			df=df[(df['contract_code']==str(contract_code))]
			return df # 近3天历史成交
		except Exception as e:
			print(str(e))
			time.sleep(3)	
		
def static(contract_code):# 获得账户持仓量，现价，保证金比例，强平价格，当前btc量，BTC营收比例，当前现金，现金营收比例
	global msg_list
	#print(dm.contract_account_position_info("BTC"))
	btc_init=3
	cost_init=5060

	try:

		if len(msg_list)>5:
			msg_list=msg_list[3:len(msg_list)]

		res=dm.contract_account_position_info("BTC")
		if res['status']=='ok':
			res=res['data'][0]
		
		margin_balance=res['margin_balance'] if res['margin_balance'] is not None else 0
		risk_rate=res['risk_rate'] if res['risk_rate'] is not None else 0
		liquidation_price=res['liquidation_price'] if res['liquidation_price'] is not None else 0
		positions=res['positions'] if res['positions'] is not None else ''
		#print(positions)
		buy_last_price=''
		buy_volume=''
		buy_available=''
		sell_last_price=''
		sell_volume=''
		sell_available=''
		for r in positions:
			if r['contract_code']==contract_code and r['direction']=='buy':
				#print(r['last_price'])
				buy_last_price=r['last_price']
				buy_volume=r['volume']
				buy_available=r['available']
			if r['contract_code']==contract_code and r['direction']=='sell':
				#print(r['last_price'])

				sell_last_price=r['last_price']
				sell_volume=r['volume']
				sell_available=r['available']


		result='当前合约持仓= '+str(round(margin_balance,4))+'\n'
		result+='当前保证金率= '+str(round(risk_rate,4))+'\n'
		result+='当前强平价格= '+str(round(liquidation_price,5))+'当前价格= '+str(sell_last_price)+  '\n'
		result+='当前BTC盈利百分比= '+str(int(margin_balance/btc_init*100-100))+'%\n'
		result+='当前多空手数= buy '+str(buy_volume)+' sell '+str(sell_volume)+' \n'
		result+='当前多空持仓= buy '+str(buy_available)+' sell '+str(sell_available)+' \n'
		#print(result)
		result={}
		result['当前合约持仓']=str(round(margin_balance,4))
		result['当前保证金率']=str(round(risk_rate,4))
		result['当前强平价格']=str(round(liquidation_price,5))
		result['当前价格']=str(buy_last_price)
		#result['当前BTC盈利百分比']=str(int(margin_balance/btc_init*100-100))+'%'
		result['当前多空手数']='buy '+str(buy_volume)+' sell '+str(sell_volume)
		#result['当前多空持仓']='buy '+str(buy_available)+' sell '+str(sell_available)
		result['time']=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		#print(3,result)
		msg_list.append(result)

		if len(msg_list)>2:
				
			if msg_list[len(msg_list)-1]['当前多空手数']!=msg_list[len(msg_list)-2]['当前多空手数']:
				print('trading- ',str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
				print('old',msg_list[len(msg_list)-2]['当前多空手数'])
				print('new',msg_list[len(msg_list)-1]['当前多空手数'])
				send_mail("report warning list","".join('old'+str(msg_list[len(msg_list)-2]['当前多空手数'])+'new'+msg_list[len(msg_list)-1]['当前多空手数']))


	except :
		print(str('error'))

	#print(33,msg_list)
	# res=''
	# page_index=1
	# res=dm.get_contract_open_orders(symbol='BTC',page_index=str(page_index))
	# if res['status']=='ok':
	# 	orders=res['data']['orders']

	# while page_index<int(res['data']['total_page']):
	#  	page_index+=1
	#  	res=''
	#  	res=dm.get_history_orders(symbol='BTC',page_index=str(page_index))
	#  	if res['status']=='ok':
	#  		orders+=res['data']['orders']
	#  	else:
	#  		page_index=page_index-1
	 	

	# # buy_=[]
	# # sell=[]
	# df=pd.DataFrame.from_dict(orders)
	# # #df=df[(df['order_id']==656581740190896128)]
	# # df.eval('本金_BTC=100/trade_price',inplace=True)
	# # df.eval('手续费比例=trade_fee/本金_BTC',inplace=True)

	# df=df.groupby(['direction','offset']).max()
	# print(df)

def send_mail(sub,content):  

    mail_host="smtp.qq.com"  #设置服务器
    mail_user="58254451"    #用户名
    mail_pass="eiwgkmguzeorbggb"   #口令 
    mail_postfix="qq.com"  #发件箱的后缀
	   

    to_list=["58254451@qq.com"]
    me="<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    print(msg.as_string())
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print (str(e))  
        return False  

def trading_deal(contract_code,dis_,volume_,lever_rate_):# 获取价格并处理 （挂单、查挂单、查成交，查价格）
	
	# 2020-5-28 改为每次开单记录订单号、预期价格等，查询单个订单来判断是否重新开仓等
	# step1、init的时候记录init的订单号
	# step2、每次轮询这些订单的状态


	global trades_list

	print('start',str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))

	#2020-05-15 考虑到有部分成交的可能
	#获取历史订单接口返回的df后，按照order_id 分组求和订单数
	#merge 分组后和分组前的数据，然后去重 生成新的df，不包含拆单数据的部分
	#以不拆单的数据进行后续计算

	df_history_orders=LH_get_history_orders(contract_code)#获取历史成交的订单
	df_=df_history_orders[['trade_volume','order_id']].groupby(['order_id']).sum()
	df_.columns=['trade_volume_clac']
	df_=pd.merge(df_,df_history_orders,how='right',on='order_id')[['order_id_str','direction','trade_volume_clac','trade_price','offset','contract_code']]
	df_history_orders=df_.drop_duplicates()



	#df_contract_open_orders=LH_get_contract_open_orders(contract_code)#获取当前仍然挂着的订单
	print('end',str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))

	print('step2',len(trades_list))
	try:
		if len(trades_list)>2:
			df_orders_sub=[]


			trade_id=trades_list[len(trades_list)-1]['order_id_str'].tolist()

			df_orders_sub=df_history_orders[~df_history_orders['order_id_str'].isin(trade_id)]
			#print(df_history_orders,2)
			#print(df_orders_sub,4)
			
			if df_orders_sub.shape[1]>0:
				print(df_orders_sub)
				# book=dm.contract_account_position_info("BTC")#获取当前持仓
				# sell_volume=''#防止接口返回不是ok，误判
				# buy_volume=''#防止接口返回不是ok，误判
				# if book['status']=='ok':
				# 	book=book['data'][0]
				# 	sell_volume=0
				# 	buy_volume=0
				# 	positions=book['positions'] if book['positions'] is not None else ''
				# 	for r in positions:
				# 		if r['contract_code']==contract_code and r['direction']=='buy':
				# 			buy_volume=r['volume']
				# 		if r['contract_code']==contract_code and r['direction']=='sell':
				# 			sell_volume=r['volume']

				for item  in df_orders_sub.iterrows():
					
					if item[1]['offset']=='close' and item[1]['direction']=='sell' and item[1]['trade_volume_clac']==volume_:    #平多，sell-100 开多
									print(item[1]['trade_price']+dis_,1)
									dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']-dis_, volume=volume_, direction='buy', offset='open',lever_rate=lever_rate_, order_price_type='limit')
									

					if item[1]['offset']=='close' and item[1]['direction']=='buy' and item[1]['trade_volume_clac']==volume_:    #平空，buy+100 开空
									print(item[1]['trade_price']-dis_,2)
									dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']+dis_, volume=volume_, direction='sell', offset='open',lever_rate=lever_rate_, order_price_type='limit')
		
					if item[1]['offset']=='open' and item[1]['direction']=='sell' and item[1]['trade_volume_clac']==volume_:    #开空 ，sell-100 平空 open close 代表平空
									print(item[1]['trade_price']-dis_,3)
									dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']-dis_, volume=volume_, direction='buy', offset='close',lever_rate=lever_rate_, order_price_type='limit')
									#dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']-dis_, volume=volume_, direction='buy', offset='open',lever_rate=lever_rate_, order_price_type='limit')
									
					if item[1]['offset']=='open' and item[1]['direction']=='buy' and item[1]['trade_volume_clac']==volume_:    #开多，buy+100 平多  # sell close 代表平多
									print(item[1]['trade_price']+dis_,4)
									dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']+dis_, volume=volume_, direction='sell', offset='close',lever_rate=lever_rate_, order_price_type='limit')
									#dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']+dis_, volume=volume_, direction='sell', offset='open',lever_rate=lever_rate_, order_price_type='limit')
		
					# #2020-05-19 增加双向开单实验

					# # 开空 且 持仓没有多 那么多挂一个开多
					# if buy_volume==0 and  item[1]['offset']=='open' and item[1]['direction']=='sell' and item[1]['trade_volume_clac']==volume_: 
					# 				print(item[1]['trade_price']+dis_,1)
					# 				dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']-dis_, volume=volume_, direction='buy', offset='open',lever_rate=lever_rate_, order_price_type='limit')
					# # 开多 且 持仓没有空 那么多挂一个开空
					# if sell_volume==0 and item[1]['offset']=='open' and item[1]['direction']=='buy' and item[1]['trade_volume_clac']==volume_: 
					# 				print(item[1]['trade_price']-dis_,2)
					# 				dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=item[1]['trade_price']+dis_, volume=volume_, direction='sell', offset='open',lever_rate=lever_rate_, order_price_type='limit')


		trades_list.append(df_history_orders)

		if len(trades_list)>5:
			trades_list=trades_list[len(trades_list)-3:len(trades_list)]





	except Exception as e:
		print(e)
		print('trading deal init error')
		raise e

	#step1 初始化 -- 就当前价格，上下加距离，生成1个 挂单列表，判断没有挂单的时候挂上去，不需要一开始开太多
	# try:

		# ask_price=''
		# bid_price=''
		# res=dm.get_contract_market_merged(symbol='BTC_CQ')#这比较操蛋，如果换季需要调整
		# if res['status']=='ok':
		# 	ask_price=res['tick']['ask'][0]
		# 	bid_price=res['tick']['bid'][0]

	# 	contract_open_orders_init=df_contract_open_orders.shape[1]
	# 	if contract_open_orders_init==0:
	# 		for x in range(1,len_+1):
	# 			contract_open_list.append(int((ask_price+bid_price)/2)+dis_*x)
	# 			contract_open_list.append(int((ask_price+bid_price)/2)-dis_*x)
	# 		datetime_=str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
	# 		print(contract_open_list)
	# 	for r in contract_open_list:
	# 		if r>int((ask_price+bid_price)/2):
	# 			dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code=contract_code,price=r, volume=volume_, direction='sell', offset='open',lever_rate=lever_rate_, order_price_type='limit')
	# 		else:
	# 			dm.send_contract_order(  symbol='BTC', contract_type='333',client_order_id='',contract_code=contract_code,price=r, volume=volume_, direction='buy', offset='open',lever_rate=lever_rate_, order_price_type='limit')
	# except Exception as e:
	# 	print(e)
	# 	print('trading deal deal_contract_order error')
	# 	raise e
	


	## 获得最近成交的单子，拿到价格，比如原先是6200 和6400 ，最近发现6400成交，又发现6400的挂单没有了，挂6300开多，挂6300平空
	# 只有单向手数大于1的时候，才挂平
	# 原来是 6200 ，6400 ，6500
    # 什么情况开多，开空，平多，平空

    #获取尽三日左右成交，对比上次所有成交，多出来的拿出来
    #拿出来后和list对比，如果开单成交是 6300，那么改变list
    #如果平单不多扩充list




    #在成交组成的list的那个单价上方挂空
    #在成交组成的list的那个单价下放开空
    #在成交组成的list那个单下放挂平空，volume=1永远不平
    #在成交组成的list那个单上方挂平多，volume=1永远不平


    #拿到平单成交记录，每个成交的，都应该在上下挂单，6100成了多单，那应该在6000 开多，6200平空，6200开空
    #												 6400 成了多单，那么应该在6300开多，6300平空，6500平多，6500开空
    #若果同等价格已经有的不挂

	####step2 获取挂单的内容、成交监测、和当前价格比较、看差异，决定怎么添加挂单

	# if len(msg_list)>2:
			
	# 	if msg_list[len(msg_list)-1]['当前多空手数']!=msg_list[len(msg_list)-2]['当前多空手数']:
	# 		print('trading- ',str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	# 		print('old',msg_list[len(msg_list)-2]['当前多空手数'])
	# 		print('new',msg_list[len(msg_list)-1]['当前多空手数'])
	# 		send_mail("个人报警BTC报警","".join('old'+str(msg_list[len(msg_list)-2]['当前多空手数'])+'new'+msg_list[len(msg_list)-1]['当前多空手数']))





if __name__ == '__main__':

	trade_p=trading_auto('BTC200626',10,1,20,5,'init')#品种、距离、手数、杠杆、网格大小,是否创建初始单

	while 1:
		time.sleep(2)
		trade_p.trading_deal()
		#static('BTC200626') # 统计一个线程
				#	 紧急止盈止损一个线程

# 	print('start',str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
#	res=dm.get_contract_order_detail('BTC', order_id='715489532950429696',order_type='1',created_at='1590632320428')
# 	#print(res)

# 	res=dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='', contract_code='BTC200626',price='9150', volume=2, direction='sell', offset='open',lever_rate=20, order_price_type='limit')
# 	if res['status']=='ok':
# 		order_id=res['data']['order_id']
# 		ts=res['ts']
# 	res=''
# 	print(order_id,ts)
# # 		#order_id=''
# # 	print('end',str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))
# # #715561992793997312 1590644873589
# # 	print(dm.get_contract_order_detail('BTC', order_id='715561992793997312',order_type='1',created_at='1590644873589'))
# # 	print('end',str((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')))

# 	#dm.send_contract_order( symbol='BTC', contract_type='333',client_order_id='20200528143030_9300_1', contract_code='BTC200626',price='9182' volume='1', direction='buy', offset='close',lever_rate=20, order_price_type='limit')
# 	#init的时候返回 order_id list


# 	# order_id={}
# 	# order_id['333']='ts33'
# 	# order_id['44']='ts44'
# 	# while 1:
# 	# 	time.sleep(1)
# 	# 	print(4)
	

# 	# 	for k in list(order_id.keys()):
# 	# 		print(k)
# 	# 		order_id.pop(k)
	#715489532950429696 1590632320428

	#print(LH_get_history_orders('BTC200626'))