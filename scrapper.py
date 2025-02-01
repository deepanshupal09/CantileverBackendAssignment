import requests
import json
import os
import time 
from selenium.webdriver.common.by import By
from tqdm import tqdm
from collections import defaultdict
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from inscriptis import get_text
from newspaper import fulltext
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

def extract_job_ids(html_soup):
    str_soup = str(html_soup)
    split_list = str_soup.split('jobKey')[1:]
    job_key_location = {}
    for value in split_list:
        key = value[3: value.find('\",')]
        location = value.split('location')[1][3: value.split('location')[1].find('\",')]
        job_key_location[key] = location

    return job_key_location


def fetch_job_description(job_key):
    
#     url = "https://apis.indeed.com/graphql?co=US"
    url = "https://www.indeed.com/cmp/-/rpc/fetch-jobs?jobKey={}"
    driver = webdriver.Chrome()
    driver.get(url.format(job_key))
    html_source = driver.page_source
    driver.close()
    
    soup = BeautifulSoup(html_source, features='html.parser')
    
    job_data = json.loads(soup.text)

    return job_data


def write_jds(path, jd_content):
    
    with open(path, 'w') as f:
        f.write(jd_content)

def extract_jds(company_jobs_url, company, company_code, jd_limit):
    try:
#         processed_paths = {}
        for offset in range(0, jd_limit, 100):
            driver = webdriver.Chrome()
            driver.get(company_jobs_url.format(company, offset))
            html_source = driver.page_source
            driver.close()

            soup = BeautifulSoup(html_source, features='html.parser')

            # fetch jobs key and location list
            job_key_location = extract_job_ids(soup)

            # fetch job description
            for key in tqdm(job_key_location):

                job_resp = fetch_job_description(key)
#                 print(job_resp)
                job_details = job_resp['jobData']['results'][0]['job']
                job_title = job_details['title'].replace('/', '-')
                job_department = company.replace('/', '-')
                job_location = job_key_location[key].replace('/', '-')
                job_description_html = job_details['description']['html']
                try:
                    job_description_text = get_text(job_description_html)
                except:
                    try:
                        job_description_text = fulltext(job_description_html)
                    except:
                        try:
                            job_description_text = BeautifulSoup(job_description_html, features='html.parser').text
                        except:
                            job_description_text = job_description_html
                            print('HTML Written', job_title, job_department, job_location)

                company_folder = company_code + '' + 'Job Description' + '' + 'July2023Batch01/'

                # create directory
                os.makedirs(os.path.dirname('JDs/' + company_folder), exist_ok=True)

                file_path = company_folder + job_title + '' + job_department + '' + job_location + '.txt'
                
#                 if file_path not in processed_paths.keys():
#                     processed_paths[file_path] = 1
#                 else:
#                     old_file_path = file_path
#                     file_path = file_path[:-4] + '_' + str(processed_paths[file_path]) + '.txt'
#                     processed_paths[old_file_path] += 1

                write_jds(file_path, job_description_text)
    
    except Exception as err:
            print('Error', err)

# companies_df = pd.read_csv('companies.csv')

# for idx in range(len(companies_df)):
try:
    company = 'kfc-uk'
    company_code = 'kfc-uk'
    offset = 0
    jd_limit = 600
    company_jobs_url = 'https://harri.com/internal/{}'
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(company_jobs_url.format(company))
    try:
        wait = WebDriverWait(driver, 10)
        print("waiting")
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[4]/button')))
        close_button.click()
        # button = driver.find_element(By.xpath('//*[@id="harriApp"]/div[1]/div/div[1]/div[4]/button'))
        # print(button)
        # button.click()
        print('dropdown clicked')
    except:
        print("no dropdown clicked")
        pass
    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     # print("*")
    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    
    max_scroll_attempts = 50
    scroll_attempts = 0
    
    while scroll_attempts < max_scroll_attempts:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
    
        if new_height == last_height:
            break
        
        last_height = new_height
        scroll_attempts += 1
    # dropdown = ""
    # destination_page_link = driver.find_element_by_xpath(dropdown)
    # destination_page_link.click()
    wait = WebDriverWait(driver, 90)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, features='html.parser')
    # print("try to find btn")
    
    # print("apply found")
    # jobContainer=soup.find_all('div',{'class':'job-with-data'})
    i=0
    # length=len(jobContainer)
    # for i in range(length):
    applyBtn=soup.find_all('div',{'class':'btn apply-mode-btn large-btn'})
    j=0
    # for j in range(len(applyBtn)):
        # print("inside to find a")
    links = soup.find_all('a',{'class':'job-item-ref'})
    for link in links:
        href = link.get('href')  # Get the 'href' attribute of the <a> tag
        goto = "https://harri.com/"+href
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(goto)
        wait = WebDriverWait(driver, 20)
        print("waiting")
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fancybox-wrap"]/div/a')))
        close_button.click()
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, features='html.parser')
        jds=soup.find('div',{'class':'bio-details ng-scope'})
        # title=soup.find('div',{'class':'info-box d-none d-sm-block'})
        # heading=title.text
        text=jds.text
        print("about to close browser")
        driver.close()
        print("closed browser")
        cleaned_jd = text.replace('\xa0', ' ').replace('\n', ' ')
        file_path = 'jds/' + company + '/' + str(i) + '.txt'
        write_jds(file_path, cleaned_jd)
        cleaned_jd=''
        i+=1
    # len(applyBtn)
    driver.close()

except Exception as err:
    print('Error')