# coding=utf-8


from question_classifier import *


class QuestionPaser:





    def parser_main(self,e,q,k):

        #
        entity_dict,question_types,entity_key=e,q,k


        if entity_key in ['开题','中期','答辩','毕业']:
            cql='MATCH (n:`论文答辩`) WHERE n.name="{}" RETURN {}'.format(entity_key,"n."+", n.".join(entity_dict))
        if entity_key in ['暑期学校','选课','课程']:
            cql='MATCH (n:`教学服务`) WHERE n.name="{}" RETURN {}'.format(entity_key,"n."+", n.".join(entity_dict))

        return cql





if __name__ == '__main__':
    ques="可以不参加暑期学校吗,暑期学校的成绩怎么认定"
    e,q,k=QuestionClassifier().classify(ques)
    QuestionPaser().parser_main(e,q,k)

