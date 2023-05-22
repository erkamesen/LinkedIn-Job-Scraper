from selenium import webdriver 
from selenium.webdriver.firefox.service import Service # selenium.webdriver.chrome.service
from selenium.webdriver.firefox.options import Options



# Its Firefox if u use chrome set ChromeOptions for chrome
def get_driver():
    driver_path = "./geckodriver"  # replace with your browser driver s path
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    return webdriver.Firefox(options=options, service=Service(
        executable_path=driver_path))  # webdriver.Chrome() & webdriver.ChromeOptions()
    
