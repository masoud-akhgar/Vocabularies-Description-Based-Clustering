import re
import psycopg2
from parsivar import Normalizer, FindStems, POSTagger
from collections import Counter
from SchoolIdClass import SchoolId
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hazm import *
import sys
import urllib.parse
import mysql.connector
from main import PredictionWords
con = mysql.connector.connect(host="Censored", user="Censored",password="Censored", database="Censored",auth_plugin='Censored')
cursor=con.cursor()
query = "SELECT ut.id,ut.subject,ut.url,ut.user_id,ut.parameters,ut.created_at FROM `Censored` as ut WHERE 1;"
cursor.execute(query)
table = cursor.fetchall()
df = pd.DataFrame (table, columns = ['id','subject','url','user_id','parameters','created_at'])
allWords=[]
allWordsWithCities=[]
allWordsWithCategories=[]
citiesAndUnuseful = SchoolId.getCities()

def dateAndTime(fdate,tdate):
    global df
    dfid = df['id']
    date = df['created_at'][:]#[:10]
    time = df['created_at'][:]#[11:20]
    fday,fmonth,fyear = fdate
    tday,tmonth,tyear = tdate
    minId=10000000;maxId=-1
    flag=False
    # cnt=0
    print(fday,fmonth,fyear,tday,tmonth,tyear)

    for index in range(len(date)):
        el = str(date[index])
        if len(el)==0 or el=="NaT":
            el="2022-04-20 10:27:10"
        year = int(el[:4])
        month = int(el[5:7])
        day = int(el[8:10])

        if (year,month,day) >= (fyear,fmonth,fday) and (year,month,day) <= (tyear,tmonth,tday):
            minId = min(minId,dfid[index])
            maxId = max(dfid[index],maxId)
            # if (month,day) <= (tmonth,tday) and (month,day) >= (fmonth,fday):
            #     minId = min(minId,dfid[index])
            #     maxId = max(dfid[index],maxId)
    # print(cnt)
    # return


        # if >fyear and int(el[:4])<tyear:
        #     flag=True

        # if int(el[:4])==fyear or int(el[:4])==tyear:
        #     if (int(el[5:7])>fmonth and int(el[5:7])<tmonth):
        #         flag=True

        # if int(el[5:7])==fmonth or int(el[:4])==tmonth:
        #     if int(el[8:10])>=fday and int(el[8:10])<=tday:
        #         flag=True

        # if flag==True:
        #     if minId>dfid[index]:
        #         minId=dfid[index]
        #     if maxId<dfid[index]:
        #         maxId=dfid[index]

    return (minId,maxId)
            
def extractedSearchedTerm(arr, index):
    global allWords,citiesAndUnuseful
    urlParts = ["cityId",'regionId',"category","age",'gender',"courseSchool","="]
    persianSearchedTerm=""
    for jarr in arr:
        for jremove in urlParts:
            if jremove in jarr:
                jarr = jarr.replace(jremove,"")
        jarr = jarr.replace("+"," ")
        if "%" in jarr:
            persianSearchedTerm = urllib.parse.unquote(jarr)
            persianSearchedTerm = persianSearchedTerm.replace("�","").replace("%","").replace("8","")
            persianArr = persianSearchedTerm.split()
            persianArr = [w for w in persianArr if not w in citiesAndUnuseful and len(w)>1]  # delete contining سال
            allWords.append((index , persianArr))
    return persianSearchedTerm

def extractedSearchedCategory(arr, index):
    global allWordsWithCategories
    for jarr in arr:
        if "category" in jarr:
            if "%" in jarr:
                continue
            allWordsWithCategories.append((index,int(jarr[9:])))
    return

def extractedSearchedCity(arr, index):
    global allWordsWithCategories
    for jarr in arr:
        if "cityId" in jarr:
            if "undefined" in jarr or jarr[7:]=="":
                continue
            
            allWordsWithCities.append((index,int(jarr[7:])))
    return

def makeUnikCities():
    wordSet={''}
    file1 = open('cities.txt', 'r') # orginal deleted!...
    Lines = file1.readlines()
    file = open('cities.txt', 'w')
    for line in Lines:
        wordSet.add(line.strip())

    for line in wordSet:
        file.write(line+' \n')
    file.close()

def flatteningArr(counts):
    arr=[]
    for sublist in counts:
        if isinstance(sublist[1],list):
            for item in sublist[1]:
                arr.append((sublist[0],item))
        else:
            arr.append((sublist[0],sublist[1]))
    return arr

def extractedFilteredWordsInTime(fdate,tdate):
    global allWords
    rangeId = dateAndTime(fdate,tdate) # (1,29000) #
    counts=[]
    for w in allWords:
        if w[0]<rangeId[0] or w[0]>rangeId[1]:
            continue
        counts.append(w)

    return counts

def findSearchedTerm():
    global df,allWords,citiesAndUnuseful,allWordsWithCities
    df2 = pd.read_csv('citiesId.csv',encoding = "utf8")
    dfid = df['id']
    subject = df['subject']
    parameters = df['parameters']
    url = df['url']
    print("ok")

    for index in range(len(dfid)):
        el = str(subject[index])
        elUrl = url[index]
        para=parameters[index]

        if el=="resultPage":
            remainedUrl = elUrl[elUrl.find("searchInput=")+12:]
            if remainedUrl!="":
                findex = para.find('"')+14
                findex = para.find('"',findex)+1
                sindex = para.find('"',findex+1)
                finalString = para[findex:sindex]
                finalString = re.sub(r'[^\w]', ' ', finalString)
                finalString = re.sub('[a-z]+', ' ', finalString)
                finalString = re.sub('[0-9]+', ' ', finalString)
                finalString = finalString.split()           # convert to array
                finalString2=finalString
                for el in citiesAndUnuseful:
                    for fel in finalString:
                        if el==fel and len(el)!=0:
                            select = df2["name"]==el
                            if len(df2.loc[select]["id"].to_numpy())!=0:
                                allWordsWithCities.append((index,df2.loc[select]["id"].to_numpy()[0]))
                            finalString2 = list(filter((fel).__ne__, finalString2))
                            continue

                if len(finalString2)>1:
                    allWords.append((index,finalString2))
                # return para[findex:sindex]
        
        if el=="search":
            burntString = elUrl.find('search?q=')+9
            if burntString<10:
                burntString = elUrl.find('search?=')+8
            # &cityId=  &regionId=   &category=  &age=   &gender=   &courseSchool
            arr = elUrl[burntString:].split("&")
            extractedSearchedTerm(arr,index)
            extractedSearchedCategory(arr,index)
            extractedSearchedCity(arr,index)

def possibleSplitedWords(content): # RECEIVE ARRAY OR FILE => splitted word
    global allWords
    arrExpected = ["ها","های","سار","سان","کار","گر","وار","واره","وند","وار","ور","ی","ات","یی","یان"]
    newContent=[]
    stopWords = SchoolId.getStopWords()
    flag=False

    for element in content:
        # split not inserted space
        if len(element)>=8:
            for j in range(3,len(element)-3):
                if (element[:j] in allWords or element[:j] in stopWords) and (element[j:] in allWords or element[j:] in stopWords):
                    newContent.append(element[:j])
                    newContent.append(element[j:])
        else:
            newContent.append(element)

    newContent.append(element[:-1]+"گان")
    for j in arrExpected:
        newContent.append(element+j)
        newContent.append(element+" "+j)

    return newContent

def plotTouple(touple):
    names = list(map(list, zip(*touple)))[0]
    values = list(map(list, zip(*touple)))[1]
    plt.bar(names, values, width=0.3)
    plt.rcParams.update({'font.size': 12})
    plt.xticks(rotation=40)
    plt.rcParams['font.size'] = '12'
    plt.show()

def displayNumberOfOccuranceInTime(string,fdate,tdate,time,plotChart):
    global allWords
    if time:
        counts = extractedFilteredWordsInTime(fdate,tdate)
    else:
        counts = allWords
    counts=flatteningArr(counts)
    if len(string)==0:
        counts = list(map(list, zip(*counts)))[1]
        counts = sorted(Counter(counts).items(), key=lambda tup: tup[1])[-20:]
        if plotChart:
            plotTouple(counts)
        return counts
    else:
        cases = possibleSplitedWords([string])
        cases.append(string)
        answers=[]

        counts = list(map(list, zip(*counts)))[1]
        for el in Counter(counts).items():
            for case in cases:
                if el[0]==case:
                    answers.append(el)
                    break
        if plotChart:
            plotTouple(answers)      

def displayNumberOfOccuranceInCities(string, fdate, tdate, time, name):
    global allWords,allWordsWithCities
    allWords2=allWords
    if time:
        allWords2 = extractedFilteredWordsInTime(fdate, tdate)
    fArr = flatteningArr(allWords2);index1=0
    sArr = allWordsWithCities;index2=0
    if name:
        df2 = pd.read_csv('citiesId.csv',encoding = "utf8")
    
    arr=[]
    while True:
        if index1==len(fArr) or index2==len(sArr) :
            break
        if fArr[index1][1]!=string:
            index1+=1
            continue
        elif fArr[index1][0]<sArr[index2][0]:
            index1+=1
        elif fArr[index1][0]>sArr[index2][0]:
            index2+=1
        else:
            if name:
                select = df2["id"]==sArr[index2][1]
                if len(df2.loc[select]["name"].to_numpy())!=0:
                    nameOfCity=df2.loc[select]["name"].to_numpy()[0]
                if nameOfCity in arr:
                    arr[nameOfCity]=arr[nameOfCity]+1
                else:
                    arr[nameOfCity]=1
            else:
                searchedTerm=str(sArr[index2][1])
                arr.append(searchedTerm)
            index1+=1
    print(sorted(Counter(arr).items(), key=lambda tup: tup[1])[-20:])
    return arr

def displayNumberOfSearchedTermInACity(nameOfCity,fdate,tdate,time,plotChart):
    global allWords,allWordsWithCities
    allWords2=allWords
    if time:
        allWords2 = extractedFilteredWordsInTime(fdate, tdate)
    fArr = flatteningArr(allWords2);index1=0
    sArr = allWordsWithCities;index2=0
    df2 = pd.read_csv('citiesId.csv',encoding = "utf8")
    select = df2["name"]==nameOfCity
    if len(df2.loc[select]["id"].to_numpy())!=0:
        idOfCity=df2.loc[select]["id"].to_numpy()[0]
    else:
        return "there is no such city!"
    
    arr=[]
    while True:
        if index1==len(fArr) or index2==len(sArr) :
            break
        if sArr[index2][1]!=idOfCity:
            index2+=1
            continue
        elif fArr[index1][0]<sArr[index2][0]:
            index1+=1
        elif fArr[index1][0]>sArr[index2][0]:
            index2+=1
        else:
            searchedTerm=str(fArr[index1][1])
            arr.append(searchedTerm)
            index2+=1
    # print(sorted(Counter(arr).items(), key=lambda tup: tup[1])[-20:])
    answer = Counter(arr).items()
    if plotChart:
        plotTouple(sorted(answer, key=lambda tup: tup[1])[-20:])
    print(answer)
    return answer

def similarWords(word):
    return PredictionWords.similarWords(word)

findSearchedTerm()
fday,fmonth,fyear,tday,tmonth,tyear = 1,1,2019,31,3,2020
fdate=(fday,fmonth,fyear);tdate=(tday,tmonth,tyear)

#                   argumant, fdate and tdate , time filter , other flags
displayNumberOfOccuranceInTime("کاظمیان",fdate,tdate,False,True) # filter time - plot flag
displayNumberOfOccuranceInTime("",fdate,tdate,False,True) # filter time - plot flag
displayNumberOfOccuranceInCities("رزمی",fdate,tdate,False,False)   # alltime/specific - cityId/name of city
displayNumberOfSearchedTermInACity("مشهد",fdate,tdate,True,True)        # filter time - plotChart
similarWords("بچه")
# print(allWordsWithCities)
