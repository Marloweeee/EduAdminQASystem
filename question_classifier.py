import ahocorasick

class QuestionClassifier:

    def __init__(self):

        # 实体节点询问特征词
        self.thesis_begin=['开题','论文要开题','毕设开题','开题报告','开始','开始写','写论文','开题答辩']# 开题
        self.thesis_mid=['中期','中期答辩','中期报告','中期审核','中期评审','中期检查']# 中期
        self.thesis_end=['答辩','毕设答辩','最终答辩','毕业设计答辩']# 答辩
        self.graduate=['毕业','盲审']# 毕业
        self.summer_school=['暑期课程','暑期学校','暑期选课','暑假课程','暑假学校','暑假选课','暑期','暑假']# 暑期学校
        self.course=['重修','不及格','退选','英语课','政治课','培养方案','先修课','课程','欠费','本科']# 课程
        self.lesson=['教学云','教学云课程查询','教学云故障']# 上课、教学云
        self.nation_scholarship=['国家奖学金']# 国家奖学金
        self.academic_scholarship=['学业奖学金']# 学业奖学金
        self.go_abroad=['出国','留学','国外']# 出国
        self.dual_culture=['联合培养','联培']# 联合培养
        self.competition=['竞赛','比赛']# 竞赛
        self.advanced_class=['先进班集体','先进班级','先进集体']# 先进班集体
        self.region_words=set(self.thesis_begin+self.thesis_mid+self.thesis_end+self.graduate+self.summer_school+
                              self.course+self.lesson+self.nation_scholarship+self.academic_scholarship+
                              self.go_abroad+self.dual_culture+self.competition+self.advanced_class)


        # 构建实体节点对应的属性特征疑问词
        # 1.开题+中期
        self.thesis_time=['时间','时候','日期','大体日期']# 询问时间
        self.thesis_commit_way=['方式','怎么提交','如何提交','怎么去提交','怎样提交','怎样去提交']# 询问提交方式
        self.thesis_review=['评审','怎么评审','评审方式','怎样评审','怎么去评审','怎样去评审','评审小组','评审的方式','评审的流程','评审流程']# 评审方式
        self.thesis_title_change=['更换题目','变更题目','选题变更','选题更换','题目变更','换题','变更选题']# 换题
        self.thesis_requirements=['要求','提交要求','有什么要求','具体要求','提交的要求','提交标准','标准','具体的要求','具体的标准']
        self.thesis_not_pass=['未通过','不通过','没有通过','失败','没通过']
        # 2.答辩
        self.defence_procedure=['流程','过程','步骤','流程环节','基本流程',]
        self.defence_reviewer=['评审专家','审核人','评阅专家','审核专家','专家','专家学者']
        self.defence_qualification=['资格','资质','参加答辩']
        self.defence_online=['疫情','线上','云','无法返校']
        self.defence_reviewer_qualification=['专家资格','专家要求','专家资质','专家需要什么资格',]
        self.defence_committee=['委员会','评审小组','评审委员会']
        self.defence_requirements=['要求','标准']
        # 3.毕业
        self.graduate_time=['时间','时候']
        self.graduate_qulification=['资格','审查','资质','审核']
        # 4.暑期学校
        self.summer_school_necessity=['参与','参加','必要性']
        self.summer_school_course=['选课','课程']
        self.summer_school_score_affirm=['成绩','认定']
        # 5.课程
        self.course_pre=['本科阶段','先修课','本科课程','本科修的','本科','暑期课程']
        self.course_sys_arrearage=['系统欠费','欠费','未交费','未缴费','没有交费','没有缴费']
        self.course_political=['中国特色社会主义理论与实践研究','课程替代','政治课替代','政治课',]
        self.course_english=['英语',]
        self.course_report=['成绩单','成绩']
        self.course_fail=['不及格','没及格','没有及格']
        self.course_rebuild=['重修']
        self.course_drop=['退选']
        self.course_training_plan=['培养方案','培养计划','培养手册']
        # 6.上课及教学云：上课
        self.lesson_teaching_cloud=['登录','网址','方式','途径','上课']
        self.lesson_research=['搜索','查看','课程']
        self.lesson_problem=['故障','无法跳转','实名认证','无法正常']
        self.lesson_feedback=['反馈','问题反馈']

        # 7.奖学金
        self.scholarship_review_org=['评选组织','机构']
        self.scholarship_elect_condition=['条件','资格','资质','要求']
        self.scholarship_deny=['取消','否决']
        self.scholarship_material=['材料','提交']
        self.scholarship_quota_allocation=['名额','分配']
        self.scholarship_time=['时间','时候','日期']

        # 8.出国
        self.abroad_condition=['条件','资格','资质']
        self.abroad_proj=['项目']#
        self.abroad_people=['适用人群']
        self.abroad_fee=['费用','花销','花费']
        self.abroad_amount=['数目','数量','多少个']
        self.abroad_times=['次数','多少次']
        self.abroad_application=['申请']
        self.abroad_approval=['审批','批准']

        # 9.联合培养
        self.culture_establish=['打造','建造','建立']
        self.culture_condition=['条件','资格','资质']
        self.culture_procedure=['流程','过程','程序']
        self.culture_admin=['管理',]
        self.culture_select=['选派方案','挑选']
        self.culture_outside_professor=['校外导师','企业导师','联培导师']
        self.culture_regulation=['规章','制度']
        self.culture_assess=['考核']

        # 10.竞赛
        self.competition_level=['级别','等级','评级','划分']
        self.competition_contents=['名单','目录','清单']
        self.competition_admin=['管理','协调','组织']
        self.competition_condition=['条件','资格','资质']
        self.competition_funding=['资助','经费','支持']
        self.competition_funding_principle=['多次','原则']
        self.competition_credit=['学分','奖励','激励']
        self.competition_student=['招生名额奖励']

        # 11.先进班集体
        self.ad_class_principle=['原则']
        self.ad_class_object=['对象','目标']
        self.ad_class_proportion=['比例','百分比']
        self.ad_class_condition=['资格','资质','条件']
        self.ad_class_procedure=['流程','程序','过程']
        self.ad_class_incentive=['奖励','激励','表彰']



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
                wd_dict[wd].append('开题报告')
            elif wd in self.thesis_mid:
                wd_dict[wd].append('中期报告')
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
            elif wd in self.go_abroad:
                wd_dict[wd].append('出国')
            elif wd in self.dual_culture:
                wd_dict[wd].append('联合培养')
            elif wd in self.competition:
                wd_dict[wd].append('竞赛')
            elif wd in self.advanced_class:
                wd_dict[wd].append('先进班集体')
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

        return final_dict

    # 基于特征词进行分类
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    def classify(self,question:str):


        edu_admin_dict=self.check_question_type(question)
        if not edu_admin_dict:
            return {}

        entity_key = list(edu_admin_dict.values())[0][0]# 实体节点

        # 收集问句中的实体节点属性及对应的问题类型
        data = {}
        data[entity_key]=[]
        question_types=[]


        '''开题+中期'''
        # 时间
        if self.check_words(self.thesis_time, question) and entity_key in ['开题报告','中期报告']:
            data[entity_key].append('提交时间')

        # 提交方式
        if self.check_words(self.thesis_commit_way, question) and entity_key in ['开题报告','中期报告']:
            data[entity_key].append('提交方式')

        # 评审小组
        if self.check_words(self.thesis_review, question) and entity_key in ['开题报告','中期报告']:
            data[entity_key].append('评审')

        # 题目变更
        if self.check_words(self.thesis_title_change, question) and entity_key in ['开题报告','中期报告']:
            data[entity_key].append('题目更改')

        # 要求
        if self.check_words(self.thesis_requirements, question) and entity_key in ['开题报告','中期报告']:
            data[entity_key].append('要求')

        # 未通过
        if self.check_words(self.thesis_not_pass, question) and entity_key in ['开题报告','中期报告']:
            data[entity_key].append('未通过')


        '''答辩'''
        # 答辩流程
        if self.check_words(self.defence_procedure, question) and entity_key=='答辩':
            data[entity_key].append('流程')
        # 评审专家
        if self.check_words(self.defence_reviewer, question) and entity_key=='答辩':
            data[entity_key].append('评审专家组成')
        # 答辩资格
        if self.check_words(self.defence_qualification, question) and entity_key=='答辩':
            data[entity_key].append('资格审查')
        # 在线答辩
        if self.check_words(self.defence_online, question) and entity_key=='答辩':
            data[entity_key].append('在线')
        # 评审资格
        if self.check_words(self.defence_reviewer_qualification, question) and entity_key=='答辩':
            data[entity_key].append('评审资格')
        # 答辩委员会组成
        if self.check_words(self.defence_committee, question) and entity_key=='答辩':
            data[entity_key].append('委员会组成')
        # 答辩要求
        if self.check_words(self.defence_requirements, question) and entity_key=='答辩':
            data[entity_key].append('要求')

        '''毕业'''
        # 盲审时间
        if self.check_words(self.graduate_time, question) and entity_key=='毕业':
            data[entity_key].append('盲审时间')
        # 资格审查
        if self.check_words(self.graduate_qulification, question) and entity_key=='毕业':
            data[entity_key].append('资格审查')

        '''暑期学校'''
        if self.check_words(self.summer_school_necessity, question) and entity_key == '暑期学校':
            data[entity_key].append('是否参与的标准')
        if self.check_words(self.summer_school_course, question) and entity_key == '暑期学校':
            data[entity_key].append('选课标准')
        if self.check_words(self.summer_school_score_affirm, question) and entity_key == '暑期学校':
            data[entity_key].append('成绩认定')

        '''课程'''
        # if self.check_words(self.course_pre, question) and entity_key == '课程':
        #     data[entity_key].append('先修课')
        if self.check_words(self.course_sys_arrearage, question) and entity_key == '课程':
            data[entity_key].append('系统欠费')
        # if self.check_words(self.course_political, question) and entity_key == '课程':
        #     data[entity_key].append('政治课')
        # if self.check_words(self.course_english, question) and entity_key == '课程':
        #     data[entity_key].append('英语课')
        # if self.check_words(self.course_report, question) and entity_key == '课程':
        #     data[entity_key].append('成绩单')
        if self.check_words(self.course_fail, question) and entity_key == '课程':
            data[entity_key].append('不及格')
        if self.check_words(self.course_rebuild, question) and entity_key == '课程':
            data[entity_key].append('课程重修')
        if self.check_words(self.course_drop, question) and entity_key == '课程':
            data[entity_key].append('课程退选')
        if self.check_words(self.course_training_plan, question) and entity_key == '课程':
            data[entity_key].append('培养方案')

        '''教学云上课'''
        if self.check_words(self.lesson_teaching_cloud, question) and entity_key == '上课':
            data[entity_key].append('教学云')
        if self.check_words(self.lesson_research, question) and entity_key == '上课':
            data[entity_key].append('课程查询')
        if self.check_words(self.lesson_problem, question) and entity_key == '上课':
            data[entity_key].append('教学云故障')
        if self.check_words(self.lesson_feedback, question) and entity_key == '上课':
            data[entity_key].append('反馈途径')

        '''奖学金'''
        if self.check_words(self.scholarship_review_org, question) and entity_key in ['国家奖学金','学业奖学金']:
            data[entity_key].append('评选机构')
        if self.check_words(self.scholarship_elect_condition, question) and entity_key in ['国家奖学金', '学业奖学金']:
            data[entity_key].append('参评条件')
        if self.check_words(self.scholarship_deny, question) and entity_key in ['国家奖学金','学业奖学金']:
            data[entity_key].append('取消资格')
        if self.check_words(self.scholarship_material, question) and entity_key in ['国家奖学金','学业奖学金']:
            data[entity_key].append('材料要求')
        if self.check_words(self.scholarship_quota_allocation, question) and entity_key in ['国家奖学金','学业奖学金']:
            data[entity_key].append('名额分配')
        if self.check_words(self.scholarship_time, question) and entity_key in ['国家奖学金','学业奖学金']:
            data[entity_key].append('发放时间')

        '''出国'''
        if self.check_words(self.abroad_condition,question) and entity_key=='出国':
            data[entity_key].append('条件')
        if self.check_words(self.abroad_proj,question) and entity_key=='出国':
            data[entity_key].append('交流项目')
        if self.check_words(self.abroad_people,question) and entity_key=='出国':
            data[entity_key].append('适用人群')
        if self.check_words(self.abroad_fee,question) and entity_key=='出国':
            data[entity_key].append('会议费用标准')
        if self.check_words(self.abroad_amount, question) and entity_key == '出国':
            data[entity_key].append('数量')
        if self.check_words(self.abroad_times,question) and entity_key=='出国':
            data[entity_key].append('次数')
        if self.check_words(self.abroad_application,question) and entity_key=='出国':
            data[entity_key].append('申请')
        if self.check_words(self.abroad_approval,question) and entity_key=='出国':
            data[entity_key].append('审批')

        '''联合培养'''
        if self.check_words(self.culture_establish,question) and entity_key=='联合培养':
            data[entity_key].append('建立途径')
        if self.check_words(self.culture_condition,question) and entity_key=='联合培养':
            data[entity_key].append('单位条件')
        if self.check_words(self.culture_procedure,question) and entity_key=='联合培养':
            data[entity_key].append('建立程序')
        if self.check_words(self.culture_admin,question) and entity_key=='联合培养':
            data[entity_key].append('管理模式')
        if self.check_words(self.culture_select,question) and entity_key=='联合培养':
            data[entity_key].append('选派方案')
        if self.check_words(self.culture_outside_professor,question) and entity_key=='联合培养':
            data[entity_key].append('校外导师')
        if self.check_words(self.culture_regulation,question) and entity_key=='联合培养':
            data[entity_key].append('规章制度')
        if self.check_words(self.culture_assess,question) and entity_key=='联合培养':
            data[entity_key].append('考核')

        '''竞赛'''
        if self.check_words(self.competition_level,question) and entity_key=='竞赛':
            data[entity_key].append('竞赛等级')
        if self.check_words(self.competition_contents, question) and entity_key == '竞赛':
            data[entity_key].append('竞赛目录')
        if self.check_words(self.competition_admin,question) and entity_key=='竞赛':
            data[entity_key].append('管理')
        if self.check_words(self.competition_condition,question) and entity_key=='竞赛':
            data[entity_key].append('参赛条件')
        if self.check_words(self.competition_funding,question) and entity_key=='竞赛':
            data[entity_key].append('参赛资助')
        if self.check_words(self.competition_funding_principle,question) and entity_key=='竞赛':
            data[entity_key].append('资金奖励原则')
        if self.check_words(self.competition_credit,question) and entity_key=='竞赛':
            data[entity_key].append('学分奖励')
        if self.check_words(self.competition_student,question) and entity_key=='竞赛':
            data[entity_key].append('招生名额奖励')

        '''先进班集体'''
        if self.check_words(self.ad_class_principle,question) and entity_key=='先进班集体':
            data[entity_key].append('原则')
        if self.check_words(self.ad_class_object,question) and entity_key=='先进班集体':
            data[entity_key].append('对象')
        if self.check_words(self.ad_class_proportion,question) and entity_key=='先进班集体':
            data[entity_key].append('比例')
        if self.check_words(self.ad_class_condition,question) and entity_key=='先进班集体':
            data[entity_key].append('评选条件')
        if self.check_words(self.ad_class_procedure,question) and entity_key=='先进班集体':
            data[entity_key].append('评选程序')
        if self.check_words(self.ad_class_incentive,question) and entity_key=='先进班集体':
            data[entity_key].append('表彰办法')




        data['question_types'] = question_types
        return data[entity_key],data['question_types'],entity_key



if __name__ == '__main__':
    print("region_words",QuestionClassifier().region_words)
    print("wdtype_dict",QuestionClassifier().build_wdtype_dict())
    print(QuestionClassifier().classify('申请出国的方式'))






