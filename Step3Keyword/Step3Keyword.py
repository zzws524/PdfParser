# -*- coding:utf-8 -*-
import sys
import os
import re
import datetime


def to_my_log(myContent):
    logFileHd=open("log.txt",'a')
    now=datetime.datetime.now()
    logFileHd.write(now.strftime('%Y-%m-%d %H:%M:%S')+"    ")
    print now.strftime('%Y-%m-%d %H:%M:%S')+"    ",
    logFileHd.write(myContent+"\n")
    print myContent
    logFileHd.close()

def to_my_summary(myContent):
    summaryFileHd=open("Summary.csv",'a')
    summaryFileHd.write(myContent+"\n")
    summaryFileHd.close()


def _get_end_word(filePath):
    tempFileHd=open(filePath,'r')
    tempFileHd.readline()
    tempEndWordRaw=tempFileHd.readline()
    tempEndWordFinal=tempEndWordRaw.replace('\t','').replace('\n','').replace(' ','')
    endArr=tempEndWordFinal.split("|")
    #for tempEachEnd in endArr:
    #    print tempEachEnd+"for debug purpose"
    return endArr



def _get_start_word(filePath):
    tempFileHd=open(filePath,'r')
    tempStartWordRaw=tempFileHd.readline()
    tempStartWordFinal=tempStartWordRaw.replace('\t','').replace('\n','').replace(' ','')
    startArr=tempStartWordFinal.split("|")
    #for tempEachStart in startArr:
    #    print tempEachStart+"for debug purpose"     #debug purpse
    return  startArr

def _get_keywords(filePath):
    tempFileHd=open(filePath,'r')
    tempAllKeywords=[]
    for eachLine in tempFileHd.readlines():
        tempEachItem=eachLine.replace('\t','').replace('\n','').replace(' ','')
        if tempEachItem !='':
            tempAllKeywords.append(tempEachItem)
            #print tempEachItem   #for debug
    return tempAllKeywords



def _parse_txt_file(filePath,startWord,endWord):
    initCounter=0     #start to count line btw start word and end word.
    counterStartFlag=False
    minLineNumber=10  #at least 10 lines btw start and end word. Otherwise, it's catalog
    tempContentStr=''

    try:
        tempStartStr=u'([\u4e00-\u9fa5]'+unicode(startWord)+u')|('+unicode(startWord)+u'[\u4e00-\u9fa5]'+u')'
        uniStartWordReg=re.compile(tempStartStr)

        tempEndStr=u'([\u4e00-\u9fa5]'+unicode(endWord)+u')|('+unicode(endWord)+u'[\u4e00-\u9fa5]'+u')'
        uniEndWordReg=re.compile(tempEndStr)

    except ValueError:
        to_my_log("Error: something went wrong when script try to parse start word and end word.")
        sys.exit()


    tempFileHd=open(filePath,'r')


    for eachLine in tempFileHd.readlines():
        uniEachline=eachLine.decode('utf8')
        if re.search(startWord,eachLine) != None and re.search(uniStartWordReg,uniEachline)==None:
            #print eachLine    #debug: print line if start word is found.
            counterStartFlag=True
        if counterStartFlag==True:
            initCounter=initCounter+1
            tempContentStr=tempContentStr+eachLine
        if re.search(endWord,eachLine) != None and re.search(uniEndWordReg,uniEachline)==None:
            #print eachLine    #debug: print line if end word is found.
            counterStartFlag=False
            if initCounter<minLineNumber:
                tempContentStr=''

    if counterStartFlag==True:
        #print "Only find start word, but missing end word"   #debug:if only start word is found, ignore it.
        tempContentStr=''

    return tempContentStr



def _pull_keyword(keyContent,filePath):
    currentPath=os.getcwd()
    configKeywordsPath=currentPath+"/Config/KeyWords.txt"
    keyWords=_get_keywords(configKeywordsPath)
    if os.path.isfile(configKeywordsPath)!=True:
        to_my_log("No config files or wrong file name")
        sys.exit()

    for eachKeyWord in keyWords:
        tempPattern=re.compile(eachKeyWord)
        tmpFindAll=tempPattern.findall(keyContent)
        to_my_log("find "+str(len(tmpFindAll))+' '+eachKeyWord)
        to_my_summary(filePath+","+"Find Content,"+eachKeyWord+","+str(len(tmpFindAll))+",")






def summarize__txt_file(eachFilePath):
    to_my_log('---------------------')
    to_my_log("start to parse "+eachFilePath)
    currentPath=os.getcwd()
    configStartToEndPath=currentPath+"/Config/StartToEnd.txt"

    if os.path.isfile(configStartToEndPath)!=True:
        to_my_log("No config files or wrong file name")
        sys.exit()

    startWordArr=_get_start_word(configStartToEndPath)
    endWordArr=_get_end_word(configStartToEndPath)
    findKeyContentFlag=False

    for startWord in startWordArr:
        for endWord in endWordArr:
            to_my_log("Search between " + startWord + " to " +endWord)
            myContent=_parse_txt_file(eachFilePath,startWord,endWord)
            if myContent != "":
                to_my_log("Find contents between two keywords :) Stop searching...")
                findKeyContentFlag=True
                break
            else:
                to_my_log("Not found anything between two keywords. Continue searching...")
        else:
            continue
        break

    if findKeyContentFlag==False:
        to_my_log("Warning: Didn't find anything between two keywords for this file. Please check.")
        to_my_summary(eachFilePath+","+"No Content,"+"N/A"+","+"N/A"+",")
    else:
        _pull_keyword(myContent,eachFilePath)






if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    currentPath=os.getcwd()
    txtFilesPath=currentPath+"/TXTs"
    txtFolders=os.listdir(txtFilesPath)

    sumFileHd=open("Summary.csv","w")
    sumFileHd.write("File Name,Search Content,Key Words,Quantity,\n")
    sumFileHd.close()

    for eachTxtFolder in txtFolders:
        eachTxtFolderPath=txtFilesPath+"/"+eachTxtFolder
        txtFinalcialStatements=os.listdir(eachTxtFolderPath)

        for eachTxtFinaStatement in txtFinalcialStatements:
            tempEachTxtFinaStatementPath=eachTxtFolderPath+"/"+eachTxtFinaStatement
            summarize__txt_file(tempEachTxtFinaStatementPath)

