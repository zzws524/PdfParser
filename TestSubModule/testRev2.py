# -*- coding:utf-8 -*-

import re
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf8')


searchTxt='重要事项等'
newSearchTxt=searchTxt.decode('utf8')
uniSearchTxt=str([unicode(searchTxt,'utf-8')])





temReg=re.compile(u'重要事项([\u4e00-\u9fa5])')

regResult=re.search(temReg,newSearchTxt)

if regResult !=None:
    print "find it"
    print regResult.group(1).encode('utf8')
else:
    print "not find"
