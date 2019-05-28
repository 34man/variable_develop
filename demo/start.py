# ！/usr/bin/env/python
# coding: utf-8

"""
@File       :start.py
@auth       :sx
@Date       :2019/5/23
@Desc       :
"""

import sys
import pandas as pd
import numpy as np

sys.path.append('/data/proj/exdata/00.analysis/variable_develop')
import os

os.getcwd()
os.chdir("/data/proj/exdata/00.analysis/variable_develop")
from variables.hive_data import load_data, delete_a
from demo.variable import variable

sql = """
select * from (
    select  detail.id_file,
            detail.net_way,
            detail.net_type,
            detail.start_time,                      
            detail.fee,                             
            detail.total_time,
            detail.business_name,
            detail.total_traffic,
            summary.time_crawl
        from ods.ods_udw_sctx_data_product_waf09zz01_netflow_detail_compressed detail inner join 
                  ods.ods_udw_sctx_data_product_waf09zz01_operator_summary summary on detail.id_file = summary.id_file
)a limit 20000
"""

df_raw = load_data(sql)
df_raw = delete_a(df_raw)
len(np.unique(df_raw['id_file']))
df_raw.to_csv("raw.csv", index=False)
df_raw = pd.read_csv("raw.csv")

df_batch1 = variable(df_raw, 1)
df_batch1.to_csv("df_batch1.csv", index=False)
df_batch1 = pd.read_csv("df_batch1.csv")

df_batch2 = variable(df_batch1, 2)
df_batch2.to_csv("df_batch2.csv", index=False)

dfs = pd.read_csv("dfs.csv")
dfs['status'].value_counts()
df_batch3 = variable(dfs, 3)






# df = {"A": [1.12, 2123213, 3, 4, 5]}
# df = pd.DataFrame(df, index=[1])
# dfs = pd.read_csv('dfs.csv')
#
# dfs[dfs['dur_time'] == '1m'].shape
#
Employees = {
    'Employee': ['Jon', 'Mark', 'Tina', 'Maria', 'Bill', 'Jon', 'Mark', 'Tina', 'Maria', 'Bill', 'Jon', 'Mark', 'Tina',
                 'Maria', 'Bill', 'Jon', 'Mark', 'Tina', 'Maria', 'Bill'],
    'Sales': [1000, 300, 400, 500, 800, 1000, 500, 700, 50, 60, 1000, 900, 750, 200, 300, 1000, 900, 250, 750, 50],
    'Quarter': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4],
    'Country': ['US', 'Japan', 'Brazil', 'UK', 'US', 'Brazil', 'Japan', 'Brazil', 'US', 'US', 'US', 'Japan', 'Brazil',
                'UK', 'Brazil', 'Japan', 'Japan', 'Brazil', 'UK', 'US']
    }


import pandas as pd
import numpy as np
df = pd.DataFrame(Employees, columns=['Employee', 'Sales', 'Quarter', 'Country'])

# df_test = pd.DataFrame(index=np.unique(df['Employee']), columns=["top薪水国家"])
#
# df_test["top薪水国家"] = df["Country"]
#
# df.sort_values(by=["Employee", 'Sales'], inplace=True)
# df.drop_duplicates(subset=['Employee'], keep='last', inplace=True)

df['age'] = np.nan
df.loc[0, 'age'] = 23
df.set_index('Employee', inplace=True)
df2 = df.pivot_table(index=['Country'], values=['age'], aggfunc=np.mean)['age']
for c1, c2 in zip(df2['Country'], df2['Sales']):

    var = df[(df['Country'] == c1) & (df['Sales'] == c2)].Employee


df3 = pd.DataFrame(columns=['Sales'], index=np.unique(df['Name of Employee']))
