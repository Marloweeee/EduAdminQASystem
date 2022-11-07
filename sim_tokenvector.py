
# coding: utf-8


import gensim
import pandas as pd
import numpy as np
from cfg import *




class SimTokenVec:

    def __init__(self):
        # self.embedding_path = 'model/token_vector.bin'
        self.embedding_path = bin_path
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

    def read_data(self,path):
        questions_list, answers_list = [], []
        data = pd.read_csv(path)
        for idx in range(len(data)):
            Q, A = (data.iloc[idx].values.tolist())[:]
            questions_list.append(Q)
            answers_list.append(A)
        return questions_list,answers_list

    def similarity_cosine(self, vector, text):  # 基于余弦相似度的相似度计算

        vector1 = np.array(vector)
        word_list = [word for word in text]
        vector2 = self.get_vector(word_list, self.vec_size)
        cos1 = np.sum(vector1 * vector2)
        cos21, cos22 = np.sqrt(sum(vector1 ** 2)), np.sqrt(sum(vector2 ** 2))
        similarity = cos1 / float(cos21 * cos22)
        return similarity


    def get_max_idx(self,text,q_list,v_list):

        sim = []
        simer = SimTokenVec()
        for i in range(len(q_list)):
            sim.append(simer.similarity_cosine(vector=v_list[i], text=text))
        max_of_sim_score = max(sim)
        idx = sim.index(max_of_sim_score)

        return idx,max_of_sim_score

    def query(self,text: str, vec_list: list, questions_list: list, answers_list: list):

        idx, sim_score = self.get_max_idx(text, questions_list,vec_list)
        return answers_list[idx], sim_score





if __name__ == '__main__':

    q_list, a_list, v_list = [], [], []
    df = pd.read_csv('data/QA.csv')

    for idx in range(len(df)):
        Q, A = (df.iloc[idx].values.tolist())[:]
        q_list.append(Q)
        a_list.append(A)

    for i in q_list:
        v_list.append(SimTokenVec().get_vector(word_list=i, vec_size=vec_size))

    while 1:
        text1 = input('enter sent1:').strip()
        print(SimTokenVec().query(text1,v_list,q_list,a_list))
