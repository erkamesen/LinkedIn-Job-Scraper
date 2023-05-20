from selenium import webdriver
# selenium.webdriver.chrome.service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import json
import math
import os
import time



""" SELENIUM """

# Version: 4.5.0

""" CREATE DRIVER INSTANCE """
# Its Firefox if u use chrome set ChromeOptions for chrome

driver_path = "./geckodriver"  # replace with your browser driver s path
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Firefox(options=options, service=Service(
    executable_path=driver_path))  # webdriver.Chrome() & webdriver.ChromeOptions()

###########################

class LinkedIn:

    def __init__(self, job_name="industrial engineer", currentJobId=3599754837, geoId=92000000, number_of_jobs=None, location="Worldwide"):
        self.job_name = job_name
        self.location = location
        self.currentJobId = currentJobId
        self.geoId = geoId
        self.number_of_jobs = number_of_jobs
        self.number_of_pages = None
        self.filename = str(round(time.time(), 0)).replace(".0", "")
        self.URL = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?currentJobId={currentJobId}&f_TPR=r2592000&geoId={geoId}&keywords={job_name}&location={location}&refresh=true&start="

    def run(self):
        self.fetch_numbers()
        time.sleep(2)
        for page in range(self.number_of_jobs):
            a = time.time()
            if page > 999:
                print("SCRAPING IS COMPLETE")
                break
            self.open_page(page=(page))
            datas = self.fetch_datas()
            self.record_to_csv(data=datas)
            self.number_of_jobs -= 25
            if self.number_of_jobs < 0:
                break
            b = time.time()
            print(f"- - - - -\n\
                  Total Pages: {self.number_of_pages}\nCurrent page: {page}\n\
                  Remaining Jobs: {self.number_of_jobs}\nRemaining Pages: {int(self.number_of_pages)-int(page)}\n- - - - -")
            print("Running Time:", round(b-a,1), "second", "\n- - - - -")
    def open_page(self, page):
        """
        It takes the value of the start= query as a parameter.
        """
        driver.get(f"{self.URL}{page}")

    def fetch_numbers(self):
        """
        If number_of_jobs is given as a parameter, it returns the page number accordingly.
        Else it goes to the original url and gets the job count there and returns.
        """
        driver.maximize_window()
        if self.number_of_jobs:
            self.number_of_pages = int(math.ceil(self.number_of_jobs/25))
        else:

            orj_URL = f"https://www.linkedin.com/jobs/search/?currentJobId={self.currentJobId}&f_TPR=r2592000&geoId={self.geoId}&keywords={self.job_name}&location={self.location}&refresh=true"
            driver.get(orj_URL)
            number_of_jobs = driver.find_element(
                By.CLASS_NAME, "results-context-header__job-count").text.replace("+", "").replace(",", "")
            to_number = pd.to_numeric(number_of_jobs)
            self.number_of_jobs = to_number
            self.number_of_pages = int(math.ceil(to_number/25))

    def fetch_datas(self):
        datas = []
        """ 
        There are 25 jobs per page, we check the status of the remaining number of jobs.
        """
        if self.number_of_jobs > 25:
            for i in range(25):
                ls = LinkedIn.find_elems(index=i)
                if ls.count("Unknown") == 7:
                    continue
                else:
                    datas.append(LinkedIn.find_elems(index=i))
            return datas
        else:
            for i in range(self.number_of_jobs):
                ls = LinkedIn.find_elems(index=i)
                if ls.count("Unknown") == 7:
                    continue
                else:
                    datas.append(LinkedIn.find_elems(index=i))
            return datas

    def fetch_job_datas(self, job_link):

        driver.get(job_link)
        driver.find_element(
            By.XPATH, "/html/body/main/section[1]/div/div/section[1]/div/div/section/button[1]").click()
        time.sleep(0.1)
        job_description = driver.find_element(
            By.CLASS_NAME, "decorated-job-posting__details").text
        print(job_description)
        print(driver.find_element(By.CLASS_NAME,
              "artdeco-entity-image ").get_attribute("src"))
        print(driver.find_element(By.CLASS_NAME,
              "description__job-criteria-list").text)

    @staticmethod
    def find_elems(index):
        try:
            company = driver.find_elements(
                By.CLASS_NAME, 'base-search-card__subtitle')[index].text
        except IndexError:
            company = "Unknown"
        try:
            company_url = driver.find_elements(
                By.CLASS_NAME, "hidden-nested-link")[index].get_attribute('href')
        except IndexError:
            company_url = "Unknown"
        try:
            title = driver.find_elements(
                By.CLASS_NAME, 'base-search-card__title')[index].text
        except IndexError:
            title = "Unknown"
        try:
            benefit = driver.find_elements(
                By.CLASS_NAME, "result-benefits__text")[index].text
        except IndexError:
            benefit = "Unkown"
        try:
            location = driver.find_elements(
                By.CLASS_NAME, "job-search-card__location")[index].text
        except IndexError:
            location = "Unknown"
        try:
            link = driver.find_elements(
                By.CLASS_NAME, 'base-card__full-link')[index].get_attribute('href')
        except IndexError:
            link = "Unknown"
        try:
            listing_date = driver.find_elements(
                By.CLASS_NAME, "job-search-card__listdate")[index].text
        except IndexError:
            listing_date = "Unknown"

        return [company, title, company_url, location, benefit, link, listing_date]

    def record_to_json(self, data: list):
        for count, item in enumerate(data):
            to_json = {
                count: item
            }
        if not os.path.exists(f"{self.filename}.json"):
            with open(f"{self.filename}.json", "w") as f:
                print("JSON FILE CREATED")
        else:
            with open(f"{self.filename}.json", "a", encoding="utf-8") as f:
                for item in data:
                    to_json = {
                        "COMPANY": item[0],
                        "TITLE": item[1],
                        "COMPANY_URL": item[2],
                        "LOCATION": item[3],
                        "BENEFIT": item[4],
                        "JOB_URL": item[5],
                        "LISTING_DATE": item[6]
                    }
                    json.dump(to_json, f, ensure_ascii=False, indent=None)

    def record_to_csv(self, data: list):
        field_names = ['COMPANY', 'TITLE', 'COMPANY_URL', 'LOCATION', 'BENEFIT',
                       'JOB_URL', 'LISTING_DATE']
        if not os.path.exists(f"{self.filename}.csv"):
            with open(f"{self.filename}.csv", 'w') as f:
                print("CSV FILE CREATED")
                writer = csv.writer(f)
                writer.writerow(field_names)
        else:
            with open(f"{self.filename}.csv", "a") as f:
                writer = csv.writer(f, dialect='excel')
                for item in data:
                    writer.writerow(item)