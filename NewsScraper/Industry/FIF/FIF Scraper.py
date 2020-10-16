import datetime
import os
import pandas as pd
import re
import shelve
import time
import datetime
# libraries to crawl websites
from bs4 import BeautifulSoup
from selenium import webdriver
from pynput.mouse import Button, Controller
from unicodedata import normalize

path = '/Users/zhoujiawang/Desktop/Brandeis Life/2020 Fall/Field Project/NewsScraper'
os.chdir(path)
driver = webdriver.Chrome(executable_path='/Users/zhoujiawang/Desktop/Brandeis Life/2020 Fall/Field Project/NewsScraper/chromedriver')

link_head = 'https://fif.com/index.php/news-events/fif-news?start='
page_index = [5*i for i in range(133)]
#We need furthur Inspection on that, when to stop?

FIF_NewsMaster = []

for index in page_index:
    links_to_scrape = link_head + str(index)
    driver.get(links_to_scrape)
    # Finding all the news in the website and bringing them to python
    news = driver.find_elements_by_xpath("//article[@class='uk-article tm-article']")
    for r in range(len(news)):
        one_news = {}
        one_news['website name'] = 'Financial Information Forum'
        soup = BeautifulSoup(news[r].get_attribute('innerHTML'))
        try:
            one_news_title_text = soup.find('a').get('title')
        except:
            one_news_title_text = ""
        one_news['headline'] = one_news_title_text

        try:
            one_news_link = 'fif.com' + soup.find('a').get('href')
        except:
            one_news_link = ""
        one_news['link'] = one_news_link

        try:
            openparagraph_raw = soup.find('div',attrs={'class':'tm-article'}).get_text(strip=True)
            one_news_openparagraph = openparagraph_raw.replace('\n','')
            normalize('NFKD', one_news_openparagraph)
        except:
            one_news_openparagraph = ""
        one_news['open paragraph'] = one_news_openparagraph

        try:
            time_raw = soup.find(text = re.compile('^POSTED')).replace('POSTED ','')
            time_dt = datetime.datetime.strptime(time_raw, "%b %d,%Y")
            one_news_time = datetime.datetime.timestamp(time_dt)
        except:
            one_news_time = ""
        one_news['timestamp'] = one_news_time
        FIF_NewsMaster.append(one_news)

FIF = pd.DataFrame.from_dict(FIF_NewsMaster)
FIF = FIF[['website name','headline','open paragraph','link','timestamp']]
FIF.to_csv('FIF_news')