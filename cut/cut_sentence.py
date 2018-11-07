# -*- coding: utf-8 -*- 
# @Time : 2018/11/5 16:05 
# @Author : Allen 
# @Site :  结巴分词
import jieba
from utils import load_txt
import jieba.posseg as pseg


class Cut:
    def __init__(self):
        ([jieba.add_word(d) for d in load_txt('./cut/my_word.txt')])
        self.stop_dict = set([d for d in load_txt('./cut/my_stop_word.txt')])

    def cut_sentence(self, sentence):
        return ' '.join([w for w, f in pseg.cut(sentence) if not w in self.stop_dict and not f == 'x'])
