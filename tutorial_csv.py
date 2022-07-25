# to see csv use : https://www.convertcsv.com/csv-viewer-editor.htm
# to see documentation: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
#                               PANDAS
import pandas as pd
import bisect
import re
#                               SELECT A COLUMN
# df = pd.read_csv("temp.csv",encoding = "utf8")
# select = df["subject"]=="search"
# print(df)   # or df["subject"](.head()) for example


#                               CREATE COLUMN
# df = df.loc[: , ["Period", "Data_value"]];
# df["Period_Data_value"] = df["Data_value"]/df["Period"] 
# print(df.head())

#                               FILTER COLUMNS
# df = pd.read_csv("temp.csv",encoding = "utf8")
# print(df.filter(items=['id', 'subject']))

#                               FITER ROWS
# df = pd.read_csv("temp.csv",encoding = "utf8")
# select = df.user_id=="NaN"
# print(type(df.user_id[0]))
# print(df.user_id[0])
# print(isinstance(df.user_id[0],type(None)))
# print(df.loc[select,:])

# OR: print(df.loc[:]['subject'])


#                               CONCAT  
# finalDf = pd.concat([df,df2])


#                               STATISTICS
# df = pd.read_csv("temp.csv",encoding = "utf8")
# print(df.url)
# print(pd.isna(df.user_id))


#                               Delete Tags
# CLEANR = re.compile('<.*?>')  
# title = df["title"]

# arr=[1,2,[1,2,3]]
# print(arr[:][2])
SCHOOL_DESCRIPTION_SOURCE="schools_title_desc_tags.csv"

# print('مدرسه دانشمند کوچولو'=="مدرسه دانشمند کوچولو")
# df = pd.read_csv(SCHOOL_DESCRIPTION_SOURCE,encoding = "utf8")
# title = df["title"]
# print(title[1])
aa=list(range(1,48,1))
print(aa)