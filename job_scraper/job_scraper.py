from config import get_driver
import csv
import time
import os
from .controller import url_control, url_not_found_check, login_screen_check,\
      get_job_locators_attribute, get_job_locators_text, get_posting_date, set_filename


class JobScraper:
    field_names = ['COMPANY', 'TITLE', 'COMPANY_URL', 'LOCATION', 'BENEFIT',
                            'JOB_URL', "JOB_DESCRIPTION", "COMPANY_IMAGE", "APPLICANT_NUM", "POSTED_TIME",
                                "SENIORITY_LEVEL", "EMPLOYMENT_TYPE", "JOB_FUNCTION", "INDUSTRIES"]


    def __init__(self, filename):
        self.filename = set_filename(filename)
        self.driver = get_driver()
        

    def run(self):
        data = self.read_csv()
        for count, data in enumerate(csv.DictReader(data)):
            print("SCRAPING....")
            print(count, "\n- - - - -")
            JOB_URL = data["JOB_URL"]
            if not JOB_URL:
                print("URL NOT FOUND")
                continue
            print(data["JOB_URL"])
            job_datas = self.fetch_job_datas(job_link=JOB_URL)
            if not job_datas:
                print("URL NOT FOUND, PASSING...")
                continue
            data.update(job_datas)
            self.records_to_csv(data=data)
        data.close()

    
    def fetch_job_datas(self, job_link) -> dict:
        time.sleep(1)

        job_link = url_control(job_link)
        self.driver.get(job_link)

        if url_not_found_check(self.driver):
            return {}

        login_screen_check(self.driver)

        job_description = get_job_locators_text(
            self.driver, ".decorated-job-posting__details")
        posted_time_ago = get_job_locators_text(
            self.driver, ".posted-time-ago__text")
        applicant_num = get_job_locators_text(
            self.driver, ".num-applicants__caption")
        seniority_level = get_job_locators_text(
            self.driver, "li.description__job-criteria-item:nth-child(1) > span:nth-child(2)")
        employment_type = get_job_locators_text(
            self.driver, "li.description__job-criteria-item:nth-child(2) > span:nth-child(2)")
        job_function = get_job_locators_text(
            self.driver, "li.description__job-criteria-item:nth-child(3) > span:nth-child(2)")
        industries = get_job_locators_text(
            self.driver, "li.description__job-criteria-item:nth-child(4) > h3:nth-child(1)")
        company_image = get_job_locators_attribute(
            self.driver, ".artdeco-entity-image--square-3", "src")

        posted_time = get_posting_date(posted_time_ago=posted_time_ago)
    

        return {"JOB_DESCRIPTION": job_description, "COMPANY_IMAGE": company_image,
                "APPLICANT_NUM": applicant_num, "POSTED_TIME": posted_time, "SENIORITY_LEVEL": seniority_level,
                "EMPLOYMENT_TYPE": employment_type, "JOB_FUNCTION": job_function, "INDUSTRIES": industries}

    def records_to_csv(self, data: dict):
        if not os.path.exists(f"job-details-{self.filename}"):
            with open(f"job-details-{self.filename}", 'w') as f:
                print("CSV FILE CREATED")
                writer = csv.writer(f)
                writer.writerow(JobScraper.field_names)

        with open(f"job-details-{self.filename}", "a") as output:
            writer = csv.DictWriter(output, data.keys())
            writer.writerow(data)

    
    def read_csv(self):
        data = open(f"{self.filename}", "r")
        return data