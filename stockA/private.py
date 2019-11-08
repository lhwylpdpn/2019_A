# !/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import os


class deal_data: #交易数据类
    def __init__(self):
        self.data=pd.DataFrame()
    def get_csv_deal_ht_normal(self):#获取华泰所有交易数据_正常账户
        filelist=[]
        for root, dirs, files in os.walk(os.getcwd()+"\\data_normal\\"):
            filelist=files
        for file in filelist:
            self.data =self.data.append(pd.read_csv(os.getcwd()+"\\data_normal\\"+file))


    def get_csv_deal_ht_Margin(self):#获取华泰所有交易数据_保证金账户
        pass

    def merge_clac(self):#执行计算交易数据
        pass

    def get_result(self):
        return  self.data
class market_data: #行情数据类


    def __init__(self):
        self.data_=''#接口返回的所有

    def get_market_data_date(self, object_id,date):#获取日数据
        pass

    def get_market_data_all(self, object_id):  # 获取所有历史
        pass

class report_: #各类要出的图形,调用各类函数直接生成图，呈现
    def __init__(self):
        pass

class clac_analysis: #各类计算、统计，调用各类函数，直接返回dataframe
    def __init__(self):
        pass




if __name__ == '__main__':
    deal_=deal_data()
    deal_.get_csv_deal_ht_normal()
    test=deal_.get_result()

    print test
