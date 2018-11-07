# -*- coding: utf-8 -*- 
# @Time : 2018/11/5 16:03 
# @Author : Allen 
# @Site :  余弦相似
from model.model_service import get_data_dict
from cut.cut_sentence import Cut
from utils import save_pickle, load_pickle
import os
import numpy as np
import math


class Cos:
    def __init__(self):
        self.cut = Cut()
        self.data_dict = get_data_dict()
        self.entity_word_dict = self.get_entity_word_dict()
        self.all_word_dict = self.get_all_word_dict()
        self.entity_sentence_vector = self.get_entity_sentence_vector()
        self.all_sentence_vector = self.get_all_sentence_vector()

    def get_all_word_dict(self):
        data_path = r'./similarity/all_word_dict.pkl'
        if os.path.exists(data_path):
            word_vector = load_pickle(data_path)
        else:
            all_dict = self.get_all_dict(self.data_dict)
            word_vector = self.get_dict_key_num(all_dict)
            save_pickle(data_path, word_vector)
        return word_vector

    def get_all_dict(self, data_dict):
        temp = {}
        for d in data_dict.values():
            temp = dict(temp, **d)
        return temp

    def get_entity_word_dict(self):
        data_path = r'./similarity/entity_word_dict.pkl'
        if os.path.exists(data_path):
            word_vector = load_pickle(data_path)
        else:
            word_vector = self.get_dict_key_num(self.data_dict)
            save_pickle(data_path, word_vector)
        return word_vector

    def get_dict_key_num(self, data_dict):
        '''
        获取字典key分词的词典
        :param data_dict:字典
        :return:{词1:1，词2:2}
        '''
        word_vector = {}
        count = 0
        for k in data_dict.keys():
            for d in self.cut.cut_sentence(k).split():
                if d not in word_vector:
                    word_vector[d] = count
                    count += 1
        return word_vector

    def get_entity_sentence_vector(self):
        data_path = r'./similarity/entity_sentence_vector.pkl'
        if os.path.exists(data_path):
            all_sentence_vector = load_pickle(data_path)
        else:
            all_sentence_vector = self.get_dict_vector(self.data_dict)
            save_pickle(data_path, all_sentence_vector)
        return all_sentence_vector

    def get_dict_vector(self, data_dict):
        '''
        得到字典中key的向量
        :param data_dict:字典
        :return:{key:向量}
        '''
        all_sentence_vector = {}
        for k in data_dict.keys():
            temp_vec = self.get_sentence_vector(k, self.entity_word_dict)
            all_sentence_vector[k] = temp_vec
        return all_sentence_vector

    def get_all_sentence_vector(self):
        data_path = r'./similarity/all_sentence_vector.pkl'
        if os.path.exists(data_path):
            all_sentence_vector = load_pickle(data_path)
        else:
            all_sentence_vector = self.get_data_dict_vector(self.data_dict)
            save_pickle(data_path, all_sentence_vector)
        return all_sentence_vector

    def get_data_dict_vector(self, data_dict):
        all_sentence_vector = {}
        for k, v in data_dict.items():
            sentence_vector = {}
            for k1, v1 in v.items():
                sentence_vector[k1] = self.get_sentence_vector(k1, self.all_word_dict)
            all_sentence_vector[k] = sentence_vector
        return all_sentence_vector

    def get_sentence_vector(self, sentence, word_dict):
        temp_vec = np.zeros([1, len(word_dict)])
        for d in self.cut.cut_sentence(sentence).split():
            if d in word_dict.keys():
                temp_vec[:, word_dict[d]] += 1
        return temp_vec

    def similarity(self, sentence):
        answer = ''
        max_vec = 0
        # print(self.cut.cut_sentence(sentence))
        sentence_vec = self.get_sentence_vector(sentence, self.entity_word_dict)
        entity_name = self.concat_dict_vector(self.entity_sentence_vector, sentence_vec)
        if entity_name:
            print(entity_name)
            sentence_vec = self.get_sentence_vector(sentence, self.all_word_dict)
            answer = self.concat_dict_vector(self.all_sentence_vector[entity_name], sentence_vec)
            print(answer)
            return self.data_dict[entity_name][answer]
        else:
            return False

    def concat_dict_vector(self, dict_vector, sentence_vec):
        '''
        句子向量个字典的向量cos
        :return:最相似的字典key
        '''
        max_vec = 0
        answer = ''
        for k, v in dict_vector.items():
            vec = self.compute_cos(sentence_vec, v)
            if vec > max_vec:
                max_vec = vec
                answer = k
        return answer

    def compute_cos(self, A, B):
        num = float(A.dot(B.T))
        denom = np.linalg.norm(A) * np.linalg.norm(B)
        cos = num / denom
        sim = 0.5 + 0.5 * cos
        return sim

    def cos(self, vector1, vector2):
        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
            return 0.5 + 0.5 * dot_product / ((normA * normB) ** 0.5)

    def VectorCosine(self, x, y):
        ''' 计算向量夹角余弦 '''
        vc = []
        for i in range(1, len(x) - 2):
            xc1 = x[i] - x[i - 1]
            xc2 = x[i + 1] - x[i]
            yc1 = y[i] - y[i - 1]
            yc2 = y[i + 1] - y[i]
            vc.append((xc1 * xc2 + yc1 * yc2) / (math.sqrt(xc1 ** 2 + yc1 ** 2) * math.sqrt(xc2 ** 2 + yc2 ** 2)))

        return vc


def main():
    cos = Cos()
    while True:
        x = input()
        cos.similarity(x)


if __name__ == '__main__':
    main()
