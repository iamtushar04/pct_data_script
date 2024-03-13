from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Result:
    publication_number:str
    title: str
    weblink: str
    publication_date: str
    international_application_no: Optional[str] = None
    international_filing_date: Optional[str] = None
    ipc: Optional[str] = None
    applicants: Optional[str] = None
    inventors: Optional[str] = None
    agents: Optional[str] = None
    priority_data: Optional[str] = None
    publication_language: Optional[str] = None
    filing_language: Optional[str] = None
    applicant_info: Optional[dict] = None
    agent_info: Optional[dict] = None
    email: Optional[str] = None
    phone: Optional[str] = None


def get_output(data_dict: dict) -> Result:
    data_keys = list(data_dict.keys())
    for key in (data_keys):
        data_dict[key.replace(' ', '_').replace('.', '').lower()] = data_dict.pop(key)
    return Result(**data_dict)