# -*- coding: utf-8 -*- 
# @Time : 2018/11/5 9:34 
# @Author : Allen 
# @Site :  数据
import pandas as pd
import os
import numpy as np
from utils import load_pickle, save_pickle


def get_data_dict():
    data_path = r'./model/data_dict.pkl'
    if os.path.exists(data_path):
        entity_dict = load_pickle(data_path)
    else:
        root = r'C:\Users\User\Desktop\政务大厅模板知识'
        entity_dict = {}
        for name in os.listdir(root):
            print(name)
            df = read_excel(os.path.join(root, name))
            qa_dict_temp, entity_name = format_df(df)
            entity_dict[entity_name] = qa_dict_temp
            # qa_dict = dict(qa_dict, **qa_dict_temp)
        save_pickle(data_path, entity_dict)
    return entity_dict


def read_excel(path):
    return pd.read_excel(path)


def format_df(df):
    qa_dict = {}
    entity_name = ''
    for i, row in df.iterrows():
        if not row['实例名称'] is np.nan:
            entity_name = ''.join(row['实例名称'].split())
        if not row['标准问题'] is np.nan:
            answer = ''.join(row['标准答案'].split())
            qa_dict[''.join(row['标准问题'].split())] = answer
        if not row['测试样例'] is np.nan:
            qa_dict[''.join(row['测试样例'].split())] = answer
    return (qa_dict, entity_name)


if __name__ == '__main__':
    print(len(get_data_dict()))
