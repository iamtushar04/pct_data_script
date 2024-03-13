import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from source.explore_web import WebTraversal
import time
import pandas as pd

URL = "https://www.gtlaw.com/en/professionals?&keyword=Trademark"
# web_driver = WebTraversal()
# web_driver.goto_webpage(URL)

# options = Options()
# options.add_experimental_option("prefs", CHROME_PDF_DOWNLOAD_PREFERENCE)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url=URL)
driver.maximize_window()
time.sleep(2)
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
next_page = "https://www.gtlaw.com/en/professionals?pageNum={page_num}&keyword=Trademark"
# data = driver.find_element(By.CLASS_NAME, "coveo-result-list-container coveo-list-layout-container")
result = []
total_records = 248#int(driver.find_element(By.CLASS_NAME, "coveo-highlight-total-count").text)
page_num=1
while len(result) <= total_records:
    try:
        data = driver.find_elements(By.CLASS_NAME, "info-container")
        if len(data):
            url = driver.current_url
            for i in range(1, len(data)+1):
                driver.find_element(By.XPATH,
                                    f'//*[@id="main-content"]/main/div[5]/div[2]/div[1]/div[{i}]/div[2]/div[1]/div[1]/a').click()
                time.sleep(1)
                temp = {}
                temp['name'] = driver.find_element(By.CLASS_NAME, "name").text
                temp['designation'] = driver.find_element(By.CLASS_NAME, "main-title").text
                temp['email'] = driver.find_element(By.CLASS_NAME, "email").text
                temp['location'] = driver.find_element(By.CLASS_NAME, "office-link").text
                phone = driver.find_elements(By.CLASS_NAME, "phone")
                temp['phone'] = ', '.join([element.text for element in phone])
                print(temp)
                driver.get(url=url)
                time.sleep(1)
                result.append(temp)

        page_num += 1
        driver.get(url=next_page.format(page_num=page_num)) #driver.find_element(By.CLASS_NAME, "coveo-pager-next-icon").click()
        time.sleep(1)
    except IndexError:
        pass
    except Exception as e:
        pass
import pdb;pdb.set_trace()
df = pd.DataFrame(result)
df.to_csv("GreenbergTraurig.csv")
print("Successfully Fetched Data")
