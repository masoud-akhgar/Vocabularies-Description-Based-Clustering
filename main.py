import string
from gensim.models import Word2Vec
import pandas as pd
import requests
import mysql.connector
import bisect
from bs4 import BeautifulSoup
from SchoolIdClass import SchoolId
import re
from parsivar import Normalizer, FindStems, POSTagger
from hazm import *
from collections import Counter
import numpy as np
import shutil
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pickle
from scipy import sparse
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import DBSCAN

# WORKING_FILE="resultPage-search_activity.csv"
# WORKING_FILE_USER="resultPage-search_activity_UserOwned.csv"
# SOURCE_FILE="users_tracking_activity_log.csv"
SCHOOL_DESCRIPTION_EXTRACTED="schoolDescriptionExtracted.txt"
SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE="schoolDescriptionExtractedOffline.txt"  # 29916
COURSE_DESCRIPTION_EXTRACTED_OFFLINE="courseDescriptionExtractedOffline.txt"
SCHOOL_SOURCE="schools.csv" #"schools_title_desc_tags.csv"
COURSE_SOURCE="courses.csv" #"schools_title_desc_tags.csv"
REALTIME_BACKUP="backup-realtime.txt"
SPARSE_MATRIX='sparseMatrix.npz'
K_CLUSTER_NUMBERS=65    # 80 - 95 perfect
SCHOOL_MAX_ID=29908
DONEID =3555           # 29917 25670
EnglishWordsFile="EnglishWords.txt"
COURSE_MAX_ID=5918
TAG_COEFFICIENT_COMPARED_TO_DESCRIPTION = 3

# con = mysql.connector.connect(host="https://panel.nikaro.ir/nikaro_pma/index.php", user="admin_view",password="nik@r0@dminView", database="nikaroir_nikaro",auth_plugin='mysql_native_password')  
# cursor=con.cursor()

def getSourceFileFromDB():  # Incompleted
  query = "SELECT ut.id,ut.subject FROM `users_tracking_activity_log` as ut WHERE 1 LIMIT 10;"
  cursor.execute(query)
  table = cursor.fetchall()
  df = pd.DataFrame (table, columns = ['id','subject'])
  print(df)

def saveDf(df, namefile):
  csv = df.loc[:].to_csv(index = False , line_terminator='\n')
  file = open(namefile, "wt+" ,encoding='utf-8')
  file.write(csv)
  file.close()

def removeOtherFields(df,remaining_fields):    
  df = df.filter(items=remaining_fields)
  return df

def updateCsvFiles():
  global cursor
  # getSourceFileFromDB()             # Incompleted
  # makeResultpageAndSearch_Csv()
  makeResultpageAndSearchUserOwned_Csv()

def makeResultpageAndSearchUserOwned_Csv():
  mainDf = pd.read_csv(SOURCE_FILE,encoding = "utf-8")
  mainDf = removeOtherFields(mainDf, ["id", "user_id"])
  select = pd.isna(mainDf.user_id)
  finalDf = mainDf.loc[~select,:]

  saveDf(finalDf, WORKING_FILE_USER)

def makeResultpageAndSearch_Csv():
  global WORKING_FILE,SOURCE_FILE
  mainDf = pd.read_csv(SOURCE_FILE,encoding = "utf-8")
  select = mainDf["subject"]=="resultPage"
  select2 = mainDf["subject"]=="search"
  df = mainDf.loc[select,:]
  df2 = mainDf.loc[select2,:]
  finalDf = pd.concat([df, df2])
  finalDf = removeOtherFields(finalDf, ['id', 'subject','url','parameters'])

  saveDf(finalDf, WORKING_FILE)

def extractTags(text):
  firstIndex = text.find('id="Tags_TagsContainer__16Pew">')+len('id="Tags_TagsContainer__16Pew">')
  if firstIndex<=100:
    return ""
  secondIndex = text.find('<div id="SchoolPage_SecondSection_LeftSide__20L1B"',firstIndex)
  tagText = text[firstIndex:secondIndex].replace("</div>","").split('<div class="Tags_Tag__3phPO">')
  tagText = [x for x in tagText if x]   # remove nulls
  tagText = ' '.join(tagText).split()
  return list(set(tagText))

def cleanDescription(englishwords, content,file):
  global COURSE_DESCRIPTION_EXTRACTED_OFFLINE
  if file==0:
    # delete additional symbols
    description = re.sub(r'[^\w]', ' ', content)
    description=description.replace("&lt;p&gt;",' ');description=description.replace("&lt;/p&gt;",' ')
    description=description.replace('.', ' ');description=description.replace('آ', 'ا')
    description=description.replace('&;;', '');description=description.replace('&', ' ')
    description=description.replace('،', '');description=description.replace("نشستن","")
    description=description.replace(':', '');description=description.replace(':', '')
    description=description.replace(';', '');description=description.replace('&;', ' ')
    description=description.replace('=', ' ');description=description.replace('/', ' ')
    description=description.replace('/&;', ' ');description=description.replace('&;/&;', ' ')
    description=description.replace("&;#۱۰;",' ');description=description.replace("٪",'')
    description=description.replace("+",'');description=description.replace("4D",'')
    description=description.replace("4دی",'');description=description.replace("14",'')
    description=description.replace("_"," ");description=description.replace("3ds","")
    description=description.replace("2016","");description=description.replace("انداختن","")
    description_arr2 = description.split() 
    stemclass = Stemmer()
    description_arr2 = [w for w in description_arr2 if len(w)>1 and w!="NULL"]  # delete english words
    description_arr2 = [w for w in description_arr2 if not re.match(r'[A-Z]+', w, re.I)]  # delete english words
    description_arr2 = [w for w in description_arr2 if not "سال" in w]  # delete contining سال
    description_arr2 = [w for w in description_arr2 if not "تاریخ" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "کد" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "تومان" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "3D" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "in" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "هزار" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "pt" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not "تست" in w]  # delete contining تاریخ
    description_arr2 = [w for w in description_arr2 if not w.isnumeric()]  # delete contining سال
    description_arr3=[]
    for el in description_arr2:
      res = ''.join([i for i in el if not i.isdigit()]) # delete numeric character
      stemclass.stem(res).replace('#', ' ')
      description_arr3.append(res)
    description_arr2 = description_arr3

    # arr_description2 =[]
    # for el in description_arr2:
    #     string = re.sub('[\W_]*', '', el)
    #     string = re.sub('[a-zA-Z]', '', el)
    #     converted = FindStems().convert_to_stem(string)
    #     if not ('&' in converted):
    #       string = converted
    #     arr_description2.append(string)
    arr_description2 = [x for x in description_arr2 if x]   # remove nulls
    return arr_description2
  else:
    flag=False
    if content==COURSE_DESCRIPTION_EXTRACTED_OFFLINE:
      flag=True
    file1 = open(content, "r" ,encoding='utf-8')
    Lines = file1.readlines()
    file1= open(content, "w" ,encoding='utf-8')
    index=0
    for line in Lines:
      index+=1
      
      # if index<DONEID:
      #   continue
      if line.strip()=="":
        continue
      arr = line.split("||") 
      
      if arr[1].strip()=="":
        continue
      # 26054   
      # id, description, title, tags
      if flag:
        file1.write(arr[0]+"|| "+' '.join(cleanDescription(False, arr[1],0))+"|| "+' '.join(cleanDescription(False, arr[2],0))+" ||"+
        ' '.join(cleanDescription(False, arr[3],0))+" ||"+arr[4])
      else:
        file1.write(arr[0]+"||"+' '.join(cleanDescription(False, arr[1],0))+"||"+' '.join(cleanDescription(False, arr[2],0))+"||"+
        ' '.join(cleanDescription(False, arr[3],0))+"\n")

    file1.close()
  return 

def splitDescriptionWords(content,fileinput,flag2): # RECEIVE ARRAY OR FILE => splitted word
  global allWords
  arrExpected = ["ها","های","سار","سان","کار","گر","وار","واره","وند","وار","ور","ی","ات","یی","یان"]
  wordExpected = ["عمران","انسان","گواهینامه","کارگردان","آرایشگری","آرایشگر","کوهنوردی","پژوهشسرا","پژوهشسر","ارایشگری","ارایشگر","فیلم","فیلمنامه","بازیگردان","کارگردان","بندرعباس","کرمانشاه","سوارکاری","سوارکار","مایکروسافت","ژیمناستیک"]
  compoundExpected=[("هنرهای","هنر"),("روشهای","روش"),("هنرجویان","هنرجو"),("کودکان","کودک"),("هنری","هنر"),("مربیان","مربی"),("اموزشهای","اموزش"),("رزش","ورزش"),("کشورهای","کشور"),("استا","استاد"),("کارگردانی","کارگردان"),("خوراکهای","خوراک"),("نوشیدنیهای","نوشیدنی"),("یشگری","ارایشگری"),("ارا",""),("ینامه",""),("سنامه","اساسنامه"),("نشناسان","روانشناس"),
  ("یشگاه","ازمایشگاه نمایشگاه"),("اموز",""),("ورز","ورزش"),("رزش","ورزش"),("رستان",""),("کلاسفیلفیلمنامه","کلاس فیلم فیلمنامه"),('کلاسها',"کلاس"),("ژیمن","ژیمناستیک"),("استیک","")]
  newContent=[]
  stopWords = SchoolId.getStopWords()
  if fileinput==0:
    flag=False
    for element in content:
      #alternative
      if flag2:
        if len(element)<=4:
          newContent.append(element)
          continue
        if element=="سبکهای":
          element="سبک"
        if element=="اسلایدها":
          element="اسلاید"
        # split not inserted space
        if len(element)>=8:
          for j in range(3,len(element)-3):
            if (element[:j] in allWords or element[:j] in stopWords) and (element[j:] in allWords or element[j:] in stopWords):
              newContent.append(element[:j])
              newContent.append(element[j:])
              flag=True
              break
          if not flag:
            newContent.append(element)
        else:
          newContent.append(element)

      # # split symbols and word
      else:     # flag2=false
        if element in wordExpected:
          newContent.append(element)
          continue

        if element == wordExpected:
          newContent.append(element)
          continue

        if "کوه" in element:
          newContent.append(element)
          continue
        
        if "یتها" == element:
          continue

        for j in arrExpected:
          if j == element[-1*len(j):]:
            if element[:-1*len(j)] in allWords:
              newContent.append(element[:-1*len(j)])
              flag=True
              break
        if not flag:
          for j in compoundExpected:
            if j[0]==element:
              newContent.append(j[1])
              flag=True
          if not flag:
            newContent.append(element)

    return newContent
  else:
    flag3=False
    if content==COURSE_DESCRIPTION_EXTRACTED_OFFLINE:
      flag3=True
    file1 = open(content, "r" ,encoding='utf-8') #
    Lines = file1.readlines()
    file1= open(content, "w" ,encoding='utf-8')
    index=0
    print(content)
    for line in Lines:
      index+=1
      # print("jeree")

      line = line.replace('\n' , '')
      arr = line.split("||")
      # if int(arr[0])<DONEID:
      if flag3:
        # print(arr[0])
        # print(arr[1])
        # print(arr[2]+"here")
        # print(arr[3])
        # return
        file1.write(arr[0]+"||"+' '.join(splitDescriptionWords(arr[1].split(),0,flag2))+"||"+' '.join(splitDescriptionWords(arr[2].split(),0,flag2))+"||"+
        ' '.join(splitDescriptionWords(arr[3].split(),0,flag2))+"||"+arr[4]+"\n")
      else:
        file1.write(arr[0]+"||"+' '.join(splitDescriptionWords(arr[1].split(),0,flag2))+"||"+' '.join(splitDescriptionWords(arr[2].split(),0,flag2))+"||"+
        ' '.join(splitDescriptionWords(arr[3].split(),0,flag2))+"\n")
    file1.close()
  return 

def clearStopWordsOccurance(content, file):
  global COURSE_DESCRIPTION_EXTRACTED_OFFLINE
  stopWords = SchoolId.getStopWords()
  if file==0:
    content2=content
    for element in content:
      if element in stopWords:
        content2 = list(filter((element.strip()).__ne__, content2)) # finalDescArr.remove all(element)
    return content2
  else:
    flag=False
    if content==COURSE_DESCRIPTION_EXTRACTED_OFFLINE:
      flag=True
    file1 = open(content, "r" ,encoding='utf-8')
    Lines = file1.readlines()
    file1= open(content, "w" ,encoding='utf-8')
    index=0

    for line in Lines:
      index+=1
      arr = line.split("||")
      # if int(arr[0])<DONEID:  1774
      #   continue
      if line.strip()=="":
        continue

      if flag:
        file1.write(arr[0]+"||"+' '.join(clearStopWordsOccurance(arr[1].split(),0))+"||"+' '.join(clearStopWordsOccurance(arr[2].split(),0))+"||"+
        ' '.join(clearStopWordsOccurance(arr[3].split(),0))+"||"+arr[4])
      else:
        file1.write(arr[0]+"||"+' '.join(clearStopWordsOccurance(arr[1].split(),0))+"||"+' '.join(clearStopWordsOccurance(arr[2].split(),0))+"||"+
        ' '.join(clearStopWordsOccurance(arr[3].split(),0))+"\n")
    file1.close()
  return 

def clearUndesiredRoles(content,filei):
  Undesirable = SchoolId.getUndesirableRoles()
  if filei==0:
    postTaggerObj = POSTagger(model='resources/postagger.model')
    content = postTaggerObj.tag(content)
    arr=[]
    for element in content:
      if "V"==element[1] or "P"==element[1] or "POSTP"==element[1] or "DET"==element[1] or "CONJ"==element[1] or "NUMe"==element[1] or "NUM"==element[1] or "AJ"==element[1] or "AJe"==element[1]:
        continue
      else:
        arr.append(element[0])
    return arr
  else:
    file1 = open("FirstBackupCourse.txt", "r" ,encoding='utf-8')
    Lines = file1.readlines()
    file1= open(content, "a" ,encoding='utf-8')
    index=0
    print("here00")
    for line in Lines:
      index+=1
      print(index)
      if index<=3985:
        continue
      arr = line.split("||")
      
      if line.strip()=="":
        continue
      # print((arr[0]+"||"+' '.join(clearStopWordsOccurance(arr[1].split(),0))+"||"+' '.join(clearStopWordsOccurance(arr[2].split(),0))+"||"+
      # ' '.join(clearStopWordsOccurance(arr[3].split(),0))+"\n"))
      file1.write(arr[0]+"||"+' '.join(clearUndesiredRoles(arr[1].split(),0))+"||"+' '.join(clearUndesiredRoles(arr[2].split(),0))+"||"+
      ' '.join(clearUndesiredRoles(arr[3].split(),0))+"|| "+arr[4])
      # elif larr==3:
      #   file1.write(arr[0]+"||"+' '.join(clearUndesiredRoles(arr[1].split(),0))+"||"+' '.join(clearUndesiredRoles(arr[2].split(),0))+"||"+" || \n")
      # elif larr==2:
      #   file1.write(arr[0]+"||"+' '.join(clearUndesiredRoles(arr[1].split(),0))+"|| "+"||"+" \n")
    
    file1.close()

def UndesiredRolesFile(finalDescArr):
  global SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE
  file1= open("undesirableRoles.txt", "w" ,encoding='utf-8')
  file2 = open(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, "r" ,encoding='utf-8')
  Lines = file2.readlines()
  postTaggerObj = POSTagger(model='resources/postagger.model')
  index=0

  for line in Lines:
    index+=1
    # print(index)
    arr = line.split("||")
    if len(arr)==0 or len(arr)==1:
      continue
    descArrRole1 = postTaggerObj.tag(arr[1].split())      # role determination
    descArrRole2 = postTaggerObj.tag(arr[2].split())      # role determination
    descArrRole3 = postTaggerObj.tag(arr[3].split())      # role determination
    descArrRole = descArrRole1+descArrRole2+descArrRole3
    # descArrRole = np.array(descArrRole).flatten()
    for element in descArrRole:
      if len(element)==0:
        continue
      if "V"==element[1] or "P"==element[1] or "POSTP"==element[1] or "DET"==element[1] or "CONJ"==element[1] or "NUMe"==element[1] or "NUM"==element[1] or "AJ"==element[1] or "AJe"==element[1]:
        file1.write(element[0]+" \n")
      else:
        continue
  file1.close()
  return 

def extractDescriptionTagTitle(content):
  CLEANR = re.compile('<.*?>')
  df = pd.read_csv(content,encoding = "utf8")
  desc = df["desciption"];title = df["title"];tag = df["tags"];dfid=df["id"]
  flag=False
  if content==COURSE_SOURCE:
    flag=True
  if flag:
    category=df["category_id"]
  index=-1
  arr=[]
  for line in range(len(title)-1):
    index+=1
    if dfid[index]<=DONEID:
      continue
    row=[]
    try:
      filteredTitle = re.sub(CLEANR, '', title[index])
    except:
      filteredTitle="NULL"
    try:
      filteredDesc = re.sub(CLEANR, '', desc[index])
    except:
      filteredDesc="NULL"
    try:
      filteredTag = re.sub(CLEANR, '', tag[index])
    except:
      filteredTag =""
    if flag:
      filteredCategory = category[index]
    row.append(dfid[index])
    row.append(filteredTitle) 
    row.append(filteredDesc) 
    row.append(filteredTag.split('-'))
    if flag:
      row.append(filteredCategory)
    arr.append(row)
    # if dfid[index]==29918:  # END OF FILE
    #   return arr
    # if index==16396:
    #   print(row)
    #   print(arr[16395])
    #   return
  return arr

def extractContentCoursePagesIntoFileOffline():
  global COURSE_DESCRIPTION_EXTRACTED_OFFLINE,COURSE_SOURCE
  file = open(COURSE_DESCRIPTION_EXTRACTED_OFFLINE, "w" ,encoding='utf-8')
  arr = extractDescriptionTagTitle(COURSE_SOURCE) # offline
  Ids = [row[0] for row in arr]
  title = [row[1].replace("آموزشگاه","") for row in arr]
  desc = [row[2] for row in arr]
  tagsArr = [row[3] for row in arr]
  categoryArr = [row[4] for row in arr]
  for index in range(0,len(desc)):
    desc[index] = desc[index].replace('\n','')
    title[index] = title[index].replace('\n','')
    # descArr = clearStopWordsOccurance(descArr,0)
    finalDescArr = desc[index].split()# UndesiredRolesFile(desc[index].split())
    filteredTitle = title[index].split() #clearStopWordsOccurance(title[index].split(),0)
    filteredtagsArr = tagsArr[index] #clearStopWordsOccurance(tagsArr[index],0)

    lineforwrite=str(Ids[index])+"||"+' '.join(filteredTitle)+"||"+' '.join(finalDescArr)+"||"+' '.join(filteredtagsArr)+"|| "+str(categoryArr[index])
    file.write(lineforwrite.replace('\n','')+'\n')

  file.close()

def extractContentSchoolPagesIntoFileOffline():
  global SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE,SCHOOL_SOURCE
  file = open(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, "w" ,encoding='utf-8')
  arr = extractDescriptionTagTitle(SCHOOL_SOURCE) # offline
  Ids = [row[0] for row in arr]
  title = [row[1].replace("آموزشگاه","") for row in arr]
  desc = [row[2] for row in arr]
  tagsArr = [row[3] for row in arr]
  for index in range(0,len(desc)):
    print(Ids[index])
    desc[index] = desc[index].replace('\n','')
    title[index] = title[index].replace('\n','')
    # descArr = cleanDescription(False, desc[index],0)
    # descArr = clearStopWordsOccurance(descArr,0)
    finalDescArr = desc[index].split()# UndesiredRolesFile(desc[index].split())
    filteredTitle = title[index].split() #clearStopWordsOccurance(title[index].split(),0)
    filteredtagsArr = tagsArr[index] #clearStopWordsOccurance(tagsArr[index],0)

    file.write(str(Ids[index])+"||"+' '.join(filteredTitle)+"||"+' '.join(finalDescArr)+"||"+' '.join(filteredtagsArr)+"\n")

  file.close()
  # clearStopWordsOccurance(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE,1)
  # cleanDescription(False, SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE,1)
  return

def extractDescription(text):
  # text.find('<p><p class="SchoolSpecs_Description__2lWCi">')+len('<p><p class="SchoolSpecs_Description__2lWCi">')
  firstIndex = text.find('<meta property="og:description"')
  secondIndex = text.find('/>',firstIndex)
  tagText = text[firstIndex:secondIndex]
  return tagText[tagText.find('content="')+9:-1]

def extractContentSchoolPagesIntoFile():  # using Website & CSV
  global SCHOOL_DESCRIPTION_EXTRACTED
  arr=SchoolId.getArr()    # return array containing IDs existing  ( time consuming... )
  url_school="https://nikaro.ir/school/"
  file = open(SCHOOL_DESCRIPTION_EXTRACTED, "a" ,encoding='utf-8')
  for x in range(842,1800):
    print(url_school+str(x))
    index = bisect.bisect_left(arr, x)
    if index != len(arr) and arr[index]==x:
      page = requests.get(url_school+str(x))
      soup = BeautifulSoup(page.text, 'html.parser')
      if soup.title==None:
        continue # almost it does not come here

      desc = extractDescription(page.text) # online
      descArr = cleanDescription(False, desc,0)
      finalDescArr = clearStopWordsOccurance(descArr, 0)
      title = clearStopWordsOccurance(soup.title.text.replace("آموزشگاه","").split(),0)
      tagsArr = extractTags(page.text)
      tagsArr = clearStopWordsOccurance(tagsArr,0)

      # id, description, title, tags
      file.write(str(x)+"||"+' '.join(title)+"||"+' '.join(finalDescArr)+"||"+' '.join(tagsArr)+"\n")

  file.close()

def findInSortedArr(arr,x):
  arr = SchoolId.getArr()
  ans_arr = []
  for x in range(1,SCHOOL_MAX_ID):
    index = bisect.bisect_left(arr, x)
    if index != len(arr) and arr[index]!=x:
      ans_arr.append(x)
  return ans_arr

def makeUnikStopWords(content):
  wordSet={''}
  file1 = open(content, 'r') # orginal deleted!...
  Lines = file1.readlines()
  for line in Lines:
    wordSet.add(line.strip())
  
  file2 = open(content, 'w')
  for line in wordSet:
    file2.write(str(line)+'\n')
  file2.close()

def deleteEmptyLines(content):
  global COURSE_SOURCE
  file1 = open(content, "r" ,encoding='utf-8')
  Lines = file1.readlines()
  file1 = open(content, "w" ,encoding='utf-8')
  index=0
  for index in range(len(Lines)-1):
    index+=1
    # if index<DONEID:
    #   continue
    line = Lines[index]
    arr = line.split("||")
    if line.strip()=="" or len(arr)<=2:
      continue
    if content==COURSE_SOURCE and len(arr)<=3:
      continue
    if arr[2].strip()=="":
      continue

    if index!=len(Lines)-1:
      line2 = Lines[index+1]
      arr2 = line2.split("||")
      if len(line2)!=0 and (not arr2[0].isnumeric() or int(arr2[0])<int(arr[0])):
        line = line+line2
        line = line.replace('\n','')
        line+='\n'
        index+=1
    file1.write(line)
  file1.close()

def countExtractedWords(content):
  file1 = open(content, "r" ,encoding='utf-8')
  Lines = file1.readlines()
  arrWords=[]
  arr=[]
  index=0
  for i in range(len(Lines)-1):
    index+=1
    
    arr = Lines[i].split("||")
    if len(arr)==4:
      arrWords+=arr[1].split() + arr[2].split() + arr[3].split()
    elif len(arr)<=2:
      continue
    else:
      arrWords+=arr[1].split() + arr[2].split() #+ arr[3].split()

  # print(sorted(Counter(arrWords).items(), key=lambda tup: tup[1]))
  return sorted(Counter(arrWords).items(), key=lambda tup: tup[1])

def okBug():
  global SCHOOL_DESCRIPTION_EXTRACTED,SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE
  file1 = open(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, "r" ,encoding='utf-8')
  Lines = file1.readlines()
  file1 = open(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, "a" ,encoding='utf-8')
  index=0
  arr=[]
  for line in Lines:
    index+=1
    arr = line.split("||")
    if index>DONEID:
      if len(arr)<=1:
        continue
      for j in range(len(arr[1])):
        if len(arr[1])<=j:
          break
        if ord(arr[1][j])==32 and ord(arr[1][j-1])!=32 and ord(arr[1][j+1])!=32:
          arr[1]=arr[1][:j]+arr[1][j+1:]
    else:
      continue
  
    file1.write(arr[0]+"||"+arr[1]+"||"+arr[2]+"||"+arr[3]+"")
  file1.close()

def getDescAndTag():
  file1 = open(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, "r" ,encoding='utf-8')
  Lines = file1.readlines()
  corpus=[]
  for i in range(len(Lines)-1):
    arr = Lines[i].split("||")
    if len(arr)==4:
      corpus.append(arr[2] +" "+ TAG_COEFFICIENT_COMPARED_TO_DESCRIPTION * (arr[3][:-1]+" "))
    else:
      corpus.append(arr[2] +" "+ TAG_COEFFICIENT_COMPARED_TO_DESCRIPTION * (arr[3][:-1]+" "))
  return corpus

def sparseMatrixProvider(vectorizer):
  global SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE,SPARSE_MATRIX,allWords
  corpus = getDescAndTag()                    # corpus = string used for train
  X1 = vectorizer.fit_transform(corpus)       # convert string for each document to word counts
  # print(corpus[0],X1.toarray())
  return X1

def addEnglishWordsToFile(content):
  global EnglishWordsFile
  shutil.copyfile("EnglishWordsBackup.txt", "EnglishWords.txt")  #completed before added eng words
  file1 = open(content, "r" ,encoding='utf-8')
  Lines = file1.readlines()
  file2 = open(EnglishWordsFile, "r" ,encoding='utf-8')
  LinesSource = file2.readlines()
  file3 = open(content, "w" ,encoding='utf-8')
  beginindex=0;flag=0
  for index in range(len(LinesSource)-1):
    arr2 = LinesSource[index].split("||")
    for jindex in range(beginindex,len(Lines)-1):
      arr = Lines[jindex].split("||")
      if int(arr[0])==int(arr2[0]):
        if int(arr[0])>29000:
          flag=True
        if int(arr[0])<29000 and flag:
          return
        file3.write(arr[0]+"||"+arr[1]+"||"+arr[2]+arr2[1][:-1]+"||"+arr[3])
        beginindex = jindex+1
        if beginindex>=len(Lines)-2:
          return
        break
      else:
        if int(arr[0])>29000:
          flag=True
        if int(arr[0])<29000 and flag:
          return
        file3.write(arr[0]+"||"+arr[1]+"||"+arr[2]+"||"+arr[3])
  # print(index)
  file3.close()

def createPureEnglishWords(content):
  global EnglishWordsFile
  # file1 = open(EnglishWordsFile, "w" ,encoding='utf-8')
  # if content==SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE:
  #   source = SCHOOL_SOURCE
  # else:
  #   source = COURSE_SOURCE
  # arr = extractDescriptionTagTitle(source)  
  # idcol = [row[0] for row in arr]
  # desc = [row[2] for row in arr]

  # for index in range(0,len(desc)):
  #   el = desc[index]
  #   el = cleanDescription(True, el,0)         # just one time 
  #   arr2 = [w for w in el if re.match(r'[A-Z]+', w, re.I) and len(w)>2 and w!="NULL"]  # delete english words
  #   if len(arr2)!=0:
  #     file1.write(str(idcol[index])+" || "+ ' '.join(arr2)+"\n")
  # file1.close()

def printKmeans(kmeans,vectorizer,sortedarr):
  order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
  terms = vectorizer.get_feature_names()
  num=0
  for i in range(K_CLUSTER_NUMBERS):
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
      print(' %s' % terms[ind])

def returnPrediction(article,vectorizer,kmeans,order_centroids,terms):
  arr=[]
  Y = vectorizer.transform([article])
  prediction = kmeans.predict(Y)
  i = prediction[0]
  print("Prediction 1 - Cluster %d:" % i),
  for ind in order_centroids[i, :20]:
    print(' %s' % terms[ind])
    arr.append(terms[ind])
  return arr

def show_recommendations(kmeans, product,vectorizer,sortedarr):
  order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
  terms = vectorizer.get_feature_names()

  corpus = getDescAndTag()
  for article in corpus:
    if product in article.split():
      return returnPrediction(article,vectorizer,kmeans,order_centroids,terms)
      
  cases = possibleSplitedWords([product])
  cases.append(product)
  if "ا" in product:
    cases.append(product.replace("ا","آ"))
  if "آ" in product:
    cases.append(product.replace("آ","ا"))
  for article in corpus:
    for case in cases:
      if case==article:
        return returnPrediction(article,vectorizer,kmeans,order_centroids,terms)
  
  return returnPrediction(product,vectorizer,kmeans,order_centroids,terms)


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

def loadAll():
  X1 = sparse.load_npz(SPARSE_MATRIX)           # load sparse matrix from file
  vectorizer = pickle.load(open("vectorizer.pk", "rb")) # load vectorizer
  kmeans = pickle.load(open("kmeans.pkl", "rb")) # load model
  return (X1,vectorizer,kmeans)

def addCourseDesToSchoolDes():
  global COURSE_DESCRIPTION_EXTRACTED_OFFLINE,SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE
  file1 = open(COURSE_DESCRIPTION_EXTRACTED_OFFLINE, "r" ,encoding='utf-8')
  Lines = file1.readlines()
  file2= open(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, "a" ,encoding='utf-8')
  for line in Lines:
    arr = line.split("||")
    file2.write(str(29916+int(arr[0]))+"||"+arr[1]+"||"+arr[2]+"||"+arr[3]+"\n")
  file2.close()

allWords = countExtractedWords(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE)
def mainProcess():
  c=COURSE_DESCRIPTION_EXTRACTED_OFFLINE
  s=SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE
  content=s
  #                                             # EXTRACTING...
  # makeUnikStopWords('Stop_Words2.txt')
  # extractContentSchoolPagesIntoFile()         # Online using web
  # extractContentSchoolPagesIntoFileOffline()

  # extractContentCoursePagesIntoFileOffline()  # course4226

  #                                             # PREPROCESSING...
  # deleteEmptyLines(content)
  # cleanDescription(False, content,1)# s,1)  
  # splitDescriptionWords(content,1,True)# s,1,allWords)   # needs allwords + has 2 modes
  # splitDescriptionWords(content,1,False)# s,1,allWords)   # needs allwords + has 2 modes
  # clearStopWordsOccurance(content,1)  
  # cleanDescription(False, content,1)# s,1)  
  # deleteEmptyLines(content)

  # UndesiredRolesFile(s)
  # addCourseDesToSchoolDes()
  # clearUndesiredRoles(content,1)              # unneccessary
  # createPureEnglishWords(s)                    # and add them to file ( there is no need to it now)
  # addEnglishWordsToFile(s)                      # is not always correct


  #                                             K - M E A N S
  # # # #                                             # FEATURE EXTRACTING...
  # vectorizer = TfidfVectorizer() 
  # X1 = sparseMatrixProvider(vectorizer)
  # kmeans = KMeans(n_clusters = K_CLUSTER_NUMBERS, init = 'k-means++')
  # kmeans.fit(X1)
  # # # # #                                               PREDICTION

  

  # # #                                              # SAVE AND LOAD MODEL
  # pickle.dump(kmeans, open("kmeans.pkl", "wb")) # save model to file
  # sparse.save_npz(SPARSE_MATRIX, X1)          # save sparse matrix to file
  # with open('vectorizer.pk', 'wb') as fin:    # save vectorize
  #   pickle.dump(vectorizer, fin)

  # X1,vectorizer,kmeans = loadAll()
  # show_recommendations(kmeans,"فوتبال",vectorizer,allWords)

  # printKmeans(kmeans,vectorizer,allWords)

  #                                                      # TEST
  # categorize saved vectorize and model...
  # categorize()
  
  # # sample = vectorizer.fit_transform("جسم")

# okBug()
# extractDescriptionTagTitle()
# splitDescriptionWords(descArr)

# mainProcess()
# x_axis.append(kmeans.inertia_)
# y_axis.append(j)
# print(x_axis[0])
# y_kmeans = kmeans.fit_predict(X)

# shutil.copyfile(SCHOOL_DESCRIPTION_EXTRACTED_OFFLINE, REALTIME_BACKUP)  #completed before added eng words

class PredictionWords:
  def similarWords(string):
      X1,vectorizer,kmeans = loadAll()
      show_recommendations(kmeans,string,vectorizer,allWords)