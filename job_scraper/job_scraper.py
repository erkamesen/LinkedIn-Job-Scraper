from config import get_driver
import csv
import time, os
from .controller import url_control, url_not_found_check, login_screen_check,\
      get_job_locators_attribute, get_job_locators_text, get_posting_date, easy_apply_check



driver = get_driver()



class JobScraper:
    field_names = ['COMPANY', 'TITLE', 'COMPANY_URL', 'LOCATION', 'BENEFIT',
                            'JOB_URL',"JOB_DESCRIPTION", "EASY_APPLY", "COMPANY_IMAGE", "APPLICANT_NUM", "POSTED_TIME",
                                "SENIORITY_LEVEL", "EMPLOYMENT_TYPE", "JOB_FUNCTION", "INDUSTRIES"]


    def __init__(self, filename):
        self.filename = filename

    
    
    def run(self):
        with open(self.filename, "r") as data:
            for count,data in enumerate(csv.DictReader(data)):
                print("SCRAPING....")
                print(count, "\n- - - - -")
                JOB_URL = data["JOB_URL"]
                if not JOB_URL:
                    print("URL NOT FOUND")
                    continue
                print(data["JOB_URL"])
                job_datas = JobScraper.fetch_job_datas(job_link=JOB_URL)
                if not job_datas:
                    print("URL NOT FOUND PASSING...")
                    continue

                data.update(job_datas)
                if not os.path.exists(f"{self.filename}-job-details.csv"):
                    with open(f"{self.filename}-job-details.csv", 'w') as f:
                        print("CSV FILE CREATED")
                        writer = csv.writer(f)
                        writer.writerow(JobScraper.field_names)
              
                with open(f"{self.filename}-job-details.csv", "a") as output:
                    writer = csv.DictWriter(output, data.keys())
                    writer.writerow(data)


    @staticmethod
    def fetch_job_datas(job_link) -> dict:
        time.sleep(1)

        job_link = url_control(job_link)
        driver.get(job_link)

        if url_not_found_check(driver):
            return {}

        login_screen_check(driver)

        job_description = get_job_locators_text(
            driver, ".decorated-job-posting__details")
        posted_time_ago = get_job_locators_text(driver, ".posted-time-ago__text")
        applicant_num = get_job_locators_text(driver, ".num-applicants__caption")
        apply_button = get_job_locators_text(
            driver, "button.apply-button:nth-child(1)")
        seniority_level = get_job_locators_text(
            driver, "li.description__job-criteria-item:nth-child(1) > span:nth-child(2)")
        employment_type = get_job_locators_text(
            driver, "li.description__job-criteria-item:nth-child(2) > span:nth-child(2)")
        job_function = get_job_locators_text(
            driver, "li.description__job-criteria-item:nth-child(3) > span:nth-child(2)")
        industries = get_job_locators_text(
            driver, "li.description__job-criteria-item:nth-child(4) > h3:nth-child(1)")
        company_image = get_job_locators_attribute(
            driver, ".artdeco-entity-image--square-3", "src")

        posted_time = get_posting_date(posted_time_ago=posted_time_ago)
        easy_apply = easy_apply_check(apply_button=apply_button)

        return {"JOB_DESCRIPTION": job_description, "EASY_APPLY": easy_apply, "COMPANY_IMAGE": company_image,
                "APPLICANT_NUM": applicant_num, "POSTED_TIME": posted_time, "SENIORITY_LEVEL": seniority_level,
                "EMPLOYMENT_TYPE": employment_type, "JOB_FUNCTION": job_function, "INDUSTRIES": industries}


