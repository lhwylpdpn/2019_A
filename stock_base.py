#!/usr/bin/python
# -*- coding: UTF-8 -*- 



import os
import sys
import time
import csv
import sys
import datetime
import os
import shutil
import re
import time
import tushare as ts
import pandas as pd
import numpy as np
def return_dis(n):
	dis=[]
	if n==0:
		return dis
	if n==1:
		return [1]
	if n==2:
		return [1,1] 
	if n>2:
		dis.append(1)
		dis.append(1)
		for x in xrange(2,n):
		
				dis.append(dis[len(dis)-1]+dis[len(dis)-2])
	return dis


def getEveryDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def clac(A,x,n,m):

	res=return_dis(n-m)
	res2=return_dis(n)
	sum_cost=0
	sum_lost=0
	for _ in xrange(1,len(res)+1):
		sum_cost+=(A-(_-1)*x)*res[_-1]
		sum_lost+=res[_-1]*(len(res)-_)*x

	print  sum(res2[-2:])-sum_lost/x



def clac2(A,x,n,m):

	res=return_dis(n-1)
	res2=return_dis(n)
	sum_cost=0
	sum_lost=0
	for _ in xrange(1,len(res)+1):
		sum_cost+=(A-(_-1)*x)*res[_-1]
		sum_lost+=res[_-1]*(len(res)-_)*x

	print  sum(res2[-1:])*m-sum_lost/x


def get_data(startdate,enddate):
	df=ts.get_k_data('159915',start=startdate,end=enddate)
	#list_=df.loc['2019-06-17'].tolist()
	print df
	return df
	#print df.values.tolist()[0]
	#return df[['high','low']] 


	# date：日期
	# open：开盘价
	# high：最高价
	# close：收盘价
	# low：最低价
	# volume：成交量
	# price_change：价格变动
	# p_change：涨跌幅
	# ma5：5日均价
	# ma10：10日均价
	# ma20:20日均价
	# v_ma5:5日均量
	# v_ma10:10日均量
	# v_ma20:20日均量
	# turnover:换手率[注：指数无此项]
def clac(dis,startdate,enddate,Accuracy):
#模拟计算，计算所有天假设每个价格都准确执行了规则
#那么按照一定距离去执行，最终的成功失败分布是什么样？
#如果每个点位都执行这个策略，最终所有点位的成功失败是什么样？
#要区分是否只有隔天才可以交易


	result_=[]
	res=[]
	data=get_data(startdate,enddate)
	#date_list=data._stat_axis.values.tolist() #获取行名称
	#print data.columns.values.tolist() #获取列名称
	date_list=data['date'].tolist()
	
	data_dict={}
	for date in date_list:
		data_dict[date]=data[data['date']==date]
	
	for key in sorted(data_dict,reverse=False):
		#print data_dict[key]
		#取最高和最低之间的每个价格建仓
		open_=[]
		
		open_.append(data_dict[key]['low'].values[0])

		while data_dict[key]['high'].values[0]-Accuracy>=open_[len(open_)-1]:
			open_.append(open_[len(open_)-1]+Accuracy)
		print key ,open_
	# for date in date_list:

	# 		print data.loc[date].tolist()


	# res.append(int(float(data_[line][4])))  #这个line的最低价
	 
	# for x in xrange(int(float(data_[line][4]))+1,int(float(data_[line][3]))+1): #在这个line的最低到最高期间
	# 		res.append(x) # 总共可能产生这些个价格
	 
	# for r in res: #在区间价格内，总共找到n个价格
	# 	open_=r #每个价格开始往后看到数据收尾
	# 	i=0
	# 	open_end=len(data_)
	# 	success_='没平仓'
	# 	for line_clac in xrange(line,len(data_)):

	# 		if int(float(data_[line_clac][4]))+dis<open_: #   如果在这些价位内,向下跌出了一个dis的距离,开仓价格等于这个更低的价格
	# 			open_=int(float(data_[line_clac][4]))
	# 			i+=1 # 并且开仓次数加1
	# 		if int(float(data_[line_clac][3]))-dis>open_:
	# 			open_end=line_clac #回撤就标记结束位置
	# 			success_='成功平仓'#标记成功关仓了
	# 			break;
		
	# 	t=np.array(data_[line:open_end+1])# 
	# 	if len(t)==0:
	# 		print(line,open_end,len(data_[line:open_end]),success_)
			
	# 	#print(t.shape)
	# 	#print(str(float(max(t[:,3]))-float(min(t[:,4])))+","+str(len(t))+","+str(i))
	# 	result_.append((str(line)+","+str(data_[line][0])+","+str(data_[line][4])+","+str(float(max(t[:,3]))-float(min(t[:,4])))+","+str(len(t))+","+str(i)+","+str(success_)).split(","))
	# return result_ # 返回每个价格后续的几个数字，平仓前的最价格，最低价，经历了多久，最多补过几次仓


def test():
	pro=ts.pro_api()
	data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
	print data
if __name__ == '__main__':
	# for n in xrange(1,20):
	#test()
	clac(3,'2019-06-01','2019-06-17',0.02)
	#print t
	# 选择产品单说
	# 进场时机单说
	#======>给入 x
	# 历史很长时间出现连续n次不回2x的概率？
	# 历史很长时间出现连续n次不回x的概率？

	# ====> 根据不同风险接受度，推导出最大距离max_dis=n*x


	# price_in # 进场价格
	# dis      # 间距
	# price_out # 出厂价格
	# all_cost # 总成本
	# n # 应该可以承受多少次补位
	# x # 最小单位

	# 规则等于：
	# 0、给入 dis
	# 1、历史数据根据dis计算出n
	# 2、资金量money / n = 最小开单单位x
	# 3、x单位开 ：3次顶端单次回头出    2个连续回头出
	# 4、突破箱体只能等还是认怂



# def 选产品(参考周期):


# def 计算历史的n(参考周期2)：
# 	return n

# def 计算最小开仓单位(资金数):
# 	return x


# def 回测如果用n开单的结果分布(参考周期，n):


