from lib2to3.pgen2 import driver
import pandas as pd
from selenium import webdriver
import logging
from LinkedInUtil import Linkedin
from IndeedUtil import *
import configparser
from IndeedUtil import googleUtil


def loginInfoLinkedIn():
    config = configparser.ConfigParser()
    config.read("logininfo.config")
    email = config["LinkedIn"]["user"]
    mdp = config["LinkedIn"]["pwd"]
    return email,mdp

def apiinfo():
    config = configparser.ConfigParser()
    config.read("logininfo.config")
    apikey = config["SerpApi"]["Api_Key"]
    return apikey

def initialisationWebDriver():
    driver = webdriver.Chrome('./chromedriver')
    return driver

if __name__=='__main__':
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("START SCRAPPING ...")
    jobname="data engineer"
    location = "Paris"
    jobCollector=[]
    #dataframe2 = IndeedAPI(jobname,location,"1")
    """
    driver = initialisationWebDriver()
    email,mdp = loginInfo()
    jobCollector = Linkedin.traitementLinkedIn(driver,jobname,location,email,mdp)
    driver.close()
    dataframe1 = pd.DataFrame.from_dict(jobCollector)
    combined = pd.concat([dataframe1], ignore_index=True)
    DescriptionRawData = combined['summary']
    combined['summary'] = ""
    #DescriptionRawData.to_csv("RawData.csv")
    combined.to_csv("dataFinal.csv") 
    """
    apikey = apiinfo()
    google = googleUtil(apikey)
    df = google.search(jobname,location)
    df.to_csv("test.csv")
