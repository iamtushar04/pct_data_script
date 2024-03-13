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

keyword = "Trademark"
URL = "https://www.dlapiper.com/en/people#q=Trademark&t=All&sort=relevancy&numberOfResults=100"
next_page = "https://www.dlapiper.com/en/people#q=Trademark&first={page}&t=All&sort=relevancy&numberOfResults=100"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url=URL)
driver.maximize_window()
time.sleep(2)
import pdb;pdb.set_trace()
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
data = driver.find_elements(By.CLASS_NAME, "coveo-result-cell")
result = []

total_records = int(driver.find_element(By.CLASS_NAME, "CoveoQuerySummary").text)
records = 0
driver.find_elements(By.CSS_SELECTOR, 'span')
#CoveoFieldValue
while len(result) != total_records:
    try:
        data = driver.find_elements(By.CLASS_NAME, "professional__column--right")
        extracted_data = [element.text for element in data if element.text != '']
        i = 1;
        for each in extracted_data:
            print(i)
            row = each.split('\n')
            temp = {}
            temp['name'] = row[0]
            temp['designation'] = row[1]
            temp['location & phone'] = row[2]
            temp['email'] = row[3]
            try:
                elements = driver.find_elements(By.XPATH, f'//*[@id="coveoc76d944b"]/div[2]/div[{i}]/div/a')
                links = [element.get_attribute('href') for element in elements]
                if len(links) == 1:
                    temp['link'] = links[0]
                else:
                    temp['link'] = links[1]
            except:
                temp['link'] = ''
            result.append(temp)
            i+=1
        records +=20
        driver.get(url=next_page.format(page=records)) #driver.find_element(By.CLASS_NAME, "coveo-pager-next-icon").click()
        time.sleep(3)
    except IndexError:
        pass
    except Exception as e:
        pass
df = pd.DataFrame(result)
df.to_csv("dlapiper_data.csv")
print("Successfully Fetched Data")
