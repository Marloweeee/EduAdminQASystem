import os
import ahocorasick

class QuestionClassifier:

    def __init__(self):

        # 实体节点询问特征词
        self.thesis_begin=['开题','论文要开题','毕设开题','开题报告','开始','开始写','写论文','开题答辩']# 开题
        self.thesis_mid=['中期','中期答辩','中期报告','中期审核','中期评审','中期检查']# 中期
        self.thesis_end=['毕设答辩','最终答辩','毕业设计答辩']# 答辩
        self.graduate=['毕业','盲审']# 毕业
        self.summer_school=['暑期课程','暑期学校','暑期选课','暑假课程','暑假学校','暑假选课']# 暑期学校
        self.course=['重修','不及格','退选','英语课','政治课','培养方案','先修课']# 课程
        self.lesson=['教学云','教学云课程查询','教学云故障']# 上课、教学云
        self.nation_scholarship=['国家奖学金']# 国家奖学金
        self.academic_scholarship=['学业奖学金']# 学业奖学金
        self.region_words=set(self.thesis_begin+self.thesis_mid+self.thesis_end+self.graduate+self.summer_school+
                              self.course+self.lesson+self.nation_scholarship+self.academic_scholarship)


        # 构建实体节点对应的属性特征疑问词
        # 1.开题+中期
        self.thesis_time=['什么时间','什么时候','大概日期','大体日期','开题时间','提交时间','提交日期']# 询问时间
        self.thesis_commit_way=['提交方式','怎么提交','如何提交','怎么去提交','怎样提交','怎样去提交']# 询问提交方式
        self.thesis_review=['如何评审','怎么评审','评审方式','怎样评审','怎么去评审','怎样去评审','评审小组','评审的方式','评审的流程','评审流程']# 评审方式
        self.thesis_title_change=['更换题目','变更题目','选题变更','选题更换','题目变更','换题','变更选题']# 换题
        self.thesis_requirements=['提交要求','有什么要求','具体要求','提交的要求','提交标准','有什么标准','具体的要求','具体的标准']
        self.thesis_not_pass=['未通过','不通过','没有通过','失败','没通过']


        # 构造actree,用于后续快速匹配输入问题中的关键词
        self.region_tree=self.build_actree(list(self.region_words))
        # 构造将关键词转化为问题类型的词典，形如{"重修":[课程]}的字典
        self.wdtype_dict=self.build_wdtype_dict()

    # 构造actree，加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    # 构造词关键对应的问题类型
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.thesis_begin:
                wd_dict[wd].append('开题')
            elif wd in self.thesis_mid:
                wd_dict[wd].append('中期')
            elif wd in self.thesis_end:
                wd_dict[wd].append('答辩')
            elif wd in self.graduate:
                wd_dict[wd].append('毕业')
            elif wd in self.summer_school:
                wd_dict[wd].append('暑期学校')
            elif wd in self.course:
                wd_dict[wd].append('课程')
            elif wd in self.lesson:
                wd_dict[wd].append('上课')
            elif wd in self.nation_scholarship:
                wd_dict[wd].append('国家奖学金')
            elif wd in self.academic_scholarship:
                wd_dict[wd].append('学业奖学金')

        return wd_dict

    def check_question_type(self, question):
        region_wds = []
        # 将输入问题与字典树中的内容相比较，得到匹配后的内容，也就是用户询问的节点领域
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)



        # 去重，防止用户多次输入相同实体名称导致的异常
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)

        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        print("final_dict:{}".format(final_dict))
        return final_dict

    # 基于特征词进行分类
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    def classify(self,question:str):


        edu_admin_dict=self.check_question_type(question)
        if not edu_admin_dict:return {}
        entity_key = list(edu_admin_dict.values())[0][0]# 实体节点

        # 收集问句中的实体节点属性及对应的问题类型
        data = {}
        data[entity_key]=[]
        question_types=[]



        # 时间
        if self.check_words(self.thesis_time, question):
            question_type = 'thesis_{}_time'.format('begin' if entity_key=="开题" else 'mid')
            data[entity_key].append('提交时间')
            question_types.append(question_type)
        # 提交方式
        if self.check_words(self.thesis_commit_way, question):
            question_type = 'thesis_{}_commit_way'.format('begin' if entity_key=="开题" else 'mid')
            data[entity_key].append('提交方式')
            question_types.append(question_type)
        # 评审小组
        if self.check_words(self.thesis_review, question):
            question_type = 'thesis_{}_review'.format('begin' if entity_key=="开题" else 'mid')
            data[entity_key].append('评审')
            question_types.append(question_type)
        # 题目变更
        if self.check_words(self.thesis_title_change, question):
            question_type = 'thesis_{}_title_change'.format('begin' if entity_key=="开题" else 'mid')
            data[entity_key].append('题目更改')
            question_types.append(question_type)
        # 要求
        if self.check_words(self.thesis_requirements, question):
            question_type = 'thesis_{}_requirements'.format('begin' if entity_key=="开题" else 'mid')
            data[entity_key].append('要求')
            question_types.append(question_type)
        # 未通过
        if self.check_words(self.thesis_not_pass, question):
            question_type = 'thesis_{}_not_pass'.format('begin' if entity_key=="开题" else 'mid')
            data[entity_key].append('未通过')
            question_types.append(question_type)

        data['question_types'] = question_types
        return data[entity_key],data['question_types'],entity_key



if __name__ == '__main__':
    print("region_words",QuestionClassifier().region_words)
    print("wdtype_dict",QuestionClassifier().build_wdtype_dict())
    print(QuestionClassifier().classify('中期报告提交时间'))






