from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys   # Enter Shift bla bla
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import json


driver_path = "./geckodriver"  # replace with your browser driver s path
# Its Firefox if u use chrome set ChromeOptions for chrome
options = webdriver.FirefoxOptions()


s = Service(executable_path=driver_path)
##########################
driver = webdriver.Firefox(options=options, service=s)


# Login


class LinkedIn:

    def __init__(self, job="industrial engineer"):
        self.job = job.replace(" ", "%20")
        self.URL = "https://www.linkedin.com/jobs/search/?currentJobId=3565247855&f_TPR=r2592000&geoId=92000000&keywords=industrial%20engineer&location=Worldwide&refresh=true"
        self.number_of_jobs = None
        self.company_names = []
        self.titles = []

    def open_page(self):
        driver.maximize_window()
        driver.get(self.URL)
        driver.implicitly_wait(10)

    def fetch_number_of_jobs(self):

        number_of_jobs = driver.find_element(
            By.CLASS_NAME, "results-context-header__job-count").text.replace("+", "").replace(",", "")
        to_number = pd.to_numeric(number_of_jobs)
        self.number_of_jobs = to_number

    def scroll(self):
        i = 2
        while i <= int((5000+200)/25)+1:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            i = i + 1

            try:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.UP)
                send = driver.find_element(
                    By.XPATH, "//button[@aria-label='See more jobs']")
                driver.execute_script("arguments[0].click();", send)

                time.sleep(3)


            except:
                print("Except bloğu çalıştı.")
                pass
                time.sleep(5)

        to_json = {}
        try:
            for count,i in enumerate(range(400)):
                company = driver.find_elements(
                    By.CLASS_NAME, 'base-search-card__subtitle')[i].text
                title = driver.find_elements(
                    By.CLASS_NAME, 'base-search-card__title')[i].text
                location = driver.find_elements(By.CLASS_NAME, "job-search-card__location")[i].text
                link = driver.find_elements(
                    By.CLASS_NAME, 'base-card__full-link')[i].get_attribute('href')
                if company and title and location and link:
                    to_json[count]={
                        "title":title,
                        "companmy":company,
                        "location":location,
                        "url":link
                    
                    }
                
            with open("try.json", "w", encoding="utf-8") as f:
                json.dump(to_json, f, ensure_ascii=False, indent=2)
                
                print("- - - - - - -")
                print(title)
                print(company)
                print(location)
                print(link)
                print("- - - - - - - ")
  
                

        except IndexError:
            print("no")


if __name__ == "__main__":
    tracker = LinkedIn()
    tracker.open_page()
