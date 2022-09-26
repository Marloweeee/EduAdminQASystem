# coding=utf-8


from question_classifier import *


class QuestionPaser:





    def parser_main(self,e,q,k):

        #
        entity_dict,question_types,entity_key=e,q,k


        if entity_key in ['开题报告','中期报告','答辩','毕业']:
            cql='MATCH (n:`论文答辩`) WHERE n.name="{}" RETURN {}'.format(entity_key,"n."+", n.".join(entity_dict))
        if entity_key in ['暑期学校','选课','上课']:
            cql='MATCH (n:`教学服务`) WHERE n.name="{}" RETURN {}'.format(entity_key,"n."+", n.".join(entity_dict))
        if entity_key in ['国家奖学金','学业奖学金']:
            cql='MATCH (n:`先进个人`) WHERE n.name="{}" RETURN {}'.format(entity_key,"n."+", n.".join(entity_dict))

        return cql





if __name__ == '__main__':
    pass


