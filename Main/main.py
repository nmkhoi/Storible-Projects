from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import pandas as pd
import numpy as np
import io
import time
import datetime
import csv
import re

hashtag_pattern = r'#\S+'
username_pattern = r'@\S+'
url_pattern = r'http.+?(?="|<)'

def scrolling():
    SCROLL_PAUSE_TIME = 0.5

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

def scrape_google_new(query,no_of_records,time_query):

    def time_setting(index):

        tools = driver.find_element(by=By.XPATH, value='//*[@id="uddia_1"]/div')
        tools.click()
        time.sleep(3)

        dropdown = driver.find_elements(by=By.CLASS_NAME, value='KTBKoe')
        time_choice = [i for i in dropdown if i.text == 'Gần đây']
        time_option = time_choice[0]
        time_option.click()
        time.sleep(3)

        menu = driver.find_element(by=By.XPATH, value='//*[@id="lb"]/div/g-menu')
        item = menu.find_elements(by=By.TAG_NAME, value='g-menu-item')
        item[int(index)].click()
        time.sleep(5)

    options = webdriver.ChromeOptions()
    options.add_argument("--lang=vi")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="114.0.5735.16").install(),options=options)
    driver.set_page_load_timeout(20)

    driver.get('https://www.google.com.vn/')
    time.sleep(5)
    
    search = driver.find_elements(by=By.TAG_NAME, value='textarea')[0]
    search.send_keys(str(query))
    # search.submit()
    time.sleep(5)

    news = driver.find_element(by=By.LINK_TEXT, value='Tin tức')
    news.click()
    time.sleep(5)

    # dropdown = ['Anytime','Past hour','Past 24 hours','Past week','Past month','Past year']
    if time_query == 'Past hour': # 1
        time_setting(1)
    elif time_query == 'Past 24 hours': # 2
        time_setting(2)
    elif time_query == 'Past week': # 3
        time_setting(3)
    elif time_query == 'Past month': # 4
        time_setting(4)
    elif time_query == 'Past year': # 5
        time_setting(5)


    final_data = pd.DataFrame(columns=['headline','link'])
    try:
        # for i in range(1,no_of_records+1):
        i = 0
        while len(final_data) <= no_of_records:
            i += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            table = driver.find_element(by=By.TAG_NAME, value='table')
            page = table.find_elements(by=By.TAG_NAME, value='td')
            page[i].click()
            time.sleep(3)

            links = driver.find_elements(by=By.CLASS_NAME, value='SoaBEf')
            for link in links:
                url = link.find_elements(by=By.TAG_NAME, value='a')[0].get_attribute('href')
                headline = link.find_elements(by=By.TAG_NAME, value='div')[1].text.split('\n')[1].title()

                final_data = pd.concat([final_data, pd.DataFrame.from_records([{
                    'headline':headline,
                    'link':url
                    }])])
    except Exception as e:
        pass
    return final_data.head(no_of_records)

def scrape_tweet(query, no_of_tweets, email, password, username):

    global driver

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_page_load_timeout(20)
    driver.maximize_window()

    driver.get('https://twitter.com/i/flow/login')
    time.sleep(3)

    email_holder = driver.find_element(by=By.TAG_NAME, value='input')
    email_holder.send_keys(email)
    time.sleep(3)

    next_button = driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span')
    next_button.click()
    time.sleep(3)

    username_holder = driver.find_element(by=By.TAG_NAME, value='input') 
    username_holder.send_keys(username)
    time.sleep(3)

    next_button = driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
    next_button.click()
    time.sleep(3)

    password_holder = driver.find_elements(by=By.TAG_NAME, value='input')[1]
    password_holder.send_keys(password)
    time.sleep(3)

    login_button = driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span')
    login_button.click()
    time.sleep(5)

    # search_box = [i for i in driver.find_elements(by=By.TAG_NAME, value='input') if i.get_attribute('placeholder') == 'Search Twitter'][0]
    query = query.replace('#','%23')
    if query[0] == '@':
        url_query = 'https://twitter.com/{}'.format(query[1:])
    else:
        query = query.replace('@','%40')
        url_query = 'https://twitter.com/search?q={}&src=typed_query'.format(query)

    driver.get(url_query)
    time.sleep(10)

    final_data = pd.DataFrame(columns=['username','text','date','hashtag','external_links','reply_count','retweet_count','like_count','mention_users'])
    while len(final_data) <= no_of_tweets:
        articles = driver.find_elements(by=By.TAG_NAME, value='article')
        for article in articles:
            try:
                username = re.findall(username_pattern,[i.text for i in article.find_elements(by=By.TAG_NAME, value='div') if i.get_attribute('data-testid') == 'User-Name'][0])[0]
                text = [i.text for i in article.find_elements(by=By.TAG_NAME, value='div') if i.get_attribute('data-testid') == 'tweetText'][0]
                date = article.find_element(by=By.TAG_NAME, value='time').get_attribute('datetime')
                date = date[:date.find('T')]
                hashtag = re.findall(hashtag_pattern,text)
                external_links = re.findall(url_pattern,article.text)
                reply_count = [i.text for i in article.find_elements(by=By.TAG_NAME, value='div') if i.get_attribute('data-testid') == 'reply'][0]
                retweet_count = [i.text for i in article.find_elements(by=By.TAG_NAME, value='div') if i.get_attribute('data-testid') == 'retweet'][0]
                like_count = [i.text for i in article.find_elements(by=By.TAG_NAME, value='div') if i.get_attribute('data-testid') == 'like'][0]
                mention_users = re.findall(username_pattern,text)

                final_data = pd.concat([final_data, pd.DataFrame.from_records([{
                    'username':username,
                    'text':text,
                    'date':date,
                    'hashtag':hashtag,
                    'external_links':external_links,
                    'reply_count':reply_count,
                    'retweet_count':retweet_count,
                    'like_count':like_count,
                    'mention_users':mention_users
                    }])])
                time.sleep(2)
                # print(final_data)
            except Exception as e:
                continue
        
        # final_data.loc[final_data.astype(str).drop_duplicates().index]
        scrolling()
        time.sleep(5)
    driver.quit()
    return final_data.head(no_of_tweets)

class Twitter_Window:

    def __init__(self, master):
        
        master.title('Scrapper')
        master.resizable(False, False)
        master.configure(background = '#e1d8b9')
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background = '#e1d8b9')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))      

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        
        self.logo = PhotoImage(file = 'logo.png')
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = 'Social Media Scrapping', style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, wraplength = 300,
                  text = ("Chỗ này sẽ note cái dì đó (User Manual chẳng hạn)")).grid(row = 1, column = 1)
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text = 'Number of Records:').grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'File Name:').grid(row = 0, column = 1, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Email:').grid(row = 2, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Password:').grid(row = 2, column = 1, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Username:').grid(row = 4, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Query:').grid(row = 6, column = 0, padx = 5, sticky = 'sw')
        
        self.entry_records = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_filename = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_email = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_password = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_username = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.text_query = Text(self.frame_content, width = 50, height = 15, font = ('Arial', 10))
        
        self.entry_records.grid(row = 1, column = 0, padx = 5)
        self.entry_filename.grid(row = 1, column = 1, padx = 5)
        self.entry_email.grid(row = 3, column = 0, padx = 5)
        self.entry_password.grid(row = 3, column = 1, padx = 5)
        self.entry_username.grid(row = 5, column = 0, padx = 5)
        self.text_query.grid(row = 7, column = 0, columnspan = 2, padx = 5)
        
        ttk.Button(self.frame_content, text = 'Submit',
                   command = self.submit).grid(row = 8, column = 0, padx = 5, pady = 5, sticky = 'e')
        ttk.Button(self.frame_content, text = 'Clear',
                   command = self.clear).grid(row = 8, column = 1, padx = 5, pady = 5, sticky = 'w')

    def submit(self):
        no_of_tweets = int(self.entry_records.get())
        filename = self.entry_filename.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        username = self.entry_username.get()
        query = self.text_query.get(1.0,'end')
        self.clear()
        df = scrape_tweet(query=query, no_of_tweets=no_of_tweets, filename=filename, email=email, password=password, username=username)
        df.to_excel('{}.xlsx'.format(filename))
        # messagebox.showinfo(title = 'Explore California Feedback', message = 'Comments Submitted!')
    
    def clear(self):
        self.entry_records.delete(0, 'end')
        self.entry_filename.delete(0, 'end')
        self.text_query.delete(1.0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_username.delete(0, 'end')

class Google_Window:

    def __init__(self, master):

        # keep `root` in `self.master`
        
        master.title('Scrapper')
        master.resizable(False, False)
        master.configure(background = '#e1d8b9')
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background = '#e1d8b9')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))      

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        
        self.logo = PhotoImage(file = 'logo.png',master=master)
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = 'Social Media Scrapping', style = 'Header.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, wraplength = 300,
                  text = ("Chỗ này sẽ note cái dì đó (User Manual chẳng hạn)")).grid(row = 1, column = 1)
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        dropdown = ['Anytime','Past hour','Past 24 hours','Past week','Past month','Past year']
        self.variable = StringVar()
        self.variable.set(dropdown[0])

        ttk.Label(self.frame_content, text = 'Number of Records:').grid(row = 0, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'File Name:').grid(row = 0, column = 1, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Time:').grid(row = 2, column = 0, padx = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Query:').grid(row = 4, column = 0, padx = 5, sticky = 'sw')
        
        self.entry_records = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_filename = ttk.Entry(self.frame_content, width = 24, font = ('Arial', 10))
        self.entry_time = ttk.OptionMenu(self.frame_content,self.variable,*dropdown)
        self.text_query = Text(self.frame_content, width = 50, height = 15, font = ('Arial', 10))
        
        self.entry_records.grid(row = 1, column = 0, padx = 5)
        self.entry_filename.grid(row = 1, column = 1, padx = 5)
        self.entry_time.grid(row = 3, column = 0, padx = 5)
        self.entry_time.config(width=24)
        self.text_query.grid(row = 5, column = 0, columnspan = 2, padx = 5)
        
        ttk.Button(self.frame_content, text = 'Submit',
                   command = self.submit).grid(row = 6, column = 0, padx = 5, pady = 5, sticky = 'e')
        ttk.Button(self.frame_content, text = 'Clear',
                   command = self.clear).grid(row = 6, column = 1, padx = 5, pady = 5, sticky = 'w')

    def submit(self):
        no_of_records = int(self.entry_records.get())
        filename = self.entry_filename.get()
        time_query = self.variable.get()
        # print(time_query)
        query = self.text_query.get(1.0,'end')
        self.clear()
        df = scrape_google_new(query=query, no_of_records=no_of_records, time_query=time_query)
        df.to_excel('{}.xlsx'.format(filename))
        # messagebox.showinfo(title = 'Explore California Feedback', message = 'Comments Submitted!')
    
    def clear(self):
        self.entry_records.delete(0, 'end')
        self.entry_filename.delete(0, 'end')
        self.text_query.delete(1.0, 'end')

class Option_Window:

    def __init__(self, master):

        # keep `root` in `self.master`
        self.master = master

        self.frame_header = Frame(master)
        self.frame_header.pack()

        self.logo = PhotoImage(file = 'logo.png',master=master)
        Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        Label(self.frame_header, text = 'Social Media Scrapping').grid(row = 0, column = 1)
        Label(self.frame_header, wraplength = 300,
                  text = ("Chỗ này sẽ note cái dì đó (User Manual chẳng hạn)")).grid(row = 1, column = 1)

        self.button1 = Button(self.master, text="Twitter", command=self.load_twitter)
        self.button1.pack(side=LEFT)

        self.button2 = Button(self.master, text="Google News", command=self.load_google)
        self.button2.pack(side=RIGHT)

    def load_twitter(self):
        self.button2.destroy()
        self.button1.destroy()
        self.frame_header.destroy()

        # use `root` with another class
        self.another = Twitter_Window(self.master)

    def load_google(self):
        self.button2.destroy()
        self.button1.destroy()
        self.frame_header.destroy()

        # use `root` with another class
        self.another = Google_Window(self.master)

def main():    
    
    root = Tk()
    run = Option_Window(root)
    root.mainloop()
    
if __name__ == "__main__": main()