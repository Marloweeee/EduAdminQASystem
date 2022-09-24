# coding=utf-8


from question_classifier import *


class QuestionPaser:





    def parser_main(self,e,q,k):

        entity_dict,question_types,entity_key=e,q,k
        print(entity_dict,question_types)
        cql=['MATCH (n:`论文答辩`) WHERE n.name="{}" RETURN {}'.format(entity_key,"n."+", n.".join(entity_dict))]
        return cql





if __name__ == '__main__':
    ques="开题时间是什么时候，有什么要求，提交方式"
    e,q,k=QuestionClassifier().classify(ques)
    QuestionPaser().parser_main(e,q,k)


