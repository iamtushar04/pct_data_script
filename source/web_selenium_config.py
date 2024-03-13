import json
from dataclasses import dataclass


@dataclass
class WebSeleniumConfig:
    PCT_WEEK_DROPDOWN_ID: str
    DOWNLOAD_EXCEL: str
    TOP_ITEM: int
    TINY_WAIT: int
    AVG_WAIT: int
    MED_WAIT: int
    LARGE_WAIT: int
    DOCUMENTS: str
    PCT_BIBLIO_DATA: str
    BIBLO_LABELS_CLASS_NAME: str
    BIBLO_VALUES_CLASS_NAME: str
    DOCUMENT_REQUEST_FORM_XPATH: str
    DOCUMENT_PARENT_ROW: str
    BIBLO_FIELD_MAP: list[str]
    PREFERENCE: str
    PDF: str
    NEXT_LINE: str
    CHROME_PDF_DOWNLOAD_PREFERENCE: dict[str, any]


def read_web_config(file_: str) -> WebSeleniumConfig:
    with open(file_) as file:
        web_config = json.load(file)
        return WebSeleniumConfig(**web_config)
