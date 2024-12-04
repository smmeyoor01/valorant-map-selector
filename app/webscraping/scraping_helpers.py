from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver (e.g., Chrome)

# Function to extract agent name from URL
def agent_name(url):
    return url[39:-4].upper()

def get_base_url(driver):
    return driver.find_element(By.XPATH, "/html/head/link[10]").get_attribute('href')

# Function to get map IDs
def get_map_ids(driver):
    map_ids = []
    map_elements = driver.find_elements(By.CSS_SELECTOR, '.vm-stats-gamesnav-item.js-map-switch')[1::]
    for element in map_elements:
        if element.get_attribute('data-disabled') == '0':
            map_ids.append(int(element.get_attribute('data-game-id')))
    return map_ids