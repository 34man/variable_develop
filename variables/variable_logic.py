# ！/usr/bin/env/python
# coding: utf-8

"""
@File       :variable_logic.py
@Copyright  :sx
@Date       :2019/4/28
@Desc       :存储变量名和逻辑（变量名字组成的顺序）
"""


def get_logic(key):
    """
    获取变量命名规则
    :return:返回变量命名规则以及变量的分类
    """
    logic = {
        'order': ['perfix', "dur_time", 'start_time', "status", "fee", "total_time", "total_traffic", "net_way",
                  "business_name", "object", "cal_way"],
        'class': {
            'perfix': ["ba1_"],
            "cal_way": ["C", "M", "L", "A", "V", "S", "D"],
            "object": ["TS", "F", "D", "TT", "N"],
            "dur_time": ['00', '1d', '3d', '7d', "1m", "2m", "3m", "4m", "6m"],
            "status": ["d", "e", "h"],
            "fee": ['01Y', '10Y', '33Y', '160Y', '160YS'],
            "net_way": ['fi', '4G', 'mo', 'new', 'sh', 'ki', 'ec', 'ga'],
            "start_time": ['1', '2', '3', '4', '5'],
            "total_time": ['1h', '2h', '3h', '4h', '5h'],
            "total_traffic": ['2mb', '27mb', '166mb', '166mbs'],
            "business_name": ['1', '2', '3', '4', "5"]
        }
    }
    return logic.get(key)


def get_logic3(key):
    """
    获取变量命名规则
    :return:返回变量命名规则以及变量的分类
    """
    logic = {
        'order': ['top', "dur_time", "status", "net_way", "total_traffic", "get_val"],
        'class': {
            'top': ["top1"],
            "object": ["TS", "F", "D", "TT", "N"],
            "dur_time": ['00', '1d', '3d', '7d', "1m", "2m", "3m", "4m", "6m"],
            "status": ["d", "e", "h"],
            "fee": ['01Y', '10Y', '33Y', '160Y', '160YS'],
            "net_way": ['fi', '4G', 'mo', 'new', 'sh', 'ki', 'ec', 'ga'],
            "start_time": ['1', '2', '3', '4', '5'],
            "total_time": ['1h', '2h', '3h', '4h', '5h'],
            "total_traffic": ["TT"],
            "get_val": ["N"],
            "business_name": ['1', '2', '3', '4', "5"]
        }
    }
    return logic.get(key)
