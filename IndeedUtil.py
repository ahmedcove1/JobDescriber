import pandas as pd
import requests
from datetime import date, timedelta

import logging





def IndeedAPI(jobname,location,pagenumber):
    url = "https://indeed11.p.rapidapi.com/"
    payload = {
	"search_terms": f"{jobname}",
	"location": f"{location}",
	"page": f"{pagenumber}"
    }
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "2fe0ff98c6msh6c53fd94d13195ap1c425bjsn2c2e502a3dc2",
	    "X-RapidAPI-Host": "indeed11.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    try:
        dataframe=pd.read_json(response.text)
    except Exception:
        logging.error("ERROR while getting info from indeed API")
    dataframe = dataframe[['url','company_name','job_title','location','date','summary']].copy()
    dataframe['date']=dataframe['date'].apply(parseInt)
    return dataframe

from serpapi import GoogleSearch

class googleUtil():
    
    api_key = ""
    
    def __init__(self,apiKey):
        self.api_key = apiKey


    def parseInt(self,mot):
        res=""
        for i in mot:
            if i.isnumeric():
                res+=str(i)
        try : 
            nDaysAgo=int(res)
            daysAgo = date.today()- timedelta(days=nDaysAgo)
            daysAgo.strftime("%Y-%m-%d") 
            return daysAgo
        except:
            return ""

    def trytogetinfo(self,info):
        try : 
            return info['posted_at']
        except:
            return ''

    def search(self,jobname,location):
        params = {
            "engine": "google_jobs",
            "q": f'{jobname}',
            "location" : f'{location}',
            "hl": "fr",
            "api_key": f'{self.api_key}'
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        jobs_results = results["jobs_results"]
        df = pd.DataFrame(jobs_results)
        print(df.columns)
        job_title = df['title']
        descriptions = df['description']
        company_name = df['company_name']
        date = df['detected_extensions'].apply(self.trytogetinfo).apply(self.parseInt)
        df_location = df["location"]
        link = df["via"]
        res = df[['title',"via",'location','company_name']].merge(date,left_index=True, right_index=True)
        print(res)
        return df
    

