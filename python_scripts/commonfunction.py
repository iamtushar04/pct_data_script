import os
import requests,socket
import subprocess
import PyPDF2
from PIL import Image
import pytesseract
#from pdf2image import convеrt_from_path
from fake_useragent import UserAgent




def DownloadFile(**kwargs):
    if not os.path.exists(kwargs["dest_folder"]):
        os.makedirs(kwargs["dest_folder"])  # create folder if it does not exist

    ua_str = UserAgent().chrome
    filename = kwargs["url"].split('/')[-1].replace(" ", "_")
    file_path = os.path.join(kwargs["dest_folder"], filename)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:108.0) Gecko/20100101 Firefox/108.0'}
    headers= {"User-Agent": ua_str}

    r = requests.get(kwargs["url"],headers=headers)#, stream=True, verify=False)
    """if socket.gethostbyname(socket.gethostname()).startswith(('8', '9', '7')):
        r = requests.get(kwargs["url"], stream=True, proxies={'http': 'http://10.168.168.48:8001', 'https': 'http://10.168.168.48:8000'})
    else:
        r = requests.get(kwargs["url"], stream=True) """
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        #print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        print("Download failed: status code {}".format(r.status_code))





def pdftotext(pdf, page=None):
    """Retrieve all text from a PDF file.
    Arguments:
        pdf Path of the file to read.
        page: Number of the page to read. If None, read all the pages.
    Returns:
        A list of lines of text.
    """
    #conversion()
    saveImage()
    imagedata = ImageData("static/2.png")
    removeImage()
    #Sconvertintodataframe()
    #print(imagedata)
    #ConvertIntoImage()
    """pdf = open(pdf, 'rb')
    readPDF = PyPDF2.PdfReader(pdf, strict=False)
    for page_no in range(1,5):
        page=readPDF.pages[page_no]
        print(page)
        print(page["/Resources"]["/XObject"]["/img"+str(page_no)])
        a = ImageData(page["/Resources"]["/XObject"]["/img"+str(page_no)])
        print(a)
        #Extract the text from the page
        lines = page.extract_text()"""

    return imagedata

def removeImage():
    for i in range(1,5):
        os.remove("static/"+str(i)+".png")

def ImageData(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Mukesh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    #print(pytesseract.image_to_string(Image.open('text.jpg')))
    img_data = pytesseract.image_to_string(Image.open(img))
    img_data = img_data[150:620]
    return img_data


def saveImage():
    #Import required dependencies
    import fitz
    import os
    from PIL import Image

    #Define path to PDF file
    file_path = 'address.pdf'

    #Define path for saved images
    images_path = 'static/'

    #Open PDF file
    pdf_file = fitz.open(file_path)

    #Get the number of pages in PDF file
    page_nums = len(pdf_file)

    #Create empty list to store images information
    images_list = []

    #Extract all images information from each page
    for page_num in range(page_nums):
        page_content = pdf_file[page_num]
        images_list.extend(page_content.get_images())

    #Raise error if PDF has no images
    if len(images_list)==0:
        raise ValueError(f'No images found in {file_path}')

    #Save all the extracted images
    for i, img in enumerate(images_list, start=1):
        #Extract the image object number
        xref = img[0]
        #Extract image
        base_image = pdf_file.extract_image(xref)
        #Store image bytes
        image_bytes = base_image['image']
        #Store image extension
        image_ext = base_image['ext']
        #Generate image file name
        image_name = str(i) + '.' + image_ext
        #Save image
        with open(os.path.join(images_path, image_name) , 'wb') as image_file:
            image_file.write(image_bytes)
            image_file.close()


def ConvertIntoCSV():
    import cv2 as cv
    import numpy as np
    filename = 'static/2.png'
    img = cv.imread(cv.samples.findFile(filename))
    cImage = np.copy(img) #image to draw lines
    cv.imshow("image", img) #name the window as "image"
    cv.waitKey(0)
    cv.destroyWindow("image")



def convertintodataframe():
    import pandas as pd
    import numpy as np
    colourImg = Image.open( 'static/2.png')
    colourPixels = colourImg.convert("RGB")
    colourArray = np.array(colourPixels.getdata()).reshape(colourImg.size + (3,))
    indicesArray = np.moveaxis(np.indices(colourImg.size), 0, 2)
    allArray = np.dstack((indicesArray, colourArray)).reshape((-1, 5))
    df = pd.DataFrame(allArray, columns=["y", "x", "red","green","blue"])
    print(df)

def conversion():
    import numpy as np
    import cv2
    import os
    IMG_DIR = 'static'
    for img in os.listdir(IMG_DIR):
            img_array = cv2.imread(os.path.join(IMG_DIR,img), cv2.IMREAD_GRAYSCALE)
            img_array = (img_array.flatten())
            img_array  = img_array.reshape(-1, 1).T
            with open('output.csv', 'ab') as f:
                np.savetxt(f, img_array, delimiter=",")























def pdftotextold(pdf, page=None):
    """Retrieve all text from a PDF file.

    Arguments:
        pdf Path of the file to read.
        page: Number of the page to read. If None, read all the pages.

    Returns:
        A list of lines of text.
    """
    #pdf = open(pdf, 'w')
    #pdf = open("CJ8QXM0IDrEiuJUQWvh9UqIkTvPyg5C8Gn9uKdj-Wk4hSUYIK-_1wyMUcQshPL5DfnNt6UXVmjYxmFUtAIyACdjzc3yr8o668z5cSagnEolR2q3xTi6ga2Ldh4miNDg7.pdf", 'rb')
    pdf = open("address.pdf", 'rb')
    readPDF = PyPDF2.PdfReader(pdf, strict=False)
    for page_no in range(1,5):
        page=readPDF.pages[page_no]
        image = Image.open(page)#new added
        image.save("NewImage.gif")#new_added
        #Extract the text from the page
        lines = page.extract_text()
        img_data = ImageData(page)#new lines added
    """import slate3k as slate
    with open("Nextcloud flyer.pdf",'rb') as f:
        extracted_text = slate.PDF(f)
        print(extracted_text,"extracted_text")
    print("slate3k")"""
    """import fitz
    doc = fitz.open("static/"+pdf)
    text1 = ""
    for page in doc:
        print(page,"page page page")
        text =page.get_text()
        text1+=text
    print(text1,"text text text text")
    print("fitz")"""
    """if page is None:
        args = ['pdftotext', '-layout', '-q', pdf, '-']
    else:
        args = ['pdftotext', '-f', str(page), '-l', str(page), '-layout','-q', pdf, '-']
    try:
        txt = subprocess.check_output(args, universal_newlines=True)
        lines = txt.splitlines()
    except subprocess.CalledProcessError:
        lines = []"""
    return lines