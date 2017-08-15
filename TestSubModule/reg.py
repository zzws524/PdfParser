# -*- coding:utf-8 -*-
import re
import sys


reload(sys)
sys.setdefaultencoding='utf8'




fileHd=open('a.txt','r')


regStr1=u'([\u4e00-\u9fa5]重要事项)|(重要事项[\u4e00-\u9fa5])'
regStr2=u'([\u4e00-\u9fa5]\u91cd\u8981\u4e8b\u9879)|(\u91cd\u8981\u4e8b\u9879[\u4e00-\u9fa5])'



#uniRegStr=re.compile(unicode(regStr2,"unicode-escape"))
uniRegStr=re.compile(regStr2)

for eachLine in fileHd.readlines():
    tempEachLine=eachLine.decode('utf8')
    resultFlag=re.search(uniRegStr,tempEachLine)
    if resultFlag != None:
        print 'Find it !'
        print eachLine





fileHd.close()
