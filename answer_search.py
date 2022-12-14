# coding=utf-8
from cfg import *
import pandas as pd
from py2neo import Graph
from question_parse import *
from sim_tokenvector import SimTokenVec

class AnswerSearcher:

    def __init__(self):
        self.graph=Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="112099")

    def search_main(self,cql):


        res=self.graph.run(cql).data()
        print(res)

        return res[0]

    def answer_prettify(self,entity_key,answers):
        if not answers:
            return ''

        attribute=list(answers.keys())
        context=list(answers.values())
        context_len=len(attribute)
        ans=''

        for idx in range(context_len):
            if entity_key in ['课程','上课']:
                ans+="\033[1;31m 系统回复 \033[0m有关{}的信息如下：\n{}".format(attribute[idx].split('.')[1],context[idx])
            elif entity_key in ['国家奖学金','学业奖学金'] :
                if attribute[idx]=='取消资格':
                    ans += "\033[1;31m 系统回复 \033[0m如有下列情况之一，{}的资格将被取消：\n{}".format(attribute[idx].split('.')[1],context[idx])
                else:
                    ans +="\033[1;31m 系统回复 \033[0m：\n{}".format(context[idx])
            else:
                ans+=("\033[1;31m 系统回复 \033[0m：\n{}".format(context[idx]))
        return ans




if __name__ == '__main__':


    q_list, a_list, v_list = [], [], []
    df = pd.read_csv('data/QA.csv')

    for idx in range(len(df)):
        Q, A = (df.iloc[idx].values.tolist())[:]
        q_list.append(Q)
        a_list.append(A)

    for i in q_list:
        v_list.append(SimTokenVec().get_vector(word_list=i, vec_size=vec_size))
    print("\033[1;31m 欢迎使用智慧教务系统！\033[0m")


    while 1:
        ques,res = input("用户："),"您的问题我们还要再向相关部门请教呢，请您过两天再来试试吧"
        try:
            ans, sim_score = SimTokenVec().query(ques,v_list,q_list,a_list)
            print(sim_score)
            if sim_score >= 0.7:
                res = '\033[1;31m 系统回复 \033[0m' + ans
            else:
                if QuestionClassifier().classify(ques) != {}:
                    e, q, k = QuestionClassifier().classify(ques)
                    cql = QuestionPaser().parser_main(e, q, k)
                    ans = (AnswerSearcher().search_main(cql))
                    res = AnswerSearcher().answer_prettify(k, ans)

            print(res)
        except:
            print(res)
    # ques=input('请输入问题：')
    # e, q, k = QuestionClassifier().classify(ques)
    # cql = QuestionPaser().parser_main(e, q, k)
    # ans = (AnswerSearcher().search_main(cql))
    # res = AnswerSearcher().answer_prettify(k, ans)
    # print(res)



