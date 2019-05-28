# ！/usr/bin/env/python
# coding: utf-8

"""
@File       :check_python.py
@auth       :sx
@Date       :2019/5/27
@Desc       : 用于检验变量构造代码是不是能处理复杂数据，及代码处理过的数据是不是正确的
"""
import sys
import pandas as pd
import numpy as np
import os
sys.path.append('/data/proj/exdata/00.analysis/variable_develop')


os.chdir("/data/proj/exdata/00.analysis/variable_develop")
from variables.hive_data import load_data, delete_a
from demo.variable import variable

# 1、先判断处理一条数据和处理多条数据是不是结果一致
df_raw = pd.read_csv("raw.csv")

df_raw['id_file'].value_counts()
# 1.1、 先对批量数据进行处理

df_batch1 = variable(df_raw, 1)
# 1.2 再对第二批变量进行处理挑选id_file 为一致的数据
df_raw = df_raw[df_raw['id_file'] == "0054d1baf1064de6a043eca88c4877c5"]
df_batch12 = variable(df_raw, 1)

# 对一堆生成的和一条生成的变量进行对比
df_batch1 = df_batch1[df_batch1.index == "0054d1baf1064de6a043eca88c4877c5"]
# 对比的结果全是nan

# 2.1 自己构造一组数据进行测试
import random

df_raw = pd.DataFrame({'id_file': [0, 0, 0, 3, 4, 5, 6, 7, 8, 9],
                       "start_time": ['2018-10-23 01:23:12',
                                      '2018-10-24 01:23:12',
                                      '2018-10-25 01:23:12',
                                      '2018-10-26 01:23:12',
                                      '2018-10-27 01:23:12',
                                      '2018-10-28 01:23:12',
                                      '2018-10-29 01:23:12',
                                      '2018-10-1 01:23:12',
                                      '2018-10-3 01:23:12',
                                      '2018-10-2 01:23:12'],
                       "time_crawl": ['2018-8-23 01:23:12',
                                      '2018-8-24 01:23:12',
                                      '2018-8-25 01:23:12',
                                      '2018-8-26 01:23:12',
                                      '2018-8-27 01:23:12',
                                      '2018-9-28 01:23:12',
                                      '2018-6-29 01:23:12',
                                      '2018-7-1 01:23:12',
                                      '2018-3-3 01:23:12',
                                      '2018-7-2 01:23:12'],
                       "net_way": ["无线", '4', '3', "彩信", np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                       "business_name": ['套餐', '包', '定向', '集团', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                       "fee": [2.3, 0.03, 0.24, 0.3, 0, 0, 12, 100000, 23, 9090],
                       'total_traffic': [1231, 0, 323424, 23424, 546, 8089, 234, 0, 123, 6780],
                       'total_time': [random.random() * 3600] * 10
                       })


df_batch1 = variable(df_raw, 1)
dfs = pd.read_csv("dfs.csv")
list(df_batch1)

df_batch2.to_csv("df_batch2.csv", index=False)

dfs = pd.read_csv("dfs.csv")
dfs['status'].value_counts()
df_batch3 = variable(dfs, 3)


