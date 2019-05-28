# ！/usr/bin/env/python
# coding: utf-8

"""
@File       :dismatch_var_name.py
@auth       :sx
@Date       :2019/4/30
@Desc       : 拆分变量名的方法存放在这里,第一批第二批拆分的方法在variable.py中,不动了这里是第三批的方法
"""

from variables.variable_logic import get_logic3


def dismantle_var3_name(name):
    """
    参数是第三批变量的变量名,这个方法把变量名拆分成可以处理的{name:[时间维度, 上网方式, top几, 分组对象, ]}
    :param name:
    :return:
    """
    order = get_logic3("order")
    classes = get_logic3("class")
    name_temp = name
    sign = []
    for var in order:
        # print(var)
        li = classes.get(var)
        for ele in li:
            n, name_temp = start_delete(name_temp, ele)
            if isinstance(n, str):
                break
            if n == 0:
                break
        sign = sign + [n]
    print({name: sign})
    return {name: sign}



def ifinclude(li, string):
    """
    判断一个字符串中是否包含li中的字符串,
    :param li:
    :param string:
    :return: 1 找到了， 0 没找到
    """
    if isinstance(li, list):
        for var in li:
            if string.find(var) != -1:
                return 1
        return 0
    elif isinstance(li, str):
        if string.find(li) != -1:
            return 1
    return 0


def start_delete(string, word):
    """
    判断是不是有一个单词能开始以一个word，或者是以w开始的，以w开始的便返回0，并且删掉w，以单词开始的返回1并且删掉word
    :param string: 一段单词
    :param word: 要判断的单词
    :return: 0和1 以及返回的被截掉的string，如果没有找到，返回2和原来的单词
    """
    if string.startswith("w"):
        return 0, string[1:]
    if string.startswith(word):
        return word, string[len(word):]
    else:
        return 1, string


def name_to_dict(name, order, classes):
    """
    将输入的变量名变成以变量名为key，0为空，不为空便是该变量要素的分类
    :param name: 变量名
    :param order: 变量名的命名排序
    :param classes: 每个变量的分类
    :return: 一个字典
    """
    name_temp = name
    sign = []
    for var in order:
        # print(var)
        li = classes.get(var)
        for ele in li:
            n, name_temp = start_delete(name_temp, ele)
            if isinstance(n, str):
                break
            if n == 0:
                break
        sign = sign + [n]
    return {name: sign}


def dismantle_var2_name(name):
    """
    第二批的变量名有net_1----打头_net------,这个方法用来将一个变量名展开成两个变量名
    :param name: 变量名
    :return: 一前一后的俩个变量名
    rto2_net_1sts1mwww2wwww_net_1sts1mwww2wwww
    """
    import re
    group = re.search('^ba2_.*(ba1_.*)_(ba1_.*)$', name)
    if group:
        name1 = group.group(1)
        name2 = group.group(2)
    return name1, name2


# # test
# import sys
# import os
# os.getcwd()
# from variables.get_variable_name import get_variable_name
# from variables.variable_logic import get_logic
# order = get_logic("order")
# classes = get_logic("class")
# var_name = ['ba1_00wwwwwecwTTS']
# for name in var_name:
#     print(name_to_dict(name, order, classes))
