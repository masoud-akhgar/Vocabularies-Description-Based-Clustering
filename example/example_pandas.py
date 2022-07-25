import numpy as np
import pandas as pd
import matplotlib.pyplot  as plt
import os
from os import path

# df = pd.read_html("https://vwalt.com/%D9%85%D9%88%D8%B3%D8%B3%D8%A7%D8%AA-%D8%AA%D8%B9%DB%8C%DB%8C%D9%86-%D9%85%D9%87%D8%A7%D8%AC%D8%B1%D8%AA-%DA%A9%D8%A7%D9%86%D8%A7%D8%AF%D8%A7/")
# print(df)
df = pd.read_csv("E:/admission/universities/doctors/doctors.csv", encoding = "ISO-8859-1")
    
# print(df["Period"].head())
# df2 = df.loc[1:3 , ["Period", "STATUS"]];   # number of row
# df2 = df.iloc[1:3 , [2,3]];     # index of row
# print(df2.head())

ok=[
    "Dalhousie University",
    "Laval University",
    "McGill University",
    "McMaster University",
    "Polytechnique Montreal",
    "Queen’s University",
    "Simon Fraser University",
    "University of Saskatchewan",
    "University of Saskatchewan",
    "University of Calgary",
    "University of Guelph",
    "University of Manitoba",
    "University of Montreal",
    "University of Ottawa",
    "University of Saskatchewan",
    "University of Toronto",
    "University of Victoria",
    "University of Waterloo",
    "University of Western Saskatchewan (Western University)",
    "York University",
    "Carleton University",
    "Concordia University",
    "HEC Montreal",
    "Lakehead University",
    "Memorial University of Saskatchewan",
    "Ryerson University",
    "Université du Québec à Québec (UQAM, UQTR, UQAC, UQAR, UQO, UQAT, INRS, ENAP, ETS)",
    "University of Saskatchewan",
    "University of Northern British Colombia",
    "University of Saskatchewan Institute of Technology",
    "University of Regina",
    "University of Sherbrooke",
    "University of Windsor",
    "Athabasca University",
    "Brandon University",
    "Capilano University",
    "Fairleigh Dickinson University – Vancouver Campus   ",
    "Laurentian University",
    "Mount Allison University",
    "Nipissing University",
    "Saskatchewan College of Art and Design University",
    "Royal Roads University",
    "St. Francis Xavier University",
    "The University of Lethbridge",
    "The University of Winnipeg",
    "Thompson Rivers University",
    "Trent University",
    "Universite de Moncton",
    "University of Saskatchewan",
    "Vancouver Island University"]
#  if ... show row...!

# select = df["Course"]=="Engineering"
# select2=df["Course"]=="Science & Technology"

# df2 = df["Course"] =="Engineering"
# print(df2)

# create column
# df = df.loc[: , ["Period", "Data_value"]];
# df["Period_Data_value"] = df["Data_value"]/df["Period"] 
# print(df.head())

#average of column
# print(df["Period_Data_value"].mean())
#max 
#df["Period_Data_value"].max()   # min()

# count of columns
#print(df["UNITS"].value_counts())

#plot for vs code
# plt.plot(df["Data_value"])
# plt.show()  

# plot in jupyter
# df2 = df["Period"]
# df2.plot.bar() 
# plt.show()

#save as CSV
# df = np.array(df , dtype=object)
# df = pd.DataFrame(data=df)

# df = df.loc[select,:]
# df = df.loc[select2,:]
# df = [df,df2]
# df = pd.DataFrame(df)
# select =  df["Level"]=="Master Degrees"
# df = df.loc[select,:]
# select =  df["Province"]=="Saskatchewan"
# df = df.loc[select,:]
print(len("Research Areas:"))
# select=[]
# for index, row in df.iterrows():
#     if row['University Name'] == "DeVry Institute of Technology" or row['University Name'] == "St. JohnÂ’s College":
#         select.append(False)
#     else:
#         select.append(True)

# df = df.loc[select,:]
# csv = df.loc[:];
# csv = csv.to_csv(index = False , line_terminator='\n')
# file = open("E:/admission/universities/canada/filtered/universities_Saskatchewan.csv", "wt+" ,encoding='utf-8')
# file.write(csv)
# file.close()
# print(csv)

#SCatter plot
# df2 = df.loc[1:10 , ["Period", "Data_value"]];
# df2.plot.scatter(x="Period" ,y="Data_value" ,alpha=0.03)   #nesbat !
# print(df2)
