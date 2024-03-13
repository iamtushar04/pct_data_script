import re

NAME_EXP = r'\sName\s(.*?)Address'
ADDR_EXP = r'Address\s(.*?)State'  # r'address\s(.*?\\n)\d+ [\[|telephone|Email]'
EMAIL_EXP = r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'
# PHONE_EXP = r'([+|0]?[\d|\s|\-]{9,})'
# PHONE_EXP = r'telephone number\s(.*?)\n'
PHONE_EXP = r'(?:Telefon[ea]|phone)\s(?:Number|No)(.*?)(?:\\n|\-\d)'

AG_NAME_EXP = r'Name\s(.*?)Address'
AG_ADDR_EXP = r'Address\s(.*?)\-1\-'  # r'address\s(.*?\\n)\d+ [\[|telephone|Email]'
AG_EMAIL_EXP = r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'
AG_PHONE_EXP = r'\s([\+|0-9\s|\-|\(|\)]{11,})\n'
AG_TYPE = r'(.*?)\-1'  # r'(.*?)\|?Name'

APPLICANT_INFO = r'\[Applicant.*?States(.*?)(?:Applicant\sand|PCT)'
AGENT_INFO = r'Authorities as:(.*?)\-\d\([a|@]\)'
ATTORNEY_INFO = r'following\scapacity:(.*?)\(a\)'


def extract_value_using_regular_expression(exp: str, text: str) -> str:
    try:
        value = re.findall(exp, text, re.IGNORECASE | re.DOTALL)[0].strip().replace("\\n", " ")
    except IndexError:
        value = ''
    return value


def extract_applicant_info(text: str) -> dict[str, str]:
    text_ = re.findall(APPLICANT_INFO, text, re.IGNORECASE | re.DOTALL)
    if len(text_):
        name = extract_value_using_regular_expression(AG_NAME_EXP, text_[0])[:-3]
        address = extract_value_using_regular_expression(ADDR_EXP, text_[0])[:-4]
        email = extract_value_using_regular_expression(EMAIL_EXP, text_[0])
        phone = extract_value_using_regular_expression(AG_PHONE_EXP, text_[0])
        # return f"Name= {name},\nemail= {email},\nTelephone= {phone},\nAddress= {address}"
        return {'Name': name, 'email': email, 'Telephone': phone, 'Address': address}
    else:
        return ""


def extract_agent_info(text: str) -> dict[str, str]:
    text_ = re.findall(AGENT_INFO, text, re.IGNORECASE | re.DOTALL)
    if not len(text_):
        text_ = re.findall(ATTORNEY_INFO, text, re.IGNORECASE | re.DOTALL)
    if len(text_):
        type_ = extract_value_using_regular_expression(AG_TYPE, text_[0])[:-2]
        name = extract_value_using_regular_expression(AG_NAME_EXP, text_[0])
        address = extract_value_using_regular_expression(AG_ADDR_EXP, text_[0])[:-2]
        email = extract_value_using_regular_expression(AG_EMAIL_EXP, text_[0])
        phone = extract_value_using_regular_expression(AG_PHONE_EXP, text_[0])
        # return f"Type= {type_},\nName= {name},\nemail= {email},\nTelephone= {phone},\nAddress = {address}"
        return {'Type': type_, 'Name': name, 'email': email, 'Telephone': 'phone', 'Address': 'address'}
    else:
        return ""


def extract_email(text: str) -> str:
    # test_exp = r'\n([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
    emails = re.findall(EMAIL_EXP, text, re.IGNORECASE | re.DOTALL)
    emails = [email.strip().replace("\\n", " ") for email in emails]
    return '; '.join(list(set(emails)))


def extract_phone(text: str) -> str:
    phone = re.findall(AG_PHONE_EXP, text, re.IGNORECASE | re.DOTALL)
    phone = [ph.replace('|', '').replace('-', '').replace("(", "").replace(")", "").strip() for ph in phone]
    phone = [ph for ph in phone if len(ph) >= 10]
    phone = '\n'.join(phone).split('\n')
    return '; '.join(set([ph for ph in phone if len(ph) >= 10]))