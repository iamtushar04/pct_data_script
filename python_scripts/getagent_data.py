import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
from pathlib import Path
import pandas as pd
import xlrd  
import csv 
import pdfquery
from commonfunction import pdftotext
from selenium.webdriver.support.ui import Select
# from django.http import HttpResponse
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium.webdriver.chrome.options import Options


pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 500)

def ScrapData():
    try:    
        #Get Path fo the download folder
        #path_to_download_folder = str(os.path.join(Path.home(), "Downloads\resultList.xls"))
        #from commonfunction import DownloadFile
        #DownloadFile(dest_folder="address.pdf",url="https://patentscope.wipo.int/search/docs2/pct/WO2023092159/pdf/zZaC_K0XYHCisk9tVweBnt1dannQ4KCbIrbESLLgM94L0zIdHwCHhywJTWVg8kxSQFhSAaNLV6wGAnz1LNR2rGWn3u0fAMJW2nRt_QfdVubuo4oaGpr4AcOxvIaj2PfB?docId=id00000073060193")
        #pdftext = pdftotext("address.pdf", page=None)
        #ImageData("address.pdf")

        options = Options()
        # proxy_server_url = "127.0.0.53"
        # options.add_argument(f'--proxy-server={proxy_server_url}')
        #Initialize the URL for the scraping
        url = "https://patentscope.wipo.int/search/en/resultWeeklyBrowse.jsf" 

        # get and install deriver 
        #req_proxy = RequestProxy()
        #print(req_proxy,"req_proxy req_proxy req_proxy req_proxy req_proxy")
        #proxies = req_proxy.get_proxy_list()
        #print(proxies,"proxies proxies proxies proxies proxies")
        #PROXY = proxies[0].get_address()
        #print(PROXY,"PROXY PROXY PROXY PROXY PROXY")
        #webdriver.DesiredCapabilities.CHROME['proxy']={"httpProxy":PROXY,"ftpProxy":PROXY,"sslProxy":PROXY,"proxyType":"MANUAL",}
        driver =  webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

        # Open the above url on the browser
        driver.get(url)

        # Maximize the window
        driver.maximize_window()

        #Sleep is using for the take time for load page and its content
        time.sleep(15)

        #Select the option form the drop down
        #driver.find_element(By.ID,"formMainMenu:browseByWeek").click()
        
        #Put the date here for the selecting
        time.sleep(10)
        select = Select(driver.find_element(By.ID,'weeklyPublicationForm:currGazette:input'))

        #To enter date to select the daterange
        select.select_by_visible_text('35/2023 (31.08.2023)')

        import pdb;pdb.set_trace()
        # driver.find_element(By.PARTIAL_LINK_TEXT, rc).click()
        # driver.find_element(By.PARTIAL_LINK_TEXT, "Excel Download").click()
        #download the excel file
        #driver.find_element(By.ID,"weeklyPublicationForm:j_idt1221").click()#Excel Download
        #driver.find_element(By.PARTIAL_LINK_TEXT,"Excel Download").click()


        # wait till the file downloaded compeletly
        time.sleep(15)

        #Check the page source using deriver
        html = driver.page_source

        #Parse the html source using beautiful soup library
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(15)

        #Remove the row 1 and 2 using indexing

        # check and read downloaded file from the download folder
        downloads_path = r"C:\\Users\\Software\\Downloads\\resultList.xls"
        data = pd.read_excel(downloads_path)
        data = data.rename(columns=data.iloc[1])[2:].drop_duplicates(subset=['Applicant'], keep='first').reset_index(drop=True)

        #Remove the row 1 and 2 using indexing
        #data.drop(data.index[0])
        #data.drop(data.index[0])

        #Drop the duplicate data from the pandas dataframe
        # data.drop_duplicates(subset=['Applicant'], keep='first', inplace=True)

        #wb = xlrd.open_workbook(downloads_path) 
        #sheet = wb.sheet_by_index(0)

        #Below for loop is used to get data from the updated dataframe
        csvfile = open('Reports.csv', 'w')
        writer = csv.writer(csvfile)#, delimiter = ' ')
        #response = HttpResponse(content_type="text/csv",headers={"Content-Disposition": 'attachment; filename="Reports.csv"'},)
        #writer = csv.writer(response)
        writer.writerow(["ID","Title", "Appl.No", "IPC","Applicant","Publication Date","Priority Data","Priority Date","Agent Details"])
        for row in range(0,len(data)):

            # Get Id from the pandas dataframe
            rc,title,application_numer,ipc,applicant = data.iloc[row]["ID"],data.iloc[row]["Title"],data.iloc[row]["Appl.No"],data.iloc[row]["IPC"],data.iloc[row]["Applicant"]
            import pdb;pdb.set_trace()
            # Add id to search
            #driver.find_element(By.ID,"weeklyPublicationForm:resultTable:j_idt1225:filter").send_keys(rc)#
            driver.find_element(By.CLASS_NAME,"ui-column-filter").send_keys(rc)
            time.sleep(5)

            #click on id after searching id and wait till the data is loading from the server
            driver.find_element(By.PARTIAL_LINK_TEXT,rc).click()
            time.sleep(15)

            #driver.find_element(By.ID,"weeklyPublicationForm:resultTable:0:woLink").click()
            
            element1 = driver.find_elements(By.CLASS_NAME,"ui-corner-top")
            publication_date,priority_data,agent_details,priority_date = "","","",""
            publication_date = driver.find_elements(By.CLASS_NAME,"ps-biblio-data")
            #mydata = driver.find_element(By.ID,"detailMainForm:MyTabViewId:j_idt5673:j_idt6080")
            #print(mydata)
            for pubdate in publication_date:
                data_list = pubdate.text.split("\n")
                new_list = dict(zip(*[iter(data_list)]*2))
                #print(pubdate.text)
                try:
                    try:
                        publication_date =new_list["Publication Date"]
                    except:
                        pass
                    try:
                        priority_data =new_list["Priority Data"]
                        if priority_data != None:
                            priority_date = priority_data.split()
                            priority_date = priority_date[2]
                    except:
                        pass
                    try:
                        agent_details =new_list["Agents"]
                    except:
                        pass
                except Exception as e:
                    print(e)
            for j in element1:
                time.sleep(10)
                if j.text == "Documents":
                    driver.find_element(By.PARTIAL_LINK_TEXT,"Documents").click()
                    time.sleep(1)       
            try:
                fitd = driver.find_elements(By.CLASS_NAME,"ps-downloadables")#.click()
                k = 0
                for hre in fitd:
                    if k == 84:
                        from commonfunction import DownloadFile
                        DownloadFile(dest_folder="address.pdf",url=hre.get_attribute('href'))
                    k+=1
                try:
                    #pdf_path = r"address.pdf"
                    #pdf = pdfquery.PDFQuery(pdf_path)
                    #pdf.load()
                    
                    #Extract 
                    pdftext = pdftotext("address.pdf", page=None)
                    agent_details+=pdftext

                except Exception as e:
                    print("error e =",e)
                #text_elements = pdf.pq('LTTextLineHorizontal:in_bbox("68.0, 150.57, 101.990, 234.893")').text()#[Left, Bottom, Right, Top]
                #print(text_elements)

                #Write CSV file
                writer.writerow([rc,title, application_numer, ipc,applicant,publication_date,priority_data,priority_date,agent_details])
                time.sleep(10)

                #Closing the webdriver
                driver.close()

                #Performing the same action with new data
                url = "https://patentscope.wipo.int/search/en/resultWeeklyBrowse.jsf"
                driver =  webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver.get(url)
                driver.maximize_window()
                time.sleep(10)
            except Exception as e:
                print("error   ",e)
        
        time.sleep(20)
        # closing the webdriver
        driver.close() 
    except Exception as e:
        print(e)
        # closing the webdriver
        #driver.close()


    
if __name__ == "__main__":
    ScrapData()