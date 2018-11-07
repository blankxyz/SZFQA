# -*- coding: utf-8 -*-
# @Time : 2018/7/31 10:09
# @Author : Allen
# @Site :  主要是读取文件（csv，txt），及pickle等

import os
import pickle
import re
import time
import uuid
import shutil
import jieba
import pandas as pd
from datetime import datetime

'''
    获取当前项目路径
'''


def get_dir():
    return os.path.dirname(os.getcwd()) + os.sep


'''
    读取excel
'''


def load_excel(path, sheetname=False):
    with open(path, 'rb') as f:
        data = pd.read_excel(f, sheetname=sheetname)
    return data


'''
    读取csv
'''


def load_csv(path):
    with open(path, 'r', encoding='gb18030') as f:
        data = pd.read_csv(f)
    return data


'''
    判断目录
'''


def is_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    else:
        return True


'''
    保存为pickle
'''


def save_pickle(path, maps):
    with open(path, 'wb') as f:
        pickle.dump(maps, f)
    print("Success Save:%s" % (path))


'''
    load pickle

'''


def load_pickle(path):
    with open(path, 'rb') as f:
        maps = pickle.load(f)
    return maps


'''
    保存数据
    file_name:文件名
    names:数据
    flag:标注名
    dir:目录名

'''


def save_format_data_csv(file_name, names, flag, file_dir):
    dir_file = get_dir() + os.sep + file_dir + os.sep
    if is_dir(dir_file):
        file_name = dir_file + file_name
        with open(file_name, 'a', encoding='utf8') as f:
            for name in names:
                f.write(name + "," + flag + "\n")
        print("保存到: %s " % (file_name))


'''
    保存数据csv
    file_name:文件名
    data:数据
    file_dir:目录名

'''


def save_csv(file_name, df, file_dir):
    dir_file = get_dir() + os.sep + file_dir + os.sep
    if is_dir(dir_file):
        file_name = dir_file + file_name
        with open(file_name, 'w') as f:
            df.to_csv(f, index=0)
        print("保存到: %s " % (file_name))


'''
    多功能替换
    text:文本
    dict:需要替换的内容
'''


def multiple_replace(text, dict):
    regex = re.compile('|'.join(map(re.escape, dict)))

    def one_xlat(match):
        return dict[match.group(0)]

    return regex.sub(one_xlat, text)


'''
    保存为txt
'''


def save_txt(data, path):
    with open(path, 'w', encoding='utf8') as f:
        for d in data:
            f.write(d + '\n')
    print("Save Success !")


'''
    判读文件是否存在
'''


def is_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False


'''
    判断是否为乱码
'''


def is_messy(sentence):
    def new_len(iterable):
        try:
            return iterable.__len__()
        except AttributeError:
            return sum(1 for _ in iterable)

    luanma_len = len(sentence)
    luanma = jieba.cut(sentence)
    res = float(luanma_len / new_len(luanma))
    if res < 1.2:
        return True
    else:
        return False


'''
    是否为float
'''


def is_float(sentence):
    try:
        return type(eval(sentence)) == float
    except:
        return False


'''
    读取txt
'''


def load_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = ([d.strip() for d in f.readlines()])
    return data


'''
    str to datetime
'''


def str_to_datetime(str):
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S')


'''
    获取当前时间 datetime类型
'''


def get_datetime():
    return datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


'''
    移动文件
'''


def move_file(source_path, total_path):
    if is_dir(total_path):
        try:
            shutil.move(source_path, total_path)
        except Exception as e:
            try:
                os.remove(source_path)
                print(e)
                print("移除已存在文件")
            except:
                pass


'''
    把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
'''


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return str_to_datetime(time.strftime('%Y-%m-%d %H:%M:%S', timeStruct))


'''
    获取文件的创建时间
'''


def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


'''获取文件的修改时间'''


def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


if __name__ == '__main__':
    path = r'E:\san_wu\兴义地区各县局群资料.xlsx'
    print(os.path.getsize(path) / 1024)
