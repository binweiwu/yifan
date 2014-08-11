#!/usr/bin/etc python
# -*- coding: utf-8 -*-

import MySQLdb
import ConfigParser
import datetime
import xlwt

#数据库连接
cf = ConfigParser.ConfigParser()
cf.read('/data/db.ini')
conn = MySQLdb.Connect(
        host = cf.get('dw','host'),
        user = cf.get('dw','user'),
        passwd = cf.get('dw','passwd'),
        db = cf.get('dw','db'),
        port = int(cf.get('dw','port')))
conn.set_character_set('utf8')
cur = conn.cursor()
#日期获取
today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days = 1)
#excel文件名
FILE_NAME = "rec_courses_" + str(yesterday) + ".xls"
excel = xlwt.Workbook(encoding = 'utf-8') #打开一个工作表
#添加工作薄
##第一个工作薄
FIELDS1 = ('样本课程编号','推荐课程编号')
sql1 = """
    select www_id as sam_course_id, group_concat(rec_course_id order by score_final desc) as rec_courses_id 
    from dw_rec_course12 group by sam_course_id;
"""
cur.execute(sql1)
result_set1 = cur.fetchall() #获取数据
print "get the result1"

sheet1 = excel.add_sheet("课程推荐")
sheet1.col(0).width = 3000
sheet1.col(1).width = 7000

colnum = 0
rownum = 0
for field in FIELDS1:#写入标题
    sheet1.write(rownum,colnum,field)
    colnum += 1
else:
    rownum += 1

def write_row1(sheet,result,row_num):
    colnum = 0
    sheet.write(row_num,colnum,result[0])
    colnum += 1
    sheet.write(row_num,colnum,result[1])

for single_result in result_set1:
    write_row1(sheet1,single_result,rownum)
    rownum += 1

#第二个工作薄
FIELDS2 = ('样本课程编号','样本课程名称','推荐课程编号及名称')
sql2 = """
select www_id as sam_course_id, sam_course, group_concat(concat_ws(": ",rec_course_id,rec_course) order by score_final desc) as rec_courses 
from 
(select drc.www_id,c1.name as sam_course,drc.rec_course_id,c2.name as rec_course,drc.score_final 
from dw_rec_course12 as drc
left join www_courses as c1 on drc.www_id = c1.id
left join www_courses as c2 on drc.www_id = c2.id) as rec_h12
group by sam_course_id;
"""
cur.execute(sql2)
result_set2 = cur.fetchall()

print "get the result2"

sheet2 = excel.add_sheet("课程推荐详情")
sheet2.col(0).width = 3000
sheet2.col(1).width = 6000
sheet2.col(2).width = 17000

colnum = 0
rownum = 0
for field in FIELDS2:
    sheet2.write(rownum, colnum, field)
    colnum += 1
else:
    rownum += 1

def write_row2(sheet,result,row_num):
    colnum = 0
    sheet.write(row_num,colnum,result[0])
    colnum += 1
    sheet.write(row_num,colnum,result[1])
    colnum += 1
    sheet.write(row_num,colnum,result[2])

for single_result in result_set2:
    write_row2(sheet2,single_result,rownum)
    rownum += 1

##保存工作表并关闭数据库
excel.save(FILE_NAME)
cur.close()
conn.close()
print "end!!"



