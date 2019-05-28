import sys
import pandas as pd
import numpy as np

sys.path.append('./')
from variables.get_variable_name import get_variable_name
from variables.variable_logic import get_logic
import datetime
from variables.get_holiday_weekday import get_holiday
from variables.dismantle_var_name import dismantle_var3_name, ifinclude, name_to_dict, dismantle_var2_name
from variables.get_top_value import get_top_value
import os

os.getcwd()


def get_variable_condition(df, batch):
    """
    传进来变量名和变量对应的变量名的命名逻辑，返回一个以变量名为列名，0和真实值为值的和原始数据行数相同的dataframe
    第一批的变量根据原始字段演变而来，第二批根据第一批的字段演变而来，判断两个变量必为前面的除后面的变量，无需逻辑。
    :param df:原始的数据框,构造第一批的数据，df必须是原始的数据，第二批必须是第一批变量的数据框，第三批是原始的变量
    :param batch:表示要构造的第几批的变量
    :return:返回一个以变量名为列，只有符合变量的要求的行有值的数据框
    """
    var_name = get_variable_name(batch)
    order = get_logic('order')
    classes = get_logic("class")

    # 判断进行第几批变量构造
    if batch == 1:
        # 计算时间间隔以及我们后面要用的用来构造第一批变量的基础字段。
        print("开始第一批变量condition构造")
        df['time_diff'] = (pd.to_datetime(df['time_crawl']) - pd.to_datetime(df['start_time'])).map(lambda x: x.days)

        # 计算时间间隔
        dur_time = []
        for diff in np.array(df['time_diff']):
            if diff != diff:
                dur_time += [-1]
            else:
                if (diff <= 7) and (diff > 3):
                    dur_time += ['7d']
                elif diff == 0:
                    dur_time += ['00']
                elif diff in [2, 3]:
                    dur_time += ['3d']
                elif (diff <= 30) and (diff > 7):
                    dur_time += ['1m']
                elif (diff <= 60) and (diff > 30):
                    dur_time += ['2m']
                elif (diff <= 90) and (diff > 60):
                    dur_time += ['3m']
                elif (diff <= 120) and (diff > 90):
                    dur_time += ['4m']
                elif (diff <= 180) and (diff > 120):
                    dur_time += ['6m']
                else:
                    dur_time += ['ww']
        print("dur_time{}".format(len(dur_time)))

        # 计算时间状态 把时间格式转化到 “%Y-%m-%d'
        status = []
        for sta in np.array(df['start_time']):
            if sta != sta:
                status += [-1]
            else:
                try:
                    sta = datetime.datetime.strftime(datetime.datetime.strptime(str(sta), "%Y-%m-%d %H:%M:%S"),
                                                     "%Y-%m-%d")
                    sta = get_holiday(sta)
                except:
                    try:
                        sta = datetime.datetime.strftime(datetime.datetime.strptime(str(sta), "%Y%m%d %H:%M:%S"),
                                                         "%Y-%m-%d")
                        sta = get_holiday(sta)
                    except:
                        sta = -1

                if sta in [5, 6]:
                    status += ["e"]
                elif sta == -1:
                    status += [-1]
                else:
                    status += ["d"]

        print("status{}".format(len(status)))

        # # 总条数
        # total_size = []
        # for size in np.array(df['total_size']):
        #     if size != size:
        #         total_size += [-1]
        #     else:
        #         if size <= 500:
        #             total_size += ['500t']
        #         elif (size > 500) and (size <= 1000):
        #             total_size += ["1000t"]
        #         elif (size > 1000) and (size <= 1500):
        #             total_size += ["1500t"]
        #         elif (size > 1500) and (size <= 2000):
        #             total_size += ["2000t"]
        #         elif (size > 2000) and (size <= 3000):
        #             total_size += ["3000t"]
        #         else:
        #             total_size += ["3000ts"]

        # 通信费
        fee_tick = []
        for temp in np.array(df['fee']):
            if temp != temp:
                fee_tick += ['-1']
            else:
                if temp <= 0.01:
                    fee_tick += ['01Y']
                elif (temp > 0.01) and (temp <= 0.1):
                    fee_tick += ["10Y"]
                elif (temp > 0.1) and (temp <= 0.33):
                    fee_tick += ["33Y"]
                elif (temp > 0.33) and (temp <= 1.6):
                    fee_tick += ["160Y"]
                else:
                    fee_tick += ["160YS"]
        print("fee{}".format(len(fee_tick)))

        # 上网方式 这里需要判断net_way 和 business_name 两个字段才能做出判断
        # 准备需要的list
        g4 = ["G", "g", "cmnet", "CMNET", "普通上网"]
        movie = ['腾讯视频', '爱奇艺', '哔哩哔哩', '西瓜', '乐视', '酷狗', '芒果']
        news = ['头条', '新浪']
        shopping = ['天猫', '阿里', '京东']
        kit = ['彩信', '百度', '邮箱']
        economic = ['银行']
        game = ['网易', '腾讯']
        net_way_tick = []
        for x, y in zip(np.array(df['net_way']), np.array(df['business_name'])):
            if x != x:
                net_way_tick = net_way_tick + ['-1']
            elif ifinclude(g4, x) == 1:
                net_way_tick = net_way_tick + ['4G']
            elif x.find("无线") != -1:
                net_way_tick = net_way_tick + ['wifi']
            elif (ifinclude(movie, x) == 1) or (ifinclude(movie, y) == 1):
                net_way_tick = net_way_tick + ['mo']
            elif (ifinclude(news, x) == 1) or (ifinclude(news, y) == 1):
                net_way_tick = net_way_tick + ['new']
            elif (ifinclude(shopping, x) == 1) or (ifinclude(shopping, y) == 1):
                net_way_tick = net_way_tick + ['sh']
            elif (ifinclude(kit, x) == 1) or (ifinclude(kit, y) == 1):
                net_way_tick = net_way_tick + ['ki']
            elif (ifinclude(economic, x) == 1) or (ifinclude(economic, y) == 1):
                net_way_tick = net_way_tick + ['ec']
            elif (ifinclude(game, x) == 1) or (ifinclude(game, y) == 1):
                net_way_tick = net_way_tick + ['ga']
            else:
                net_way_tick = net_way_tick + ['w']
        print("net_way{}".format(len(net_way_tick)))

        # 开始时间
        # 开始时间需要小时就够了
        start_time_tick = []
        for time in np.array(df['start_time']):
            if time != time:
                start_time_tick = start_time_tick + ['-1']
            else:
                try:
                    hour = datetime.datetime.strptime(time, "%Y%m%d %H:%M:%S").hour + 0
                except:
                    try:
                        hour = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S").hour + 0
                    except:
                        hour = -1
                if (hour >= 1) and (hour < 6):
                    start_time_tick = start_time_tick + ['5']
                elif (6 <= hour) and (hour < 12):
                    start_time_tick = start_time_tick + ['1']
                elif (12 <= hour) and (hour < 18):
                    start_time_tick = start_time_tick + ['2']
                elif (18 <= hour) and (hour < 22):
                    start_time_tick = start_time_tick + ['3']
                elif hour in [22, 23, 0, 1]:
                    start_time_tick = start_time_tick + ['4']
        print("start_time_tick{}".format(len(start_time_tick)))
        # 总时长
        # 计算对象需要保留后面计算的数字，因此在单元格中保存 分类+“_”+ 实际值
        total_time_tick = []
        for total_hour in np.array(df['total_time']):
            if total_hour != total_hour:
                total_time_tick = total_time_tick + [-1]
            else:
                t_hour = total_hour / 3600
                if t_hour <= 0.01:
                    total_time_tick = total_time_tick + ['1h']
                elif (t_hour > 0.01) and (t_hour <= 0.08):
                    total_time_tick = total_time_tick + ['2h']
                elif (t_hour > 0.08) and (t_hour <= 0.42):
                    total_time_tick = total_time_tick + ['3h']
                elif (t_hour > 0.43) and (t_hour <= 0.74):
                    total_time_tick = total_time_tick + ['4h']
                elif t_hour > 0.74:
                    total_time_tick = total_time_tick + ['5h']
                else:
                    total_time_tick = total_time_tick + [-1]
        print("total_time{}".format(len(total_time_tick)))
        # 总流量
        total_traffic_tick = []
        for traffic in np.array(df['total_traffic']):
            if traffic != traffic:
                total_traffic_tick = total_traffic_tick + [-1]
            else:
                mb = round(traffic / 1024)
                if mb <= 0.02:
                    total_traffic_tick = total_traffic_tick + ['2mb']
                elif (mb > 0.02) and (mb <= 0.27):
                    total_traffic_tick = total_traffic_tick + ['27mb']
                elif (mb > 0.27) and (mb <= 1.66):
                    total_traffic_tick = total_traffic_tick + ['166mb']
                elif mb > 1.66:
                    total_traffic_tick = total_traffic_tick + ['166mbs']
        print("total_traffic{}".format(len(total_traffic_tick)))
        # 业务名称
        business_name_tick = []
        for name in df['business_name']:
            if name != name:
                business_name_tick = business_name_tick + [-1]
            else:
                if name.find('套餐') != -1:
                    business_name_tick = business_name_tick + [1]
                elif name.find('包') != -1:
                    business_name_tick = business_name_tick + [2]
                elif name.find('定向') != -1:
                    business_name_tick = business_name_tick + [3]
                elif (name.find('国内') != -1) or (name.find('全国') != -1):
                    business_name_tick = business_name_tick + [4]
                else:
                    business_name_tick = business_name_tick + [5]
        print("business_name{}".format(len(business_name_tick)))
        # 把上面整理好的 list 转换成数据框
        condition = {'dur_time': dur_time,
                     "status": status,
                     "fee_tick": fee_tick,
                     "net_way_tick": net_way_tick,
                     "start_time_tick": start_time_tick,
                     "total_time_tick": total_time_tick,
                     "total_traffic_tick": total_traffic_tick,
                     "business_name_tick": business_name_tick}
        condition = pd.DataFrame(condition)
        var_name_dismantle = {}

        # 解析变量名
        for name in var_name:
            var_name_dismantle.update(name_to_dict(name, order, classes))
        return condition, var_name_dismantle, var_name
    # 第二批变量的构造方法
    elif batch == 2:
        df_2 = {}
        names = get_variable_name(2)
        name_dict = map(dismantle_var2_name, names)
        for i, name in enumerate(name_dict):
            var = (np.array(df[name[0]]) / np.array(df[name[1]]))
            df_2.update({names[i]: var})
        df_2 = pd.DataFrame(df_2, index=df.index)
        return df_2

    # 第三批变量的构造方法
    # 传入第一批构造时的数据框 也就是第一批的condition

    elif batch == 3:
        conn = {
            "N": "net_way",
            "TT": "total_traffic"
        }
        # 拿到condition 数据框
        condition = df
        names = get_variable_name(3)
        names_dict = map(dismantle_var3_name, names)
        # names_dict 表示 {name:[top, dur_time, status, net_way, cal_obj, really_obj]}
        var3_names = {}
        df_3 = pd.DataFrame(columns=names, index=np.unique(condition["id_file"]))

        for name in names_dict:
            var3_names.update(name)

        for name, dis_name in var3_names.items():
            # 筛选数据集
            top, dur_time, status, net_way_tick, cal_object, really_obj = dis_name[:]
            print([top, dur_time, status, net_way_tick, cal_object, really_obj])
            df_temp = condition
            # 这里的status == w 表示 status 不参与筛选
            if status == 0:
                df_temp = df_temp[(df_temp['dur_time'] == dur_time) &
                                  (df_temp['net_way_tick'] == net_way_tick)]
            else:
                df_temp = df_temp[(df_temp['dur_time'] == dur_time) &
                                  (df_temp["status"] == status) &
                                  (df_temp['net_way_tick'] == net_way_tick)]
            df_temp = get_top_value(df_temp, conn.get(cal_object), conn.get(really_obj))
            df_temp = df_temp.set_index("id_file")
            df_3[name] = df_temp[conn.get(really_obj)]
        return df_3
    else:
        raise Exception("batch 必须是123批，请检查是不是参数传错了！")


def variable(df, batch):
    """
    现在通过以前的方法计算出的包含 原始字段的真实值的 dataframe 和 要构造的字段的变量名字构造的字典结合,构造变量
    :param df: 已经有的 符合基础变量的原始值
    :param batch: 批次
    :return: 要构造的变量的最总结果
    var_name_dismantle = {
    "net_1cts6mdwwwwwww" : ["net_1", "ct", "s", "6m", "d", "w"*7]
    "net_1cts6mdwwwwwww": [变量前缀 + 时间间隔+ 起始时间+ 时间状态 + 通信费 + 总时长 + 总流量 +
    上网方式 +  业务名称 + 计算对象 + 计算方法]
    }
    """
    if batch == 1:
        conn = {
            1: "dur_time",
            2: "start_time_tick",
            3: "status",
            4: "fee_tick",
            5: "total_time_tick",
            6: "total_traffic_tick",
            7: "net_way_tick",
            8: "business_name_tick"
        }
        cal_way = {
            'S': np.sum,
            "A": np.mean,
            "C": np.size,
            "M": np.max,
            "V": lambda x: np.var(x),
            "D": lambda x: len(x.unique())
        }
        cal_object = {
            "TS": "ant",
            "TT": "total_traffic",
            "D": "total_time",
            "F": "fee",
            "N": "net_way"
        }

        df_condition, var_name_dismantle, var_name = get_variable_condition(df, batch)

        index = np.unique(df["id_file"])
        columns = var_name
        df_condition.to_csv("condition.csv", index=False)
        df_merge = df.merge(df_condition, right_index=True, left_index=True)
        df_merge.to_csv("dfs.csv")
        dict_picture = {}
        df_final = pd.DataFrame(columns=columns, index=index)
        # 获取变量列表
        print(len(var_name))
        for name in var_name:
            dfs = df_merge
            print("dfs{}".format(dfs.shape[0]))
            var_name_dismantle_list = var_name_dismantle.get(name)
            # temp_var 代表我们要筛选的变量集合
            # class_li 变量的筛选条件的list
            temp_var = []
            classes_li = []
            for li in var_name_dismantle_list:
                if li != 0:
                    if conn.get(var_name_dismantle_list.index(li)):
                        temp_var += [conn.get(var_name_dismantle_list.index(li))]
                        classes_li += [li]
            print("{}变量分解值：{}".format(name, var_name_dismantle_list))
            print("变量{}  值 {}".format(temp_var, classes_li))
            # 在这按照我们已经拿到的变量名和筛选的条件筛选出想要的Dataframe并进行计算，能够拿到这个name下的所有以Id 分类的值
            # 1 把condition和 df merge在一起根据 id_file
            # 2 计算出符合条件的df数据块
            # 2.0 先在已经存储的数据中寻找有没有符合条件的df_temp
            # 2.1 这里将一些筛选记录下来，不用每次计算
            if tuple(temp_var + classes_li) in dict_picture:
                df_temp = dict_picture.get(tuple(temp_var + classes_li))
            else:
                for var, val in zip(temp_var, classes_li):
                    print("筛选{} 的值:{} ".format(var, val))
                    dfs = dfs[dfs[var] == val]
                    print("dfs 的大小{}".format(dfs.shape[0]))
                df_temp = dfs
                dict_picture.update({tuple(temp_var + classes_li): df_temp})
            # 3、拿到数据块df_temp为符合筛选条件的，接下来拿到计算对象和计算方法，
            cal_way_ele = cal_way.get(var_name_dismantle_list[10])
            cal_object_ele = cal_object.get(var_name_dismantle_list[9])

            # 4、对数据进行计算按照id_file 分组 并进行计算得到结果， 注意如果 cal_object 是 TS 则直接计算，不用费太大力气

            df_temp['ant'] = 1
            print("筛选数据的数据量 {}".format(df_temp.shape))
            print("正在对 {} 进行 {} 处理！！！".format(cal_object_ele, cal_way_ele))

            if df_temp.shape[0] != 0:
                if df_temp[cal_object_ele].isnull().all():
                    df_final[name] = np.nan
                else:
                    df_final_stage1 = df_temp.pivot_table(index=["id_file"], values=[cal_object_ele],
                                                          aggfunc=cal_way_ele)[cal_object_ele]
                    print(name)
                    df_final[name] = df_final_stage1
            else:
                df_final[name] = -1

            # 5、把分组完的对象存进字典中

        print("构造完成")
        return df_final
    elif batch == 2:
        df2_final = get_variable_condition(df, 2)
        return df2_final
    elif batch == 3:
        df3_final = get_variable_condition(df, 3)
        return df3_final
    else:
        get_variable_condition(df, 4)


dict_test = {str(['dur_time', '00']): 123}
if dict_test.get(str(['dur_time', '00'])):
    print('111')
dict_test2 = {"A": 1, "B": 3}
df_test = pd.DataFrame([dict_test2])
va = (df_test["A"] / df_test["B"]).values
