from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException,ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

import json
import numpy as np
import pandas as pd
from time import sleep
from datetime import date

driver = webdriver.Chrome(executable_path='chromedriver-win64\chromedriver.exe')
driver.set_page_load_timeout(20)
driver.maximize_window()

delay = 2
seedlist_competitor = pd.read_excel('Storible-Campaigns/seedlist.xlsx','competitors')
seedlist_client = pd.read_excel('Storible-Campaigns/seedlist.xlsx','clients')
today = date.today()


def waiting_until_full(delay,type):
    try:
        element_present = EC.presence_of_all_elements_located((By.XPATH, type))
        WebDriverWait(driver, delay).until(element_present)
    except TimeoutException:
        pass

#riseatseven

def riseatseven():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'riseatseven' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '//*[@id="gatsby-focus-wrapper"]/main/div[5]/div[4]')
                digital_pr = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/main/div[5]/div[4]')
                lists = digital_pr.find_elements(By.TAG_NAME,'a')
                links = [lists[i].get_attribute('href') for i in range(len(lists))]
                for link in links:
                    driver.get(link)
                    waiting_until_full(delay, '/html/body')
                    sleep(2)
                    names = driver.find_element(By.XPATH,'//*[@id="gatsby-focus-wrapper"]/main/div[1]/div[2]/div[1]/div/div/div/div/h3[2]').text
                    text = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/main/div[3]/div/div[3]/div')
                    total_links_xpath = text.find_elements(By.TAG_NAME, 'a')
                    total_links =  list({total_links_xpath[i].get_attribute('href') for i in range(len(total_links_xpath))})
                    p_date = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/main/div[3]/div/div[1]/div/div[3]/h4').text
                    url = driver.current_url
                    # ex_link = [l for l in total_links if 'weareyard' not in l]
                    links_final = [l for l in total_links if 'riseatseven' not in l]
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links_final, 'Source': url, 'Published Date': p_date}])])
                    sleep(2)

                print("Riseatseven's total campaigns are: {}".format(len(pr_camps)))
                # df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
                # df['source'] = 'riseatseven'
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
            except Exception as e:
                # pr_camps = pd.DataFrame()
                continue
    return pr_camps

#reboot
def reboot():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'reboot' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '/html/body/script[2]')
                json_raw = json.loads(driver.find_element(By.XPATH, '/html/body/script[2]').get_attribute('innerHTML')[15:-1])
                for i in json_raw:
                    for j in range(len(i['list'])):
                        name = i['list'][j]['campaign']['name'].title()
                        link = i['list'][j]['url_link']
                        source = driver.current_url
                        p_date = i['list'][j]['campaign']['start_date']
                # pr_camps = {i['list'][j]['campaign']['name'].title(): i['list'][j]['url_link'] for i in json_raw for j in range(len(i['list']))}
                        pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': name, 'Link': link, 'Source': source, 'Published Date': p_date}])])
                print("Rebootonline's total campaigns are: {}".format(len(pr_camps)))
            except Exception as e:
                print('1')
                # pr_camps = {}
                continue
            # df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
            pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
            pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
            pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
    return pr_camps

#motivepr
def motivepr():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'motivepr' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '/html/body/div[5]')
                sleep(2)
                digital_pr = driver.find_element(By.XPATH, '/html/body/div[5]/div/div')
                lists = digital_pr.find_elements(By.TAG_NAME,'a')
                links = [lists[i].get_attribute('href') for i in range(len(lists))]
                for link in links:
                    driver.get(link)
                    waiting_until_full(delay, '//*[@id="content"]/section[2]')
                    sleep(2)
                    names = driver.find_element(By.TAG_NAME,'h1').text
                    source = driver.current_url
                    p_date = 'unavailable'
                    text = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]')
                    total_links_xpath = text.find_elements(By.TAG_NAME, 'a')
                    total_links =  list({total_links_xpath[i].get_attribute('href') for i in range(len(total_links_xpath))})
                    links_final = [l for l in total_links if 'motivepr' not in l]
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links_final, 'Source': source, 'Published Date': p_date}])])
                    sleep(2)
                driver.back()
                sleep(2)
                print("MotivePR's total campaigns: {}".format(len(pr_camps)))
            except Exception as e:
                continue

    # df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
    # df['source'] = 'motivepr'
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
            # print(df)
    return pr_camps

#dontpanic
def dontpanic():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'dontpanic' in comp_link:
            driver.get(comp_link)
            waiting_until_full(delay, '//*[@id="work_items"]')
            digital_pr = driver.find_element(By.XPATH, '//*[@id="work_items"]')
            camps = [camp.get_attribute('href') for camp in digital_pr.find_elements(By.TAG_NAME, 'a')]
            try:
                for i in camps:
                    driver.get(i)
                    waiting_until_full(delay, '//*[@id="new_page_holder_inner"]/div/div[1]/div[1]')
                    sleep(10)
                    name = driver.find_element(By.TAG_NAME, 'h1').text
                    links = driver.find_element(By.CLASS_NAME,'link').find_element(By.TAG_NAME, 'a').get_attribute('href')
                    source = driver.current_url
                    p_date = 'unavailable'
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': name, 'Link': links, 'Source': source, 'Published Date': p_date}])])
                    driver.back()
                    waiting_until_full(delay, '//*[@id="work_items"]')
                    sleep(10)
            except Exception as e:
                continue
    print("Dontpanic's total campaigns are: {}".format(len(pr_camps)))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
    return pr_camps

#vervesearch
def vervesearch():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'vervesearch' in comp_link:
            driver.get(comp_link)
            waiting_until_full(delay, '/html/body/main/section[1]/div/ul')
            digital_pr = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/ul')
            camps = [camp.get_attribute('href') for camp in digital_pr.find_elements(By.TAG_NAME, 'a')]
            try:
                for camp in camps:
                    names = camp.split('/')[-2].replace('-',' ').title()
                    driver.get(camp)
                    waiting_until_full(delay, '/html/body/main/section[2]/div/a')
                    link = driver.find_elements(By.CLASS_NAME, 'button')[0].get_attribute('href')
                    source = camp
                    p_date = 'unavailable'
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': link, 'Source': source, 'Published Date': p_date}])])
                    driver.back()
                    waiting_until_full(delay, '/html/body/main/section[1]/div/ul')
                    sleep(3)
            except Exception as e:
                continue
    print("Vervesearch's total campaigns are: {}".format(len(pr_camps)))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
    return pr_camps

#neomam
def neomam():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'neomam' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '//*[@id="__layout"]/div/div/div[2]')
                for i in range(10):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                waiting_until_full(delay, '//*[@id="__layout"]/div/div/div[2]')
                sleep(2)
                digital_pr = driver.find_elements(By.LINK_TEXT,'see it live')
                for i, camp in enumerate(digital_pr):
                    camps = camp.get_attribute('href')
                    names = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/div[{}]/div[2]/p[1]/b'.format(i+1)).text
                    source = driver.current_url
                    p_date = 'unavailable'
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': camps, 'Source': source, 'Published Date': p_date}])])
                print("Neomam's total campaigns: {}".format(len(pr_camps)))
            except Exception as e:
                continue

            pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
            pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
            pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
    return pr_camps

#digitaloft
def digitaloft():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])
    
    for comp_link in seedlist_competitor['competitor_link']:
        if 'digitaloft' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '//*[@id="page"]/div[4]/div/div')
                sleep(2)
                digital_pr = driver.find_element(By.XPATH,'//*[@id="page"]/div[4]/div/div')
                camps = digital_pr.find_elements(By.TAG_NAME, 'a')
                links = list({camp.get_attribute('href') for camp in camps})
                names = [link.split('/')[-2].replace('-',' ').title() for link in links]
                pr_camps = {names[i]: links[i] for i in range(len(names))}
                print("Digitaloft's total campaigns: {}".format(len(pr_camps)))
            except Exception as e:
                continue

            df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Link'])
            df['source'] = 'https://digitaloft.co.uk/success-stories/'
            df['Publish Date'] = 'unavailable'
            df['Link'] = df['Link'].map(lambda x: str(x).replace('[',''))
            df['Link'] = df['Link'].map(lambda x: str(x).replace(']',''))
            df['Link'] = df['Link'].map(lambda x: str(x).replace("'",''))
    return df

#weareyard
def weareyard():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for comp_link in seedlist_competitor['competitor_link']:
        if 'weareyard' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '//*[@id="content"]')
                sleep(2)
                digital_pr = driver.find_elements(By.CLASS_NAME, 'casestudy_content')
                links = [digital_pr[i].find_element(By.TAG_NAME,'a').get_attribute('href') for i in range(len(digital_pr))]
                # names = [digital_pr[i].find_element(By.TAG_NAME,'h3').text for i in range(len(digital_pr))]
                for link in links:
                    driver.get(link)
                    waiting_until_full(delay, '//*[@id="content"]/section[2]')
                    sleep(2)
                    names = driver.find_element(By.TAG_NAME,'h1').text
                    text = driver.find_element(By.XPATH, '//*[@id="content"]/section[2]')
                    total_links_xpath = text.find_elements(By.TAG_NAME, 'a')
                    total_links =  list({total_links_xpath[i].get_attribute('href') for i in range(len(total_links_xpath))})
                    # ex_link = [l for l in total_links if 'weareyard' not in l]
                    links_final = [l for l in total_links if 'weareyard' not in l]
                    source = driver.current_url
                    p_date = 'unavailable'
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links_final, 'Source': source, 'Published Date': p_date}])])
                    sleep(2)
                driver.back()
                sleep(2)
                print("Weareyard's total campaigns: {}".format(len(pr_camps)))
            except Exception as e:
                continue

    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
    pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
    return pr_camps

def priceeconomic():
    pass

def fractl():
    pr_camps = {}

    for comp_link in seedlist_competitor['competitor_link']:
        if 'frac' in comp_link:
            try:
                driver.get(comp_link)
                waiting_until_full(delay, '/html/body/section[2]/div')
                sleep(2)
                pr_camps = driver.find_element(By.XPATH,'/html/body/section[2]/div')
                all_links = pr_camps.find_elements(By.TAG_NAME, 'a')
                links = list({link.get_attribute('href') for link in all_links})
                for link in links:
                    driver.get(link)
                    waiting_until_full(delay, '/html/body')
                    sleep(2)
                    names = driver.find_element(By.TAG_NAME,'h1').text
                    text = driver.find_element(By.XPATH, '/html/body')
                    total_links_xpath = text.find_elements(By.TAG_NAME, 'a')
                    total_links =  list({total_links_xpath[i].get_attribute('href') for i in range(len(total_links_xpath))})
                    # ex_link = [l for l in total_links if 'weareyard' not in l]
                    pr_camps[names] = [l for l in total_links if 'frac' not in l]
                    sleep(2)
                driver.back()
                sleep(2)
                print("Fractl's total campaigns: {}".format(len(pr_camps)))
            except Exception as e:
                pr_camps = {}
                continue
    df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
    df['source'] = 'fractl'
    df['Links'] = df['Links'].map(lambda x: str(x).replace('[',''))
    df['Links'] = df['Links'].map(lambda x: str(x).replace(']',''))
    df['Links'] = df['Links'].map(lambda x: str(x).replace("'",''))
    return df

def aria():
    pass

def journeyfurther():
    pass

def jbh():
    pass

# Client

#electronicshub

def electronicshub():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for client_link in seedlist_client['client_link']:
        if 'electronicshub' in client_link:
            try:
                driver.get(client_link)
                waiting_until_full(delay, '/html/body/div[1]/section[2]/div/div[1]')
                digital_pr = driver.find_element(By.XPATH, '/html/body/div/section[2]/div/div[1]/div/div[1]/div')
                a_ids = digital_pr.find_elements(By.TAG_NAME, 'article')
                list_id = [id.get_attribute('id') for id in a_ids]
                lists = digital_pr.find_elements(By.TAG_NAME,'a')
                for i in range(len(lists)):
                    links = driver.find_element(By.XPATH, '//*[@id="{}"]/div/section/div/div[2]/div/div[2]/div/h2/a'.format(list_id[i])).get_attribute('href')
                    names = driver.find_element(By.XPATH, '//*[@id="{}"]/div/section/div/div[2]/div/div[2]/div/h2/a'.format(list_id[i])).text
                    source = driver.current_url
                    p_date = driver.find_element(By.XPATH, '//*[@id="{}"]/div/section/div/div[2]/div/div[4]/div/ul/li/span'.format(list_id[i])).text
                    pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links, 'Source': source, 'Published Date': p_date}])])
                print("electronicshub's total campaigns are: {}".format(len(pr_camps)))
                # df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
                # df['source'] = 'https://www.electronicshub.org/insights/'
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
                # pr_camps = pr_camps.iloc[2:,:]
            except Exception as e:
                continue 
    return pr_camps

#budgetdirect

def budgetdirect():
    pr_camps = {}

    for client_link in seedlist_client['client_link']:
        if 'budgetdirect' in client_link:
            try:
                main_links = ['https://www.budgetdirect.com.au/car-insurance/articles.html', 'https://www.budgetdirect.com.au/travel-insurance/articles.html',
                        'https://www.budgetdirect.com.au/home-contents-insurance/articles.html', 'https://www.budgetdirect.com.au/life-insurance/articles.html']
                for main_link in main_links:
                    driver.get(main_link)
                    waiting_until_full(delay, '/html/body/div[4]/div[2]/div/div/div/div/div/div/div/div/div')
                    digital_pr = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div')
                    lists = digital_pr.find_elements(By.TAG_NAME,'a')
                    links = [link.get_attribute('href') for link in lists if link.get_attribute('class') == 'column__link']                  
                    texts = digital_pr.find_elements(By.TAG_NAME, 'h3')
                    names = [text.text for text in texts]
                    pr_camps = {names[i]: links[i] for i in range(len(links))}
                    print("budgetdirect's total campaigns are: {}".format(len(pr_camps)))
                    df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Link'])
            except Exception as e:
                continue
    df['Source'] = 'https://www.budgetdirect.com.au/'
    df['Published Date'] = 'unavailable'
    df['Link'] = '[]'
    df['Link'] = df['Link'].map(lambda x: str(x).replace('[',''))
    df['Link'] = df['Link'].map(lambda x: str(x).replace(']',''))
    df['Link'] = df['Link'].map(lambda x: str(x).replace("'",''))
    return df

#businessbacker

def businessbacker():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for client_link in seedlist_client['client_link']:
        if 'businessbacker' in client_link:
            try:
                for i in range(1,22):
                    driver.get(client_link + 'page/{}/'.format(i))
                    waiting_until_full(delay, '/html/body/div[2]/main/section[4]/div/div[1]/div[1]/div')
                    sleep(5)
                    digital_pr = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[4]/div/div[1]/div[1]/div')
                    source = driver.current_url
                    for j in range(1,11):
                        links = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[4]/div/div[1]/div[1]/div/div[{}]/div/p/a'.format(j)).get_attribute('href')
                        names = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[4]/div/div[1]/div[1]/div/div[{}]/div/p/a'.format(j)).text
                        p_date =  driver.find_element(By.XPATH, '/html/body/div[2]/main/section[4]/div/div[1]/div[1]/div/div[{}]/div/time'.format(j)).text
                        pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links, 'Source': source, 'Published Date': p_date}])])
                    # main_df = main_df.append(df, ignore_index=True)
                print("businessbacker's total campaigns are: {}".format(len(pr_camps)))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
            except Exception as e:
                continue
    return  pr_camps

def expedia():
    pr_camps = {}
    c = 0
    for client_link in seedlist_client['client_link']:
        if 'expedia' in client_link:
            try:
                driver.get(client_link)
                waiting_until_full(delay, '//*[@id="ag-main"]/div/div[4]')
                digital_pr = driver.find_element(By.XPATH, '//*[@id="ag-main"]/div/div[4]')
                button = digital_pr.find_element(By.XPATH, '//*[@id="ag-main"]/div/div[4]/button')
                while c <= 20:
                    button.click()
                    sleep(delay)
                    c += 1
                lists = digital_pr.find_elements(By.TAG_NAME,'a')
                links = [link.get_attribute('href') for link in lists]
                texts = digital_pr.find_elements(By.CLASS_NAME, 'ag-archive-post-title')
                names = [text.text for text in texts]
                pr_camps = {names[i]: links[i] for i in range(len(links))}
                print("expedia's total campaigns are: {}".format(len(pr_camps)))
                df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
                df['source'] = 'expedia'
                df['Links'] = df['Links'].map(lambda x: str(x).replace('[',''))
                df['Links'] = df['Links'].map(lambda x: str(x).replace(']',''))
                df['Links'] = df['Links'].map(lambda x: str(x).replace("'",''))
            except Exception as e:
                df = pd.DataFrame()
                continue

    return df

#homes

def homes():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])

    for client_link in seedlist_client['client_link']:
        if 'homes.com' in client_link:
            try:
                for i in range(1,21):
                    driver.get(client_link + 'page/{}/'.format(i))
                    waiting_until_full(delay, '//*[@id="primary"]/div[2]/div')
                    sleep(5)
                    posts = driver.find_elements(By.TAG_NAME, 'article')
                    post_ids = [id.get_attribute('id') for id in posts]
                    source = driver.current_url
                    for post in post_ids:
                        links = driver.find_element(By.XPATH, '//*[@id="{}"]/div/div[1]/a'.format(post)).get_attribute('href')
                        names = driver.find_element(By.XPATH, '//*[@id="{}"]/div/div[1]/a/h2'.format(post)).text
                        p_date = driver.find_element(By.XPATH, '//*[@id="{}"]/div/div[2]/span[2]'.format(post)).text
                        pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links, 'Source': source, 'Published Date': p_date}])])
                    # main_df = main_df.append(df, ignore_index=True)
                print("homes's total campaigns are: {}".format(len(pr_camps)))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
            except Exception as e:
                continue
    return  pr_camps

#surfshark

def surfshark():
    pr_camps = pd.DataFrame(columns=['Name', 'Link', 'Source', 'Published Date'])
    for client_link in seedlist_client['client_link']:
        if 'surfshark' in client_link:
            try:
                for i in range(1,6):
                    if i == 1:
                        driver.get(client_link)
                        waiting_until_full(delay, '//*[@id="__next"]/div/main/div[2]/div[2]/div')
                        sleep(5)
                        source = driver.current_url
                        for j in range(1,7):
                            names = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div/div[{}]/a/div/h3'.format(j)).text                                   
                            links = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div/div[{}]/a'.format(j)).get_attribute('href')
                            p_date = 'unavailable'
                            pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links, 'Source': source, 'Published Date': p_date}])])
                    else:
                        driver.get(client_link + '/{}'.format(i))
                        waiting_until_full(delay, '//*[@id="__next"]/div/main/div[2]/div/div')
                        sleep(5)
                        for j in range(1,7):
                            names = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div/div/div[{}]/a/div/h3'.format(j)).text
                            links = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div/div/div[{}]/a'.format(j)).get_attribute('href')
                            p_date = 'unavailable'
                            pr_camps = pd.concat([pr_camps, pd.DataFrame.from_records([{'Name': names, 'Link': links, 'Source': source, 'Published Date': p_date}])])
                    waiting_until_full(delay, '//*[@id="__next"]/div/main/div[2]/div[2]/div')
                    sleep(5)

                    # main_df = main_df.append(df, ignore_index=True)
                print("surfshark's total campaigns are: {}".format(len(pr_camps)))
                pr_camps['source'] = 'surfshark'
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace('[',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace(']',''))
                pr_camps['Link'] = pr_camps['Link'].map(lambda x: str(x).replace("'",''))
            except Exception as e:
                continue
    return  pr_camps

#stltraining

def stltraining():
    pr_camps = {}
    for client_link in seedlist_client['client_link']:
        if 'stl-training' in client_link:
            try:
                driver.get(client_link)
                waiting_until_full(delay, '//*[@id="beststl_maincontent"]/div[2]/section/div')
                digital_pr = driver.find_element(By.XPATH, '//*[@id="beststl_maincontent"]/div[2]/section/div')
                lists = digital_pr.find_elements(By.TAG_NAME,'a')
                links = list({lists[i].get_attribute('href') for i in range(len(lists))})
                names = [lists[i].text for i in range(len(lists)) if lists[i].text != '']
                pr_camps = {names[i]: links[i] for i in range(len(links))}
                print("stltraining's total campaigns are: {}".format(len(pr_camps)))
                df = pd.DataFrame(list(pr_camps.items()),columns=['Name','Links'])
                df['Source'] = 'https://www.stl-training.co.uk/sharing/'
                df['Published Date'] = 'unavailable'
                df['Link'] = df['Link'].map(lambda x: str(x).replace('[',''))
                df['Link'] = df['Link'].map(lambda x: str(x).replace(']',''))
                df['Link'] = df['Link'].map(lambda x: str(x).replace("'",''))
                df = df.iloc[2:,:]
            except Exception as e:
                continue 
    return df

def main():
    riseatseven_ds = riseatseven()
    reboot_ds = reboot()
    motivepr_ds = motivepr()
    dontpanic_ds = dontpanic()
    vervesearch_ds = vervesearch()
    neomam_ds = neomam()
    digitaloft_ds = digitaloft()
    weareyard_ds = weareyard()
    
    electronicshub_ds = electronicshub()
    budgetdirect_ds = budgetdirect()
    businessbacker_ds = businessbacker()
    expedia_ds = expedia()
    homes_ds = homes()
    surfshark_ds = surfshark()
    # stltraining_ds = stltraining()
    final = pd.concat([riseatseven_ds, reboot_ds, motivepr_ds, dontpanic_ds, vervesearch_ds, neomam_ds, digitaloft_ds, weareyard_ds, electronicshub_ds,
                            budgetdirect_ds, businessbacker_ds, expedia_ds, homes_ds, surfshark_ds],ignore_index=True)
    final['last_update_date'] = today.strftime('%d/%m/%Y')
    # df = pd.DataFrame(list(final.items()),columns=['Name','Links'])
    final.to_excel('digital_campaigns.xlsx')
    final = pd.read_excel('digital_campaigns.xlsx')
    final.drop(columns=final.columns[0], axis=1,  inplace=True)
    final.to_excel('digital_campaigns.xlsx')

if __name__ == "__main__":
    main()