import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
class share_stock:
    txt=""
    def __init__(self):
        page = requests.get('http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=28450080638096732')
        txt = page.text
        status = page.status_code
        soup = BeautifulSoup(page.content , 'html.parser')
        title = soup.title.text

    def get_gp(self):
        i=0
        for line in txt.split('\n'):
            i+=1
            if line.find('LSecVal')!=-1:
                break
        first = line.find("'" , line.find('LSecVal'));
        second = line.find("'" , first+1);
        sub = line[first+1:second]
    
    def get_related_company(self):
        i=0
        for line in txt.split('\n'):
            i+=1
            if line.find('RelatedCompanies')!=-1:
                break

        RelatedCompanies=[]

        first = line.find("'" , line.find('RelatedCompanies'));
        while first!=-1:
            second = line.find("'" , first+1);
            sub = line[first+1:second]
            if sub[0]>='0' or sub[0]<='9':
                first = line.find("'" , second+1);
                second = line.find("'" , first+1);
                sub = line[first+1:second]
            RelatedCompanies.append(sub)
            first = line.find("]" , second);
            first = line.find("'" , first);

        print(RelatedCompanies)
        
# page = requests.get('http://www.tsetmc.com/Loader.aspx?ParTree=151311&i=28450080638096732')
# txt = page.text
# soup = BeautifulSoup(page.content , 'html.parser')
# # print(page.text)
# # i=0
# # for line in txt.split('\n'):
# #     i+=1
# #     if line.find('Section_relco')!=-1:
# #         break

# while page.text.find("divSupervision")==-1:
#     soup = BeautifulSoup(page.content , 'html.parser')

# print("yes")



# page = requests.get('https://codal.ir/ReportList.aspx?search&Symbol=ثپردیس')
# txt = page.text
# status = page.status_code
# soup = BeautifulSoup(page.content , 'html.parser')
# title = soup.title.text 
# print(txt.find("گزارش فعالیت"))

# Instantiate an Options object
# and add the “ — headless” argument


browser = webdriver.Firefox()
browser.get('http://http://www.tsetmc.com')


# opts = Options()
# opts.add_argument(" — headless")# If necessary set the path to you browser’s location
# opts.binary_location= os.getcwd() +'\\GoogleChromePortable\GoogleChromePortable.exe'# Set the location of the webdriver
# chrome_driver = os.getcwd() +'\\chromedriver.exe”# Instantiate a webdriver'
# driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)# Load the HTML page
# driver.get(os.getcwd() +'\\test.html')
