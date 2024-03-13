import selenium.common.exceptions
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from source.web_selenium_config import read_web_config
from source.ocr_extract import extract_ocr_data


class WebTraversal:

    def __init__(self, url=None):
        self.config = read_web_config("web_selenium_config.json")
        self.url = url
        options = Options()
        options.add_experimental_option(self.config.PREFERENCE, self.config.CHROME_PDF_DOWNLOAD_PREFERENCE)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def goto_webpage(self, url=None):
        if url is None:
            url = self.url
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(self.config.LARGE_WAIT)

    def download_excel_file(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(self.config.MED_WAIT)
        select = Select(self.driver.find_element(By.ID, self.config.PCT_WEEK_DROPDOWN_ID))
        select.select_by_index(self.config.TOP_ITEM)
        time.sleep(self.config.TINY_WAIT)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, self.config.DOWNLOAD_EXCEL).click()
        time.sleep(self.config.MED_WAIT)

    def get_biblio_data(self, url):
        # self.driver.get(url)
        # time.sleep(self.config.MED_WAIT)
        # self.driver.find_element(By.PARTIAL_LINK_TEXT, self.config.PCT_BIBLIO_DATA).click()
        # time.sleep(self.config.TINY_WAIT)
        biblo_labels = self.driver.find_elements(By.CLASS_NAME, self.config.BIBLO_LABELS_CLASS_NAME)
        biblo_labels = [element.text.split(self.config.NEXT_LINE)[0] for element in biblo_labels][:-4]
        biblo_values = self.driver.find_elements(By.CLASS_NAME, self.config.BIBLO_VALUES_CLASS_NAME)
        biblo_values = [element.text.split(self.config.NEXT_LINE)[0] for element in biblo_values][:-4]
        if not len(biblo_values):
            self.driver.refresh()
            time.sleep(self.config.LARGE_WAIT)
            self.get_biblio_data(url)
        else:
            return dict(zip(biblo_labels, biblo_values))

    def download_document_pdf(self):
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.config.DOCUMENTS).click()
            time.sleep(self.config.TINY_WAIT)
            td_element = self.driver.find_element(By.XPATH, self.config.DOCUMENT_REQUEST_FORM_XPATH)
            parent_row = td_element.find_element(By.XPATH, self.config.DOCUMENT_PARENT_ROW)
            parent_row.find_element(By.PARTIAL_LINK_TEXT, self.config.PDF).click()
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.config.PCT_BIBLIO_DATA).click()
            # ele = parent_row.find_element(By.PARTIAL_LINK_TEXT, self.config.PDF).click()
            # link = ele.get_attribute("href")
            # ele.click()
            time.sleep(self.config.MED_WAIT)
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(self.config.AVG_WAIT)
            self.download_document_pdf()

    def get_inner_data(self, url):
        self.driver.get(url)
        time.sleep(self.config.MED_WAIT)
        data = self.get_biblio_data(url)
        self.download_document_pdf()
        return data

    def close_driver(self):
        self.driver.quit()
