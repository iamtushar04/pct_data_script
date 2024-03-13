import json
from dataclasses import dataclass

@dataclass
class Config:
    URL: str
    EXCEL_INPUT_FILE: str
    OUTPUT_CSV: str
    DOC_URL: str
    DOWNLOAD_PATH: str
    CSV_HEADERS: list[str]

def read_config(config_file: str) -> Config:
    with open(config_file) as file:
        data = json.load(file)
        return Config(**data)
