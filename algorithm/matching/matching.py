import os
import sys
import subprocess
import datetime
import time
import io
import re
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial

from TemplateList import templatebyProf
from TemplateList import templatebyYJH
from TemplateList import errored

def GetTemplateCountVecEx(inputDir):
    targetFile = inputDir +"/*.log"

    hadoopLogTemplate = templatebyProf + templatebyYJH + errored

    command = 'cat '+targetFile+' | cut -d" " -f3-'
    catResult = subprocess.check_output(command,shell=True).decode()
    catResultIO = io.StringIO(catResult)
    logLevelList = ["INFO","DEBUG","WARN","ERROR"]
    templateListLen = len(hadoopLogTemplate)

    templateCountVec = [0 for _ in range(templateListLen +1)]

    for line in catResultIO.readlines():
        log = line.strip("\n")
        logFlag = 0
        
        #this loop is for Data cleaning // ignore the line not to have log level string 
        for logLevel in logLevelList:
            if logLevel in log :
                logFlag =1
                break
        if logFlag != 1:
            continue

        flag=0
        for i in range(0,templateListLen):
            matched = re.match(hadoopLogTemplate[i],log)
            if matched !=None:
                templateCountVec[i] = templateCountVec[i]+1
                flag = 1
                break
        if flag !=1:
            templateCountVec[templateListLen] = templateCountVec[templateListLen] + 1

    return templateCountVec

def GetTemplateTree(hadoopLogTemplate):
    classDict = {"WARN":dict(),"DEBUG":dict(),"ERROR":dict(),"INFO":dict()}
    index = 0
    for template in hadoopLogTemplate:
        splitedList=template.split()
        logLevel = splitedList[0].strip(":")
        component = splitedList[1]
        if classDict[logLevel].get(component) == None :
            classDict[logLevel][component] = list()
        classDict[logLevel][component].append(index)

        index+=1

    return classDict

def GetTemplateCountVecOnly(inputDir):
    targetFile = inputDir +"/*.log"

    hadoopLogTemplate = templatebyProf + templatebyYJH + errored

    command = 'cat '+targetFile+' | cut -d" " -f3-'
    catResult = subprocess.check_output(command,shell=True).decode()
    catResultIO = io.StringIO(catResult)
    logLevelList = ["INFO","DEBUG","WARN","ERROR"]
    templateListLen = len(hadoopLogTemplate)

    classDict = GetTemplateTree(hadoopLogTemplate)

    templateCountVec = [0 for _ in range(templateListLen +1)]

    for line in catResultIO.readlines():
        log = line.strip("\n")
        logFlag = 0
        
        level="NULL"

        #this loop is for Data cleaning // ignore the line not to have log level string
        for logLevel in logLevelList:
            if logLevel in log :
                logFlag =1
                level = logLevel
                break
        if logFlag != 1:
            continue
        
        component= line.split()[1]
        
        if classDict[level].get(component) == None:
            templateCountVec[templateListLen] = templateCountVec[templateListLen] + 1        
            continue
        validTemplateList = classDict[level][component]
        flag=0
        for i in validTemplateList:
            matched = re.match(hadoopLogTemplate[i],log)
            if matched !=None:
                templateCountVec[i] = templateCountVec[i]+1
                flag = 1
                break
        if flag !=1:
            templateCountVec[templateListLen] = templateCountVec[templateListLen] + 1

    return templateCountVec

def GetTemplateCountVecWith(inputDir):
    targetFile = inputDir +"/*.log"

    hadoopLogTemplate = templatebyProf + templatebyYJH + errored

    command = 'cat '+targetFile+' | cut -d" " -f3-'
    catResult = subprocess.check_output(command,shell=True).decode()
    catResultIO = io.StringIO(catResult)
    logLevelList = ["INFO","DEBUG","WARN","ERROR"]
    templateListLen = len(hadoopLogTemplate)

    classDict = GetTemplateTree(hadoopLogTemplate)

    templateCountVec = [0 for _ in range(templateListLen +1)]

    mostRecentTemplate = 0
    for line in catResultIO.readlines():
        log = line.strip("\n")
        logFlag = 0

        level="NULL"

        #this loop is for Data cleaning // ignore the line not to have log level string
        for logLevel in logLevelList:
            if logLevel in log :
                logFlag =1
                level = logLevel
                break
        if logFlag != 1:
            continue

        component= line.split()[1]

        if classDict[level].get(component) == None:
            templateCountVec[templateListLen] = templateCountVec[templateListLen] + 1
            continue

        if re.match(hadoopLogTemplate[mostRecentTemplate],log) != None:
            templateCountVec[mostRecentTemplate] = templateCountVec[mostRecentTemplate]+1
            tflag = 1
            break

        validTemplateList = classDict[level][component]
        flag = 0
        index = 0
        for i in validTemplateList:
            matched = re.match(hadoopLogTemplate[i],log)
            if matched !=None:
                templateCountVec[i] = templateCountVec[i]+1
                flag = 1
                mostRecentTemplate = i
                break
            index +=1
        if flag !=1:
            templateCountVec[templateListLen] = templateCountVec[templateListLen] + 1

    return templateCountVec

if __name__ == "__main__":
    classDict = dict()

    targetDir3 = "/root/stdlog/pi"
    targetDir8 = "/root/stdlog/pagerank"
    targetDir28 = "/root/stdlog/sparktc"

    startTime = time.time()
    GetTemplateCountVecOnly(targetDir3)
    endTime3 = time.time() - startTime

    startTime = time.time()
    GetTemplateCountVecOnly(targetDir8)
    endTime8 = time.time() - startTime

    startTime = time.time()
    GetTemplateCountVecOnly(targetDir28)
    endTime28 = time.time() - startTime

    print("Only")
    print(endTime3)
    print(endTime8)
    print(endTime28)


    startTime = time.time()
    GetTemplateCountVecWith(targetDir3)
    endTime3 = time.time() - startTime

    startTime = time.time()
    GetTemplateCountVecWith(targetDir8)
    endTime8 = time.time() - startTime

    startTime = time.time()
    GetTemplateCountVecWith(targetDir28)
    endTime28 = time.time() - startTime
    print("with")
    print(endTime3)
    print(endTime8)
    print(endTime28)
