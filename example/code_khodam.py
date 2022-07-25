# from urllib.request import urlopen
# url = "http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=46348559193224090"
# page = urlopen(url)

# from tkinter import *
# import tkinter as tk
# import pytse_client as tse
# root = Tk() 
# root2 = Tk() 
# frame = tk.Frame(root)
# frame.pack()
# total_rows=0
# total_column=0
# def write_slogan():
#     print(lst[1][1])

# html_bytes = page.read()
# html = html_bytes.decode("utf-8")

# size_index = html.find("تعداد سهام")

# div_index = html.find("div",size_index)
# div_index2 = html.find("/div",div_index+2)
# print(html[div_index:div_index2])


# import time
# import requests
# from bs4 import BeautifulSoup

# page = requests.get('http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=28450080638096732')
# # time.sleep(2)
# soup = BeautifulSoup(page.text, 'html.parser')

# div = page.text.find("MainContent")
# # soup = bs4.BeautifulSoup(soup)
# # div.find("تعداد سهام")
# print(soup)
    # global total_rows,total_columns
    # lst.append((total_rows,'----','----','----'))
    # total_rows+=1
    # if(total_rows>17):
    #     return ;
    # t = Table(frame,total_rows,total_columns)

# class Table: 
      
#     def __init__(self,frame,total_rows,total_columns): 
          
#         for i in range(total_rows): 
#             for j in range(total_columns): 
#                 if(j==0):
#                     self.e = Entry(frame, width=5, fg='black', font=('Traditional Arabic',14))
#                 else:
#                     self.e = Entry(frame, width=20, fg='black', font=('Traditional Arabic',14))
                  
#                 self.e.grid(row=i, column=j) 
#                 self.e.insert(END, lst[i][j]) 

    

# lst = [
#     [0,'نام سهم','تعداد سهم','حقوق مالکانه'], 
#     # (2,' نام سهم','تعداد سهام' , 'حقوق مالکانه' )
#     [1,'----','----','----'], 
#        [2,'----','----','----'], 
#        [3,'----','----','----'], 
#        [4,'----','----','----'], 
#        [5,'----','----','----'],
#        [6,'----','----','----']] 

# total_rows = len(lst) 
# total_columns = len(lst[0]) 
   
# slogan = tk.Button(root,
#                    text="ok",
#                    command=write_slogan)
# slogan.pack(side=tk.BOTTOM)
# slogan = tk.Button(root,
#                    text="increase row",
#                    command=increase)
# slogan.pack(side=tk.BOTTOM)

# root.geometry("600x400")
# t = Table(frame,total_rows,total_columns) 
# root.mainloop() 
# from Tkinter import *



from tkinter import *
import tkinter as tk
import pytse_client as tse
root = Tk() 
 

def new_table(row):
    root2 = Tk()
    print(row[0].get())
    name = tse.download(symbols=[row[0].get()])
    p_e = row[3].get()
    tedad_sahm = row[1].get()
    hoghugh_malekane = row[2].get()
    gheymat = name.adj_close
    p_e_gp = name.group_p_e_ratio
    value_native=0

    hoghugh_malekane*=10
    value_native = hoghugh_malekane/tedad_sahm 


    rows2 = []
    for i in range(20):
        cols2 = []
        for j in range(4):
            e = Entry(relief=RIDGE)
            e.grid(row=i, column=j, sticky=NSEW)
            e.configure(bg="magenta")
            if i==0:
                if j==0:
                    e.insert(END, 'نام سهم')
                if j==1:
                    e.insert(END, 'ارزش ذاتی')
                if j==2:
                    e.insert(END, 'قیمت')
                if j==3:
                    e.insert(END, 'P/E')
                if j==4:
                    e.insert(END, 'P/E گروه')
                if j==5:
                    e.insert(END, 'نسبت قیمت به ارزش ذاتی')
            else:
                if j==0:
                    e.insert(END, row[0].get())
                if j==1:
                    e.insert(END, value_native)
                if j==2:
                    e.insert(END, gheymat)
                if j==3:
                    e.insert(END, p_e)
                if j==4:
                    e.insert(END,p_e_gp)
                if j==5:
                    e.insert(END, gheymat/value_native)
            cols2.append(e)
        rows2.append(cols)
    root2.mainloop()


def onPress2():
    global cols 
    global rows
    i = len(rows)
    global fetch
    global increase
    for j in range(4):
        e = Entry(relief=RIDGE)
        e.grid(row=i, column=j, sticky=NSEW)
        e.insert(END, '---')
        cols.append(e)
    rows.append(cols)

def onPress():
    for row in rows:
        if row[0].get()=='---':
            return ;
        if row[0].get()=='نام سهم':
            continue;
        new_table(row)

# input()

rows = []
for i in range(20):
    cols = []
    for j in range(4):
        e = Entry(relief=RIDGE)
        e.grid(row=i, column=j, sticky=NSEW)
        if i==0:
            if j==0:
                e.insert(END, 'نام سهم')
            if j==1:
                e.insert(END, 'تعداد سهم')
            if j==2:
                e.insert(END, 'حقوق مالکانه')
            if j==2:
                e.insert(END, 'p/e')
        else:
            e.insert(END, '---' )
        cols.append(e)
    rows.append(cols)

# input()
fetch = Button(text='Fetch', command=onPress).grid()
increase = Button(text='Increase row', command=onPress2).grid()
root.geometry("600x450")
root.mainloop()