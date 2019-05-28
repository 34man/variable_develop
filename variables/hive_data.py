from pyhive import hive
import pandas as pd


def load_data(sql):
    host = "10.50.40.4"
    PORT = 10000
    name = "liqingfeng"
    password = "J9qh59z39e"
    database = "rds"
    conn = hive.Connection(host=host, port=PORT, username=name, database=database, auth='LDAP', password=password)

    df = pd.read_sql(sql, conn)
    conn.close()
    return df


def delete_a(df):
    for var in df.columns:
        if str(var).startswith('a.'):
            df.rename({var: str(var).replace("a.", "")}, inplace=True, axis="columns")
    return df


def gambel_rename(df):
    df = df.rename({"total_shot_num": "总网站命中数",
                    "dubo_shot_num": "赌博网站命中数",
                    "cp_shot_num": "彩票网站命中数",
                    "qp_shot_num": "棋牌网站命中数",
                    "db_shot_num": "担保网站命中数"}, axis="columns")
    return df


def wechat_rename(df):
    df = df.rename({
        "is_reg": "是否注册了了微信",
        "acc_state": "账号是否异常"
    }, axis='columns')
    return df


def tel_rename(df):
    df = df.rename({
        "mark_num": "标记数量",
        "province": "省"
    }, axis="columns")
    return df
