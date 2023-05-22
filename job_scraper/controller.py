import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time


def get_posting_date(posted_time_ago):
    if not posted_time_ago:
        return None
    time = int(posted_time_ago.split(" ")[0])
    todays_date = datetime.datetime.now()

    if "day" in posted_time_ago:
        delta = datetime.timedelta(days=time)
        return (todays_date-delta).strftime('%Y-%m-%d')
    elif "week" in posted_time_ago:
        delta = datetime.timedelta(weeks=time)
        return (todays_date-delta).strftime('%Y-%m-%d')
    elif "month" in posted_time_ago:
        delta = datetime.timedelta(days=time*30)
        return (todays_date-delta).strftime('%Y-%m-%d')

def get_job_locators_text(driver, CSS_SELECTOR):
    try:
        return driver.find_element(
            By.CSS_SELECTOR, CSS_SELECTOR).text
    except NoSuchElementException:
        return None


def get_job_locators_attribute(driver, CSS_SELECTOR, attribute):
    try:
        return driver.find_element(
            By.CSS_SELECTOR, CSS_SELECTOR).get_attribute(attribute)
    except NoSuchElementException:
        return None

def easy_apply_check(apply_button):
    if apply_button == "Easy Apply":
        return True
    else:
        return False

def url_not_found_check(driver):
    try:
        driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div/div[5]/h1").text
        return True
    except:
        return False

def url_control(url):
    if not url.startswith("https://wwww."):
        return "https://www."+url[11:]

def login_screen_check(driver):
    try:
        driver.find_element(
            By.XPATH, "/html/body/main/section[1]/div/div/section[1]/div/div/section/button[1]").click()
    except NoSuchElementException:
        time.sleep(6)
        driver.refresh()
