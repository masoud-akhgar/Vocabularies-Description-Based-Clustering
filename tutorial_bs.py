import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import re
from SchoolIdClass import SchoolId
from parsivar import  POSTagger
# from scipy.sparse.csr_matrix import todense

page = requests.get('https://nikaro.ir/school/3')
soup = BeautifulSoup(page.text, 'html.parser')

#                                   TITLE
# print(soup.title.text[-9:])      

# print(page.text)

#                                   FIND IN TEXT
# firstIndex = page.text.find('<meta property="og:description"')
# secondIndex = page.text.find('/>',firstIndex)
# tagText = page.text[firstIndex:secondIndex]

# description = tagText[tagText.find('content="')+9:-1]

# description=description.replace('.', ' ')
# description=description.replace('&amp;',' ')
# description_arr = description.split
# arr_description2 =[]
# for el in description_arr:
#     string = re.sub('[\W_]*', '', el)
#     arr_description2.append(string)
# print(' '.join(arr_description2))


#                                   re.sub
# sss=['تنها', 'اصلی', 'جهانی', 'تخصصی', 'عنوان', 'باشگاه', 'رئیس', 'درجه', 'آقا', 'برگزاری', 'نوجوان', 'وصال', 'حامد', 'مشهد', 'رضا', 'کلاس', 'حضور', 'مدال', 'رضوی', 'دختر', 'محله', 'تیم', 'داور', 'شهر', 'مدیریت', 'پسر', 'رحمتی', 'مسابقات', 'پیشرفته', 'پاشا', 'مصطفی', 'برتر', 'انتصاب', 'مربی', 'آموزگار', 'استان', 'استاد', 'آسیایی', 'نجاتی', 'کمیته', 'راهیابی', 'کارگر', 'سنی', 'خانم', 'انتخاب', 'داوری', 'سرکار', 'خانواده', 'کشور', 'مجید', 'اس', 'هندوستان', 'خراسان', 'کسب', 'سرپرست', 'جوان', 'عضو', 'اعزام', 'هیات', 'المللی', 'نیا', '۶انتخاب', 'ذهن', 'شطرنج', 'رده', 'شرق', 'روسیه', 'اردیبهشت', 'ملی', 'قهرمانی', 'امامت', 'فدراسیون', 'احراز']
# s1=['کارگر', 'کمیته', 'اردیبهشت', 'شهر', 'شرق', 'نجاتی', 'کسب', 'هیات', 'محله', 'رئیس', 'روسیه', 'مجید', 'امامت', 'حضور', 'شطرنج', 'رضا', 'وصال', 'رده', 'انتصاب', 'استان', 'برگزاری', 'خانم', 'احراز', 'مسابقات', 'المللی', 'مصطفی', 'پسر', 'آقا', 'هندوستان', 'قهرمانی', 'مدیریت', 'مربی', 'باشگاه', 'خانواده', 'داور', 'عنوان', 'رحمتی', 'تیم', 'درجه', 'راهیابی', 'عضو', 'فدراسیون', 'استاد', 'سرپرست', 'دختر', 'داوری', 'پاشا', 'حامد', 'نوجوان', 'خراسان', 'رضوی', 'کلاس', 'آموزگار', 'سرکار', 'اعزام', 'کشور', 'ذهن', 'مدال']
# print(len(s1))
# a = ['']
# for i in a:
#     if i == '':
#         print("here")
#     print(len(i))
# newDescArr=[]
# descArr=["اژدهاها"]
# for element in descArr:
#     temp = TokenSplitter().split_token_words(element) # split a complicate word
#     if len(temp)!=0:
#         if (element,) in temp:      # the word has meaning
#             newDescArr.append(element)
#         else:                       # it contains two words in touple
#             temp = temp[0]            # return first word's interpret 
#             newDescArr.append(temp[0])
#             index+=1
#             newDescArr.append(temp[1])
#     else:                         # No detection for the word
#         newDescArr.append(element)

#     index +=1
# print(newDescArr)


#                               remove
# a= ['با', 'مدیریت', 'استاد', 'رضا', 'پاشا', 'نجاتی', 'تنها', 'داور', 'بین', 'المللی', 'و', 'مربی', 'درجه', '۱', 'خراسان', 'بزرگ', 'برگزاری', 'کلاس', 'آموزش', 'شطرنج', 'مقدماتی', 'و', 'پیشرفته', 'زیر', 'نظر', 'داور', 'و', 'مربی', 'در', 'استان', 'خراسان', 'برخی', 'از', 'افتخارات', 'باشگاه', 'ذهن', 'برتر', '۱', 'انتخاب', 'و', 'انتصاب', 'استاد', 'و', 'داور', 'فدراسیون', 'جهانی', 'شطرنج', 'رضا', 'پاشا', 'نجاتی', 'به', 'عنوان', 'تنها', 'عضو', 'خانواده', 'شطرنج', 'شرق', 'کشور', 'به', 'عنوان', 'عضو', 'اصلی', 'یکی', 'از', 'کمیته', 'اصلی', 'و', 'تخصصی', 'فدراسیون', 'شطرنج', 'ایران', 'به', 'عنوان', 'عضو', 'کمیته', 'داور', 'فدراسیون', 'شطرنج', 'ایران', '۲', 'کسب', 'و', 'احراز', 'عنوان', 'داور', 'بین', 'المللی', 'بالاترین', 'عنوان', 'داوری', 'در', 'جهان', 'توسط', 'استاد', 'رضا', 'پاشا', 'نجاتی', '۳', 'انتصاب', 'استاد', 'رضا', 'پاشا', 'نجاتی', 'به', 'عنوان', 'رئیس', 'هیات', 'شطرنج', 'کارگر', 'خراسان', 'رضوی', '۴', 'کسب', 'عنوان', 'اولین', 'آموزگار', 'فدراسیون', 'جهانی', 'شطرنج', 'در', 'خراسان', 'بزرگ', 'توسط', 'استاد', 'مصطفی', 'رحمتی', '۵', 'کسب', 'تنها', 'مدال', 'خراسان', 'بزرگ', 'در', 'مسابقات', 'قهرمانی', 'کشور', '۸', 'تا', '۱۸', 'سال', 'دختر', 'و', 'پسر', 'کشور', 'توسط', 'وصال', 'حامد', 'نیا', 'در', 'رده', 'سنی', 'زیر', '۱۶', 'سال', 'و', 'راهیابی', 'به', 'تیم', 'ملی', 'نوجوان', 'ایران', '۶انتخاب', 'سرکار', 'خانم', 'وصال', 'حامد', 'نیا', 'در', 'تیم', 'ملی', 'نوجوان', 'ایران', 'و', 'اعزام', 'به', 'مسابقات', 'جهانی', 'روسیه', '۷', 'حضور', 'جناب', 'آقا', 'مجید', 'حامد', 'نیا', 'به', 'عنوان', 'سرپرست', 'تیم', 'ملی', 'جوان', 'زیر', '۲۰', 'سال', 'در', 'مسابقات', 'آسیایی', 'هندوستان', '۱۳', 'تا', '۲۲', 'اردیبهشت', '۱۳۹۵', 'باشگاه', 'شطرنج', 'ذهن', 'برتر', 'در', 'شهر', 'مشهد', 'و', 'در', 'محله', 'امامت', 'واقع', 'شده', 'اس']
# firstIndex = page.text.find('id="Tags_TagsContainer__16Pew">')+len('id="Tags_TagsContainer__16Pew">')
# print(firstIndex<len('id="Tags_TagsContainer__16Pew">'))
# secondIndex = page.text.find('<div id="SchoolPage_SecondSection_LeftSide__20L1B"',firstIndex)
# tagText = page.text[firstIndex:secondIndex].replace("</div>","").split('<div class="Tags_Tag__3phPO">')

# print([x for x in tagText if x])   # remove nulls)

# a = ["saنسs"]
# string = re.sub('[a-zA-Z]', '', a[0])
# print(string)
# a = ["هنرهای"]
# for element in a:
#     print(element[-3:]=="های")

# a = list(filter((a[0]).__ne__, a)) # newDescArr.remove all(element)
# print(a)


# ss = ["sadنن","ن"]
# description_arr2 = [w for w in ss if not re.match(r'[A-Z]+', w, re.I)]  # delete english words
# print(description_arr2)
#     file1.write(arr[0]+"|| "+' '.join(cleanDescription(arr[1],0))+"|| "+' '.join(cleanDescription(arr[2],0))+"|| "+
#       ' '.join(cleanDescription(arr[3],0))+"\n")


textt= [
    "آکسفورد مناطق کیفیت انتشار حوزه آموزان ارائه ناشر شروع کتب آفاق بدو یورک آکادمی آغاز زبان شعبه انگلیس سیستم شمس انگلیس زبان انگلیس زبان",
 "استانبول نیمه کمبریج انگلیس سوئدی آلمان گروه مارکی ایتالیا عربی دان شکل زبا ایتالیا دان ترکی خارجه اسپانیا اسپا چینی استانبول آلمان نروژی فرانسه هلند نیول زبان انگلیس فرانسوی سوئدی روسی مارکی عربی ایتالیا دان ترکی خارجه اسپانیا اسپا چینی استانبول آلمان نروژی فرانسه هلند نیول زبان انگلیس فرانسوی سوئدی روسی مارکی عربی",
 "سطح پوشش انگلیس آزمون زنگنه الملل مشاوره زبا فرانسه انگلیس زبان آیلتس فرانسه انگلیس زبان آیلتس",
 "اطمینان سخن 1376 سابقه صحبت تقویت ذکر آموز التحصیل مرور دهنده نکته محدوده تیر سبب استادان همراه اصل اعزام پیشرفتتان جایگاهی فتان سطح مکالمه گرامر آغاز ارگان زبان امری اهدا شهریه اتمام مدرس ویژگی دانش مسیر مترج سخن هزینه ایتالیا ترکی خارجه برتر اسپانیا اسپا تیر آنلاین استانبول آلمان فرانسه نیول زبان انگلیس فرانسوی عربی ترجمه مترجم سخن هزینه ایتالیا ترکی خارجه برتر اسپانیا اسپا تیر آنلاین استانبول آلمان فرانسه نیول زبان انگلیس فرانسوی عربی ترجمه مترجم",
 "سخن کشور سالها نفت سالیان هزینه ایتالیا آموزان التحصیل اشاره زایی مسکن پرداخت غالزایی مستضعفان شرح ادعا واشتغال اعزام ساعت کمکی کارمندان آلمان مترو بنیاد خانه زبان پرسنل اشت شهریه وزارت شهرداری انگلیس طول شرکتها اثباتیست عربی نیرو نهاد مترج استانبول ترکی خارجه انگلیس فرانسوی آلمان اسپانیا فرانسه اسپا ایتالیا نیول عربی زبان استانبول ترکی خارجه انگلیس فرانسوی آلمان اسپانیا فرانسه اسپا ایتالیا نیول عربی زبان",
 "آکسفورد کشور آفرین خدشه سابقه نامه کیفیت کارکنان ماه میهن دهنده مسیر مشتریان استانهای توزیع مدرسین ایزو امنیت گواه پیشگامان سفیر شکایات افتتاح محصول دانشجو تربیت ارائه آنلاین نما اصول فرآیند صنعت منطقه همراه پایبندی کمبریج قلهک رفاه موازات پشتیبان آغاز زبان شعبه گفتمان استاندارد مدیریت سیستم الملل 3 کارشناسان کتاب مشتری دانشگاه هایبرید یندگ انگلیس زبان انگلیس زبان"
]
# vectorizer = TfidfVectorizer()
# X1 = vectorizer.fit_transform(textt)
# for i in range(10, 50, 5):
#     print(i)
print(len(" خوشنویس انجمن خودکار خطاطی"))