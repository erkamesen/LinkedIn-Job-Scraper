from selenium.webdriver.common.by import By

""" FETCH GENERAL DATAS """

def get_jobs_text(driver, index, CLASS_NAME):
    try:
        return driver.find_elements(
            By.CLASS_NAME, CLASS_NAME)[index].text
    except IndexError:
        return None
    
def get_jobs_attribute(driver, index, CLASS_NAME, attribute):
    try:
        return driver.find_elements(
            By.CLASS_NAME, CLASS_NAME)[index].get_attribute(attribute)
    except IndexError:
        return None



