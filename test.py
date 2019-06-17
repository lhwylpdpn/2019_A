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


def test():
	pds=ts.get_hist_data('159915')
	print(pds)

if __name__ == '__main__':
	# for n in xrange(1,20):
	# 	clac2(1.5,0.02,n,3)
	test()