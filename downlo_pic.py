# -*- coding: utf-8 -*-

'''
Created on 2014-7-24
#简易版本哈，可以改进为多图片下载，然后依次编写那个下载后的picture names。
@author: Kenbin
'''
import urllib
import urllib2
import os

picurl="http://images.51cto.com/files/uploadimg/20100630/104906665.jpg"
save_path="d:/"
imgData = urllib2.urlopen(picurl).read()
# 给定图片存放名称
fileName = save_path + "ddd2.jpg"
print fileName
# 文件名是否存在
if not os.path.exists(fileName):
    output = open(fileName,'wb+')
    output.write(imgData)
    output.close()
    print "Finished download \n"
print "运行完成"