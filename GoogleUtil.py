import pandas as pd
import requests
from datetime import date, timedelta
from serpapi import GoogleSearch
import configparser

import logging



"""

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
"""

class googleUtil():
        
    def apiinfo(self):
        config = configparser.ConfigParser()
        config.read("./config/logininfo.config")
        self.api_key = config["SerpApi"]["Api_Key"]

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

    def getinfo(self,info):
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
        date = df['detected_extensions'].apply(self.getinfo).apply(self.parseInt)
        df_location = df["location"]
        link = df["via"]
        res = df[['title',"via",'location','company_name','description']].merge(date,left_index=True, right_index=True)
        descriptions.to_csv("RawData2.txt")
        print(res)
        return res
    

