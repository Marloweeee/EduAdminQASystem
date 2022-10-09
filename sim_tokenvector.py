
# coding: utf-8


import gensim
import pandas as pd
import numpy as np
from cfg import *




class SimTokenVec:

    def __init__(self):
        # self.embedding_path = 'model/token_vector.bin'
        self.embedding_path = 'model/word2vec.bin'
        self.vec_size=vec_size
        self.model = gensim.models.KeyedVectors.load_word2vec_format(self.embedding_path, binary=False,limit=500)

    '''获取词向量文件'''
    def get_wordvector(self, word,vec_size:int):  # 获取词向量
        try:
            return self.model[word]
        except:
            return np.zeros(vec_size)

    def get_vector(self,word_list:str,vec_size:int):
        vector=np.zeros(vec_size)
        for word in word_list:
            vector+=self.get_wordvector(word,vec_size)
        return vector/len(word_list)


    '''基于余弦相似度计算句子之间的相似度，句子向量等于字符向量求平均'''
    def similarity_cosine(self, word_list1, word_list2):  # 给予余弦相似度的相似度计算
        vec_size=self.vec_size
        vector1,vector2=self.get_vector(word_list1,vec_size),self.get_vector(word_list2,vec_size)
        cos1 = np.sum(vector1 * vector2)
        cos21,cos22 = np.sqrt(sum(vector1 ** 2)),np.sqrt(sum(vector2 ** 2))
        similarity = cos1 / float(cos21 * cos22)
        return similarity

    '''计算句子相似度'''
    def distance(self, text1, text2):  # 相似性计算主函数
        word_list1 = [word for word in text1]
        word_list2 = [word for word in text2]
        return self.similarity_cosine(word_list1, word_list2)

def query(text: str):
    import time
    start_time=time.time()
    questions_list,answers_list = [],[]
    data = pd.read_csv(QA_path)
    for idx in range(len(data)):
        Q, A = (data.iloc[idx].values.tolist())[:]
        questions_list.append(Q)
        answers_list.append(A)

    sim = []
    for i in range(len(questions_list)):
        pre_matched_text = (" ".join(questions_list[i]))
        simer = SimTokenVec()
        sim.append(simer.distance(text, pre_matched_text))

    max_of_sim = max(sim)
    print(max_of_sim)
    index_of_max_of_sim = sim.index(max_of_sim)
    end_time=time.time()
    print("运行时间：{}".format(end_time-start_time))
    print("Q:", questions_list[index_of_max_of_sim])
    print("A", answers_list[index_of_max_of_sim])

while 1:
    text1 = input('enter sent1:').strip()
    query(text1)
