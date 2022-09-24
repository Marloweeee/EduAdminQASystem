# coding=utf-8

from py2neo import Graph
from question_parse import *

class AnswerSearcher:

    def __init__(self):
        self.graph=Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="112099")

    def search_main(self,cql):

        anwser=[]
        for query in cql:
            res=self.graph.run(query).data()
            anwser+=res

        return anwser

if __name__ == '__main__':
    ques = "开题时间是什么时候，有什么要求"
    e, q, k = QuestionClassifier().classify(ques)
    cql=QuestionPaser().parser_main(e,q,k)
    ans=(AnswerSearcher().search_main(cql))

