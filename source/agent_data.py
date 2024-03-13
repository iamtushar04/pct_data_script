import csv
import os
from datetime import datetime, date, timedelta
from source.config import read_config
from source.explore_web import WebTraversal
import pandas as pd
from source.data_processing import GetData, read_excel
from source import ocr_extract
from source.const import LANG_MAP
from source.store_to_csv import save_csv
from source.output_dict import get_output
from source.os_operations import get_latest_pdf, remove_file
import re

MONTHS_TO_TRAVEL = 27

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 500)

RESULT_KEYS = ["Publication Number", "Publication Date", "International Application No.", "International Filing Date",
               "IPC", "Applicants", "Inventors", "Agents", "Priority Data", "Publication Language", "Filing Language",
               "Applicant_info", "Agent_info"]


def filter_lang(lang_: str) -> str:
    try:
        match = re.search(r'^(.*?)\(', lang_)
        if match:
            return LANG_MAP[match.group(1).strip()]
        else:
            return LANG_MAP[lang_.strip()]
    except KeyError:
        return "en"


def ScrapData():
    CONFIG = read_config("config.json")
    web_driver = WebTraversal()
    if not os.path.exists(CONFIG.EXCEL_INPUT_FILE):
        web_driver.goto_webpage(CONFIG.URL)
        web_driver.download_excel_file()
    data = read_excel(CONFIG.EXCEL_INPUT_FILE)
    data['flag'] = data['Appl.No'].apply(lambda x: True if x.startswith('US') else False)
    data = data[data['flag'] == True].reset_index(drop=True)
    doc_ids = data['ID'].to_list()
    print(len(doc_ids))
    count = 1
    for doc_id in doc_ids[209:]:  # start today [760:]
        print(doc_id)
        doc_url = CONFIG.DOC_URL.format(doc_id=doc_id)
        inner_data = web_driver.get_inner_data(url=doc_url)
        if 'Publication Language' in inner_data:
            lang = None if inner_data['Publication Language'] is None else filter_lang(
                inner_data['Publication Language'])
        else:
            lang = None

        unwanted = set(inner_data) - set(RESULT_KEYS)
        for unwanted_key in unwanted: del inner_data[unwanted_key]
        inner_data['Weblink'] = doc_url
        inner_data['Title'] = data.loc[data['ID'] == doc_id]['Title'].to_string(index=False)
        print(f"Priority Data :{inner_data['Priority Data']}")
        print(f"count: {count}")
        if inner_data['Priority Data'] != '':
            if check_priority(inner_data['Priority Data']):
                t_data = ocr_extract.extract_ocr_data(CONFIG.DOWNLOAD_PATH, lang=lang)
                inner_data = inner_data | t_data
                output = get_output(inner_data).__dict__
                save_csv(os.path.join(CONFIG.DOWNLOAD_PATH, CONFIG.OUTPUT_CSV), output)
                print(f"Stored records: {count}")
            else:
                print(f"Priority Date {inner_data['Priority Data']} is not Qualifying.....")
                remove_file(file=os.path.join(CONFIG.DOWNLOAD_PATH, get_latest_pdf(CONFIG.DOWNLOAD_PATH)))

        else:
            remove_file(file=os.path.join(CONFIG.DOWNLOAD_PATH, get_latest_pdf(CONFIG.DOWNLOAD_PATH)))
        count += 1
    web_driver.close_driver()


def check_priority(date_: str) -> bool:
    """
    Title: Compare qualify_date with priority date to check if it qualifing or not
    Args:
        date_: date string

    Returns:

    """
    dates = [datetime.strptime(_,"%d.%m.%Y").date() for _ in date_.split(' ') if '.' in _]
    qualify_date = get_back_travelled_date(months=MONTHS_TO_TRAVEL)
    return True if min(dates) >= qualify_date else False


def get_back_travelled_date(months: int):
    """
    Title: Function to return the earlier date from today by going back to given months
    Args:
        months: Number of month that you want to go back

    Returns: back travelled date
    """
    today = date.today()
    earliest_date = today - t-imedelta(days=today.day)
    earliest_date -= timedelta(days=30 * months)

    print(f"{months} Months Ago:", earliest_date)
    return earliest_date




if __name__ == "__main__":
    ScrapData()
