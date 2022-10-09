# coding=utf-8
import re
from cfg import *
from gensim.models import word2vec, Word2Vec
import jieba
import pandas as pd


def get_stopword_list(file:str):
    with open(file, 'r', encoding='utf-8') as f:    #
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list

# 提取单字符
def get_single_word(ques:str):
    return re.findall(r'[^\x00-\xff]', ques)

# 去除停用词
def clean_stopword(str):
    stopword_list = get_stopword_list('stopwords/baidu_stopwords.txt') + get_stopword_list('stopwords/cn_stopwords.txt')
    result = ''
    word_list = jieba.lcut(str)
    for w in word_list:
        if w not in stopword_list:
            result+=w
    return result


def get_ques_str(data:pd.DataFrame):
    sentences_list=[]
    for idx in range(len(data)):
        sentences_list.append((data.iloc[idx].values.tolist())[0])
        sentences_list.append((data.iloc[idx].values.tolist())[1])
    return ''.join(sentences_list)

def word2text_vec(path:str):
    with open(path, 'w', encoding='utf-8') as f:
        for ele in single_word:
            f.write(ele+'\n')
    return list(word2vec.Text8Corpus(path))

def train_model():
    model = Word2Vec(vector_size=vec_size, min_count=1, window=3)
    model.build_vocab(sentences)
    model.train(sentences, total_examples=model.corpus_count, epochs=epoch)
    model.wv.save_word2vec_format(bin_path)


if __name__ == '__main__':


    data,path = pd.read_csv(QA_path),txt_path

    # 加载停用词表,并划分单个字符
    ques=get_ques_str(data)
    ques_res = clean_stopword(ques)
    single_word = get_single_word(ques_res)
    sentences = word2text_vec(path)

    # 加载空模型，加载词表训练
    train_model()
