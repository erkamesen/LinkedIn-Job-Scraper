from selenium.webdriver.common.by import By
import pandas as pd
import csv
import json
import math
import os
import time
from config import get_driver

from .controller import get_jobs_text, get_jobs_attribute

""" SELENIUM """

# Version: 4.5.0

""" CREATE DRIVER INSTANCE """


driver = get_driver()



###########################

class JobFinder:

    def __init__(self, job_name="industrial engineer", currentJobId=3599754837, geoId=92000000, location="Worldwide"):
        self.job_name = job_name
        self.location = location
        self.currentJobId = currentJobId
        self.geoId = geoId
        self.number_of_pages = None
        self.number_of_jobs = None
        self.filename = str(round(time.time(), 0)).replace(".0", "")
        self.URL = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?currentJobId={currentJobId}&f_TPR=r2592000&geoId={geoId}&keywords={job_name}&location={location}&refresh=true&start="

    def run(self):
        self.set_numbers()
        time.sleep(2)
        for page in range(self.number_of_jobs):
            a = time.time()
            if page > 999:
                print("SCRAPING IS COMPLETE")
                break
            self.open_page(page=(page))
            datas = self.get_datas_from_page()
            self.record_to_csv(data=datas)
            self.number_of_jobs -= 25
            if self.number_of_jobs < 0:
                break
            b = time.time()
            print(f"- - - - -\n\
                  Total Pages: {self.number_of_pages}\nCurrent page: {page}\n\
                  Remaining Jobs: {self.number_of_jobs}\nRemaining Pages: {int(self.number_of_pages)-int(page)}\n- - - - -")
            print("Running Time:", round(b-a, 1), "second", "\n- - - - -")

    def open_page(self, page):
        """
        It takes the value of the start= query as a parameter.
        """
        driver.get(f"{self.URL}{page}")
        
    def set_numbers(self):
        """
        If number_of_jobs is given as a parameter, it returns the page number accordingly.
        Else it goes to the original url and gets the job count there and returns.
        """

        orj_URL = f"https://www.linkedin.com/jobs/search/?currentJobId={self.currentJobId}&f_TPR=r2592000&geoId={self.geoId}&keywords={self.job_name}&location={self.location}&refresh=true"
        driver.get(orj_URL)
        number_of_jobs = driver.find_element(
            By.CLASS_NAME, "results-context-header__job-count").text.replace("+", "").replace(",", "")
        to_number = pd.to_numeric(number_of_jobs)

        if to_number>25000:
            self.number_of_jobs = 25000
        else:
            self.number_of_jobs = to_number
        self.number_of_pages = int(math.ceil(to_number/25))

    def get_datas_from_page(self):
        datas = []
        """ 
        There are 25 jobs per page, we check the status of the remaining number of jobs.
        """
        if self.number_of_jobs >= 25:
            for i in range(25):
                ls = JobFinder.get_jobs(index=i)
                if ls.count(None) == 7:
                    continue
                else:
                    datas.append(ls)

            return datas
        else:
            for i in range(self.number_of_jobs):
                ls = JobFinder.get_jobs(index=i)
                if ls.count(None) == 7:
                    continue
                else:
                    datas.append(ls)

            return datas

    def record_to_csv(self, data: list):
        field_names = ['COMPANY', 'TITLE', 'COMPANY_URL', 'LOCATION', 'BENEFIT',
                'JOB_URL']
        if not os.path.exists(f"{self.filename}.csv"):
            with open(f"{self.filename}.csv", 'w') as f:
                print("CSV FILE CREATED")
                writer = csv.writer(f)
                writer.writerow(field_names)
                self.record_to_csv(data=data)
        else:
            with open(f"{self.filename}.csv", "a") as f:
                writer = csv.writer(f, dialect='excel')
                for item in data:
                    writer.writerow(item)


    @staticmethod
    def get_jobs(index):
        company = get_jobs_text(driver, index, 'base-search-card__subtitle')
        title = get_jobs_text(driver, index, 'base-search-card__title')
        benefit = get_jobs_text(driver, index, "result-benefits__text")
        location = get_jobs_text(driver, index, "job-search-card__location")
        company_url = get_jobs_attribute(driver, index, "hidden-nested-link", "href")
        job_url = get_jobs_attribute(driver, index, 'base-card__full-link', "href")

        return [company, title, company_url, location, benefit, job_url]