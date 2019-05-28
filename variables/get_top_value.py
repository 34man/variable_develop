# ！/usr/bin/env/python
# coding: utf-8

"""
@File       :get_top_value.py
@auth       :sx
@Date       :2019/5/27
@Desc       :
"""
import pandas as pd


def get_top_value(df, cal_col, get_col, top=1):
    """
    本方法计算数据框df中cal_col计算为top 几的 get_col 的值
    :param df: 数据框
    :param cal_col: 计算前几的列名
    :param get_col: 想拿到的列名 ，目前只能为1
    :param top:top 表示前几的值
    :return: 数据框
    """
    df.sort_values(by=["id_file", cal_col], ascending=False, inplace=True, na_position="last")
    if top == 1:
        df.drop_duplicates(subset=['id_file'], keep='first', inplace=True)
        return df[["id_file", get_col]]

