# -*- coding: utf-8 -*- 
# @Time : 2018/11/5 10:20 
# @Author : Allen 
# @Site :  计算相似simhash
import jieba
from hashes.simhash import simhash
import re


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def get_cut_sentence(s):
    return ' '.join(jieba.cut(s))


def get_simhash(sentence1, sentence2):
    hash1 = simhash(get_cut_sentence(sentence1))
    hash2 = simhash(get_cut_sentence(sentence2))
    # print(hash1)
    # print(hash2)
    similarity = hash1.similarity(hash2)
    print(similarity)
    if similarity > 0.8:
        return similarity
    else:
        return False


#
sentence1 = '建设项目环境影响评价报告表书审批核与辐射类年审'
sentence2 = '你好'

print(get_simhash(sentence1, sentence2))
