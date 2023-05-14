import pandas as pd
from selenium import webdriver
import logging
from LinkedInUtil import Linkedin
from GoogleUtil import googleUtil






def initialisationWebDriver():
    driver = webdriver.Chrome("./config/chromedriver")
    return driver

if __name__=='__main__':
    logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("START SCRAPPING ...")
    jobname="data engineer"
    location = "Paris"
    jobCollector=[]
    driver = initialisationWebDriver()
    linkendIn_agent = Linkedin()
    email,mdp = linkendIn_agent.loginInfoLinkedIn()
    jobCollector = linkendIn_agent.traitementLinkedIn(d=driver,jobname=jobname,location=location,email=email,mdp=mdp)
    driver.close()
    dataframe1 = pd.DataFrame.from_dict(jobCollector)
    combined = pd.concat([dataframe1], ignore_index=True)
    combined.to_csv("dataFinal.csv",index=False) 
    google_agent = googleUtil()
    google_agent.apiinfo()
    df = google_agent.search(jobname,location)
    df.to_csv("test.csv")
