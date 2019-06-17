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


def get_data():
	df=ts.get_hist_data('159915')
	list_=df.loc['2019-06-17'].tolist()
	print list_
	#print df.values.tolist()[0]
	#return df[['high','low']] 
def clac(pds):#模拟计算 计算某一行后续的效果
	global data_
	result_=[]
	
	dis=3 #
	res=[]
	open_=""
	open_end=""
	res.append(int(float(data_[line][4])))  #这个line的最低价
	 
	for x in xrange(int(float(data_[line][4]))+1,int(float(data_[line][3]))+1): #在这个line的最低到最高期间
			res.append(x) # 总共可能产生这些个价格
	 
	for r in res: #在区间价格内，总共找到n个价格
		open_=r #每个价格开始往后看到数据收尾
		i=0
		open_end=len(data_)
		success_='没平仓'
		for line_clac in xrange(line,len(data_)):

			if int(float(data_[line_clac][4]))+dis<open_: #   如果在这些价位内,向下跌出了一个dis的距离,开仓价格等于这个更低的价格
				open_=int(float(data_[line_clac][4]))
				i+=1 # 并且开仓次数加1
			if int(float(data_[line_clac][3]))-dis>open_:
				open_end=line_clac #回撤就标记结束位置
				success_='成功平仓'#标记成功关仓了
				break;
		
		t=np.array(data_[line:open_end+1])# 
		if len(t)==0:
			print(line,open_end,len(data_[line:open_end]),success_)
			
		#print(t.shape)
		#print(str(float(max(t[:,3]))-float(min(t[:,4])))+","+str(len(t))+","+str(i))
		result_.append((str(line)+","+str(data_[line][0])+","+str(data_[line][4])+","+str(float(max(t[:,3]))-float(min(t[:,4])))+","+str(len(t))+","+str(i)+","+str(success_)).split(","))
	return result_ # 返回每个价格后续的几个数字，平仓前的最价格，最低价，经历了多久，最多补过几次仓

if __name__ == '__main__':
	# for n in xrange(1,20):
	# 	clac2(1.5,0.02,n,3)
	t=get_data()
	#print t
	# #进场时机单说
	# 历史很长时间出现连续n次不回2x的概率？
	# 历史很长时间出现连续n次不回x的概率？

	# xxxxx=计算出你这次能承受的距离

	# xxxx/dis=n

	# price_in # 进场价格
	# dis      # 间距
	# price_out # 出厂价格
	# all_cost # 总成本
	# n # 应该可以承受多少次补位
	# x # 最小单位

	# 规则等于：
	# 1、历史数据计算出n
	# 2、根据n 计算出 x
	# 3、x开 ：3次顶端回 出  2个回头出
	# 4、突破箱体只能等还是认怂


	# E=事件A*pA + 事件B * pb

	#   连续下撤突破最多的概率A * PA + 可以盈利的b*PB  

	#   可以选历史上出现 A的概率分布，判断后面时间内出现的可能

