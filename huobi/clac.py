#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import os
import sys
import time
import datetime
import os



#该不该继续加仓,什么时候停止--- 已知：可能下行的距离，最大多少钱，求加仓的手数，加到什么时候就不能加了


def get_continue_limit():#(dis_price,now_num,now_price,avg_price,money_alllist,numlist):

	money=100
	num=20
	dis_price=3200
	avg_price=9497
	now_num=60
	limit_price=3678
	now_price=9530

	BTC_all=1
	


	
	0.7now_num/(BTC_all+(1/avg_price-1/limit_price)*100*now_num)=limit_price
	return res
if __name__ == '__main__':
	print(get_continue_limit())


	limit_price=0.7now_num/BTC_all+0.7/100/(1/avg_price-1/limit_price)