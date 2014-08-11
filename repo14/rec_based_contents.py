#!/usr/bin/env python
# -*- encoding:utf-8 -*-

'''
Created on 2014-08-11

@author: kkb
'''
###方法一： 基于内容的推荐
import MySQLdb
import ConfigParser
import numpy as np
import jieba
import copy
import math
from collections import OrderedDict
config_parser = ConfigParser.ConfigParser()
config_parser.read('/data/db.ini')
conn_to_mysql = MySQLdb.connect(
        host=config_parser.get('dw', 'host'),
        user=config_parser.get('dw', 'user'),
        passwd=config_parser.get('dw', 'passwd'),
        db=config_parser.get('dw', 'db'),
        port=int(config_parser.get('dw', 'port')))
conn_to_mysql.set_character_set('utf8')
conn_to_mysql.ping(True)
cursor_to_mysql = conn_to_mysql.cursor()
jieba.load_userdict("/home/ubuntu/bingo/rec_file/user.dict")##可改进词语匹配（一般不需用）

scores_dict = {}#保存成绩

def get_cossimi(x,y): #余弦相似计算公式
    myx = np.array(x)
    myy = np.array(y)
    cos1 = np.sum(myx * myy)
    cos21 = np.sqrt(sum(myx * myx)+0.001)
    cos22 = np.sqrt(sum(myy * myy)+0.001)
    return cos1 / float(cos21*cos22)

def get_seg_list(course_info):#中文分词
    tmp_seg_list = jieba.cut(course_info, cut_all=True)
    return tmp_seg_list 

def topMatchesContent(sam_course,sam_course_id,num = 10): #取推荐的topN
    segs_list = []
    for course in course_origen_info:
        segs_list.append(get_seg_list(course[2]))
         
    sam_seg_list = get_seg_list(sam_course)
    f_stop = open('/home/ubuntu/bingo/rec_file/stopwords.txt','r')
    try:  
        f_stop_text = f_stop.read( )
        f_stop_text=unicode(f_stop_text,'utf-8')
    finally:  
        f_stop.close( ) 
    stop_seg_list=f_stop_text.split('\n')
    
    test_words = {}
    all_words = {}
    for myword in sam_seg_list:
        if not(myword.strip() in stop_seg_list):
            test_words.setdefault(myword, 0)
            all_words.setdefault(myword, 0)
            all_words[ myword ] += 1
    
    tmp_word_list = []
    for segs in segs_list:
        tmp_words = copy.deepcopy(test_words)
        for myword in segs:
            if not(myword.strip() in stop_seg_list):
                if tmp_words.has_key(myword):
                    tmp_words[myword]+=1
        tmp_word_list.append(tmp_words)
    
    samp_data = []
    test_data = [[] for row in range(len(tmp_word_list))]
    for key in all_words.keys():
        samp_data.append(all_words[key])
        for i in range(len(tmp_word_list)):
            test_data[i].append(tmp_word_list[i][key])
    test_simi = []
    for eachData in test_data:
        test_simi.append(get_cossimi(samp_data, eachData))   
    kkb_course = {}
    for i in range(len(course_origen_info)):
        kkb_course[course_origen_info[i][0]]=test_simi[i]
    tmp_dict_list = []
    paixu =  OrderedDict(sorted(kkb_course.items(), key=lambda t: t[1]))
    paixu.popitem()
    for i in range(num): #取top10
#     for i in range(2,len(course_origen_info)): #取出所有的
        tmp_list = paixu.popitem()
        tmp_dict = {"rec_id":tmp_list[0],"score1":tmp_list[1],"score2":0.0,"total":0.0}
        tmp_dict_list.append(tmp_dict)
    print tmp_dict_list
        
    scores_dict.update({sam_course_id: tmp_dict_list})
    
#计算用户信息的权重
##第一个方法：：
##从www_courses表里读取并拼接课程描述文本信息，取出,注意课程的status一定得是"online"
sql12 = """
SELECT a.id, a.name, CONCAT_WS(', ',a.name,a.name,a.name,a.name,a.slogan,a.slogan,a.slogan,a.intro,a.`desc`, t.name,t.name,t.name,t.name,t.desc,t.desc) as course_info 
from  www_courses a LEFT OUTER JOIN www_categories t on a.category_id = t.id where a.status = "online"
"""
cursor_to_mysql.execute(sql12)
course_origen_info = cursor_to_mysql.fetchall()

for i in range(len(course_origen_info)) :
    topMatchesContent(course_origen_info[i][2],course_origen_info[i][0])

total_score1 = 0.001
# total_score2 = 0.0000001
for course_id in scores_dict:
    for tmp_dict in scores_dict[course_id]:
        total_score1 += tmp_dict["score1"]
#         total_score2 += tmp_dict["score2"]
    for tp_dict in scores_dict[course_id]:
        tp_dict["total"] = (tp_dict["score1"]) / (total_score1)*10
    total_score1 = 0.001
#     total_score2 = 0.0000001
# 
sql1 = """
drop table if exists dw_rec_course12
"""
cursor_to_mysql.execute(sql1)
conn_to_mysql.commit() 
sql2 = """
create table dw_rec_course12 (www_id int(11),rec_course_id int(11),
        score_content float, score_final float)
"""
cursor_to_mysql.execute(sql2)
conn_to_mysql.commit() 
 
for course in scores_dict:
    tmp_list = scores_dict[course]
    for i in range(len(tmp_list)):
        cursor_to_mysql.execute('''insert into dw_rec_course12(www_id,rec_course_id,
        score_content,score_final) values(%s,%s,%s,%s) ''' 
        %(course,tmp_list[i]["rec_id"],tmp_list[i]["score1"],tmp_list[i]["total"]))

conn_to_mysql.commit()  
cursor_to_mysql.close()
conn_to_mysql.close()
    