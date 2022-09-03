from concurrent.futures import thread
from curses import KEY_ENTER
from curses.ascii import NUL
from lib2to3.pgen2 import driver
from multiprocessing.connection import wait
from time import sleep
from traceback import print_tb
import pandas as pd
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from telnetlib import EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



def loginInfo():
    with open('logininfo.txt','r') as f:
        content = f.readlines()
    
    email = content[0][:-1]
    mdp = content[1]
    return email,mdp

def logintoLinkedIn(user,mdp):
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.linkedin.com/login")
    usernameBar = driver.find_element("id","username")
    usernameBar.send_keys(user)
    passwordBar = driver.find_element("id","password")
    passwordBar.send_keys(mdp)
    btn = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
    btn.click()
    return driver

def searchlinkedIn(driver : webdriver.Chrome ,jobname : str ,location:str):
        numberofspace= jobname.count(" ")
        convertedStringjobname=jobname.replace(" ","%20",numberofspace)
        numberofspace= location.count(" ")
        convertedStringLocation = location.replace(" ","%20",numberofspace)
        url = f"https://www.linkedin.com/jobs/search/?&f_TPR=r86400&keywords={ convertedStringjobname }&location={ convertedStringLocation }"
        driver.get(url)
        return driver

def parseInt(mot):
    res=""
    for i in mot:
        if i.isnumeric():
            res+=str(i)
    nDaysAgo=int(res)
    daysAgo = date.today()- timedelta(days=nDaysAgo)
    daysAgo.strftime("%Y-%m-%d") 
    return daysAgo

def IndeedAPI(jobname,location,pagenumber):
    new_columns = ['url','name','title','location','date','sommaire']
    url = "https://indeed11.p.rapidapi.com/"
    payload = {
	"search_terms": f"{jobname}",
	"location": f"{location}",
	"page": f"{pagenumber}"
    }
    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "47cbf29e03msh0d57edfd800941cp163b5cjsnecd652ff3d97",
	"X-RapidAPI-Host": "indeed11.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    tableau=pd.read_csv('data2.csv')
    dataframe = tableau[['url','company_name','job_title','location','date','summary']].copy()
    dataframe.columns = new_columns
    dataframe['date']=dataframe['date'].apply(parseInt)
    return dataframe

if __name__=='__main__':
    user,mdp = loginInfo()
    driver = logintoLinkedIn(user,mdp)
    driver = searchlinkedIn(driver,"data Analyst",'Paris')
    sleep(1)
    source = BeautifulSoup(driver.page_source,'html.parser')
    with open("test.html","w") as wf:
        wf.write(source.prettify())
    tags =source.find_all(class_="jobs-search-results__list-item")
    #print(source.prettify())
    for tag in tags:
        try:
            print(tag.find_all(class_="artdeco-entity-lockup__title")[0].a.string)
        except:
            continue
        print()
    #driver.close()



"""


def ScrappinginfoLinkedIn(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html5lib')
    description=[]
    soup.prettify()
    table = soup.find('div', attrs = {'class':'show-more-less-html__markup show-more-less-html__markup--clamp-after-5'}) 
    return table

conn = http.client.HTTPSConnection("linkedin-jobs-search.p.rapidapi.com")

payload = "{\n    \"search_terms\": \"data engineer\",\n    \"location\": \"75\",\n    \"page\": \"1\"\n}"
headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "47cbf29e03msh0d57edfd800941cp163b5cjsnecd652ff3d97",
    'X-RapidAPI-Host': "linkedin-jobs-search.p.rapidapi.com"
    }
conn.request("POST", "/", payload, headers)
res = conn.getresponse()
data = res.read()
decodedData = data.decode("utf-8")
tableau=pd.read_csv('data.csv')
dataframe1 = tableau[['linkedin_job_url_cleaned','normalized_company_name','job_title','job_location','posted_date']].copy()
dataframe1['summary']=dataframe1['linkedin_job_url_cleaned'].apply(ScrappinginfoLinkedIn)
dataframe1.columns = new_columns
#print(dataframe1)

#print(dataframe2)
combined = pd.concat([dataframe1, dataframe2], ignore_index=True)
#print(combined['url'][0])
print(combined[['url']]) 

"""