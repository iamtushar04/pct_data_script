import os
import datetime

today = datetime.date.today()

DOWNLOAD_DIR = "C:\\Users\\Software\\Downloads"


def get_latest_pdf(file_path: str) -> str:
    pdf_files = [os.path.join(file_path, file) for file in os.listdir(file_path) if file.endswith(".pdf")]
    today_files = [file for file in pdf_files if datetime.date.fromtimestamp(os.path.getmtime(file)) == today]
    today_files.sort(key=os.path.getmtime, reverse=True)
    return today_files[0]

def remove_file(file: str):
    try:
        os.remove(file)
    except:
        pass

