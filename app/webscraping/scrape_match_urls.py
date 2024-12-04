from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_full_url(url):
    full_url = 'vlr.gg' + url
    return full_url

def get_match_urls(driver):
    urls = []
    for x in range(3, 25):
        driver.get(f'https://www.vlr.gg/matches/results/?page={x}')
        a_elements = driver.find_elements(By.XPATH, '//div[@class="wf-card"]/a')
        for a in a_elements:
            urls.append(a.get_attribute('href'))
    return urls