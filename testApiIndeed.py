import http.client
import sys
import json
import pandas as pd
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup


def parseInt(mot):
    res=""
    for i in mot:
        if i.isnumeric():
            res+=str(i)
    nDaysAgo=int(res)
    daysAgo = date.today()- timedelta(days=nDaysAgo)
    daysAgo.strftime("%Y-%m-%d") 
    return daysAgo

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
new_columns = ['url','name','title','location','date','sommaire']
dataframe1.columns = new_columns
#print(dataframe1)
url = "https://indeed11.p.rapidapi.com/"
payload = {
	"search_terms": "data engineer",
	"location": "Paris",
	"page": "1"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "47cbf29e03msh0d57edfd800941cp163b5cjsnecd652ff3d97",
	"X-RapidAPI-Host": "indeed11.p.rapidapi.com"
}
response = requests.request("POST", url, json=payload, headers=headers)
tableau2=pd.read_csv('data2.csv')
dataframe2 = tableau2[['url','company_name','job_title','location','date','summary']].copy()
dataframe2.columns = new_columns
dataframe2['date']=dataframe2['date'].apply(parseInt)
#print(dataframe2)
combined = pd.concat([dataframe1, dataframe2], ignore_index=True)
#print(combined['url'][0])
print(combined)

