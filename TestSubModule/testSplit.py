# -*- coding:utf-8 -*-



def sub1():
    #tmpStr='我是|你等|严禁'
    tmpStr='三大类咖啡机萨达了几份'
    myArr=tmpStr.split('|')
    return myArr


newArr=sub1()
print len(newArr)


print newArr[0]


for i in newArr:
    print i

