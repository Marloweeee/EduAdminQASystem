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


        res=self.graph.run(cql).data()

        return res[0]
    def answer_prettify(self,entity_key,answers):
        if not answers:
            return ''

        attribute=list(answers.keys())
        context=list(answers.values())
        context_len=len(attribute)
        ans=''

        for idx in range(context_len):
            ans+=("{}的{}是：\n{}\n".format(entity_key,attribute[idx].split('.')[1],context[idx]))


        return ans




if __name__ == '__main__':

    ques = "可以不参加暑期学校吗,暑期学校的成绩怎么认定"
    e, q, k = QuestionClassifier().classify(ques)
    cql=QuestionPaser().parser_main(e,q,k)
    ans=(AnswerSearcher().search_main(cql))
    res=AnswerSearcher().answer_prettify(k,ans)
    print(res)


