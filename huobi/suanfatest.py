#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
def BTCduo(prices,dis):
	open_=[]
	num_=[]
	benjin=[]
	open_.append(prices[0])
	num_.append(1)
	benjin.append(num_[0]*prices[0])
	shouyi=[]
	money=[]
	money.append(0)
	n=[1,1,2,3,5,8,13,21,34,55,89,144,233]
	i=0
	for p in prices[1:]:
		# print(p)
		# print(open_[-1])
		# print(",")
		if p<=open_[-1]-dis:
			i+=1
			open_.append(p)
			num_.append(n[i])
			benjin.append(p*n[i])
		if p>=open_[-1]+dis and sum(num_)>1:
			i=i-1
			shouyi.append(dis*num_[-1])
			open_.pop()
			num_.pop()
			benjin.pop()
		if p>=open_[-1]+dis and sum(num_)==1:
			open_[0]=p
		money.append(-sum(benjin)+sum(num_)*p+sum(shouyi))
	print(money)
	return(money)
	# print("num_",num_)
	# print("open_",open_)
	# print("xianjin",shouyi,sum(shouyi))
	# print("hejiliun",sum(num_)*prices[-1]-sum(benjin)+sum(shouyi))


def BTCkong(prices,dis):
	open_=[]
	num_=[]
	benjin=[]
	open_.append(prices[0])
	num_.append(1)
	benjin.append(num_[0]*prices[0])
	shouyi=[]
	money=[]
	n=[1,1,2,3,5,8,13,21,34,55,89,144,233]
	i=0
	money.append(0)
	for p in prices[1:]:
		# print(p)
		# print(open_[-1])
		# print(",")
		if p>=open_[-1]+dis:
			i+=1
			open_.append(p)
			num_.append(n[i])
			benjin.append(p*n[i])
		if p<=open_[-1]-dis and sum(num_)>1:
			i=i-1
			shouyi.append(dis*num_[-1])
			open_.pop()
			num_.pop()
			benjin.pop()
		if p<=open_[-1]-dis and sum(num_)==1:
			open_[0]=p
		money.append(sum(benjin)-sum(num_)*p+sum(shouyi))
	print(money)
	return(money)

if __name__ == '__main__':
	# prices=[]
	# prices.append(10000)

	# for x in xrange(1,10):
	# 	prices.append(prices[-1]-100)
	# for x in xrange(1,10):
	# 	prices.append(prices[-1]+100)
																																

	# res=[]
	# reskong=BTCkong(prices,100)
	# resduo=BTCduo(prices,100)
	# print("------------")
	# print(prices)
	# print("&&&&&&&&&&&&&&&&")
	# for x in xrange(0,len(reskong)):
	# 	res.append(resduo[x]+reskong[x])
	# print(res)
	# print("********************")
	n=[1,1,2,3,5,8,13,21,34,55,89]
	x=0.01*sum(n)
	print(len(n))
