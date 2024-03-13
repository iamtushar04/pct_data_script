import os.path
import pandas as pd
from source.config import read_config
from source.explore_web import WebTraversal



def read_excel(file):
    try:
        data = pd.read_excel(file)
        data = data.rename(columns=data.iloc[1])[2:].drop_duplicates(subset=['ID'], keep='first')
        return data.reset_index(drop=True)
    except FileNotFoundError:
        return f"File not found. Please Extract the file"

CONFIG = read_config("config.json")


class GetData(WebTraversal):

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def get_data():
        if not os.path.exists(CONFIG.EXCEL_INPUT_FILE):
            web_driver = WebTraversal(CONFIG.URL)
            web_driver.download_excel_file()
        return read_excel(CONFIG.EXCEL_INPUT_FILE)





