
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging


class Linkedin():


    def logintoLinkedIn(self,user, mdp, driver: webdriver.Chrome):
        driver.get("https://www.linkedin.com/login")
        usernameBar = driver.find_element("id", "username")
        usernameBar.send_keys(user)
        passwordBar = driver.find_element("id", "password")
        passwordBar.send_keys(mdp)
        btn = driver.find_element_by_xpath(
            '//*[@id="organic-div"]/form/div[3]/button')
        btn.click()
        return driver


    def searchlinkedIn(self,driver: webdriver.Chrome, jobname: str, location: str):
        numberofspace = jobname.count(" ")
        convertedStringjobname = jobname.replace(" ", "%20", numberofspace)
        numberofspace = location.count(" ")
        convertedStringLocation = location.replace(" ", "%20", numberofspace)
        url = f"https://www.linkedin.com/jobs/search?&keywords={ convertedStringjobname }&location={ convertedStringLocation }&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'"
        driver.get(url)
        LocationBar = driver.find_element(
            By.XPATH, "/html/body/div[3]/header/nav/section/section[2]/form/section[2]/input")
        LocationBar.click()
        driver.find_element(
             By.XPATH, "/html/body/div[3]/header/nav/section/section[2]/form/section[2]/button").click()
        LocationBar.send_keys(location + Keys.ENTER)
        sleep(2)
       # scroll down to have more info
        for i in range(3):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        return driver


    def getDescriptionLinkedIn(self,email, mdp, JobCollector, driver):
        driver = self.logintoLinkedIn(email, mdp, driver)
        for job in JobCollector:
            url = job['url']
            try:
                driver.get(url)
            except:
                logging.error("EROOR", "Check connection for url ", url)
            sleep(1)
            try:
                jobDescription = BeautifulSoup(
                    driver.page_source, 'html.parser').find(id="job-details")
                job['summary'] = jobDescription
            except:
                continue
        return JobCollector


    def traitementLinkedIn(self,d, jobname, location, email, mdp):
        JobCollector = []
        driver = self.searchlinkedIn(d, jobname, location)
        source = BeautifulSoup(driver.page_source, 'html.parser')
        tags = source.find_all(class_="base-search-card__title")
        for tag in tags:
            try:
                if tag.string != None:
                    jobname = tag.string.strip()
                    time = tag.parent.time["datetime"]
                    company = tag.parent.a.string.strip()
                    url = tag.parent.parent.a["href"]
                    location = tag.parent.find(
                        class_='job-search-card__location').string.strip()
                    job = {"job_title": jobname,
                           "date": time,
                           "company_name": company,
                           "location": location,
                           "url": url}
                    JobCollector.append(job)
            except:
                continue
        JobCollector = self.getDescriptionLinkedIn(email, mdp, JobCollector, driver)

        return JobCollector
