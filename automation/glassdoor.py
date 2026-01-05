import time
import bs4

from selenium import webdriver
import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = uc.Chrome()
driver.get("https://www.glassdoor.com/index.htm")
time.sleep(10)

email_input = driver.find_element(By.ID, "inlineUserEmail")
email_input.click()
email_input.send_keys("uhr88nrsf@mozmail.com")

continue_with_email = driver.find_element(By.CLASS_NAME, "emailButton")
continue_with_email.click()

time.sleep(2)
password = driver.find_element(By.ID, "inlineUserPassword")
password.click()
password.send_keys("'f>$GHthtF^ktw9")

enter_pass = driver.find_element(By.CLASS_NAME, "ButtonContainer")
enter_pass.click()
time.sleep(5)

jobs = driver.find_element(
    By.CSS_SELECTOR,
    "div > div > div > ul > li:nth-child(2)"
)

jobs.click()
time.sleep(5)

search_bar = driver.find_element(By.ID, "searchBar-jobTitle")
search_bar.click()
search_bar.send_keys("Python Developer")
time.sleep(2)

location_bar = driver.find_element(By.ID, "searchBar-location")
location_bar.clear()
location_bar.click()
location_bar.send_keys("Lahore (Pakistan)")
location_bar.send_keys(Keys.ENTER)
# time.sleep(25)


# Scrape html data
parser = bs4.BeautifulSoup(driver.page_source, "html.parser")
print(parser.prettify())

job_results = parser.find_all("div", class_="JobDetails_jobDetailsContainer__y9P3L")
print(f"Total Jobs Found: {len(job_results)}, {job_results}")
