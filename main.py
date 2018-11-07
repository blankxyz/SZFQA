# -*- coding: utf-8 -*- 
# @Time : 2018/11/5 15:20 
# @Author : Allen 
# @Site :
from similarity.cos_similarity import Cos


def main():
    cos = Cos()
    while True:
        print('请输入：')
        x = input()
        answer = cos.similarity(x)
        if answer:
            print(answer)
        else:
            print('没有这个知识')


if __name__ == '__main__':
    main()
