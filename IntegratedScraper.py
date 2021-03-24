import requests 
from bs4 import BeautifulSoup
import csv 
import time
import random
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 11.0; Windows NT 5.2; Trident/3.0)',
    'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20140725 Firefox/37.0',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/3.0)',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_7 rv:2.0; sl-SI) AppleWebKit/532.45.6 (KHTML, like Gecko) Version/5.1 Safari/532.45.6',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_0 rv:5.0; en-US) AppleWebKit/534.45.2 (KHTML, like Gecko) Version/4.1 Safari/534.45.2',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5350 (KHTML, like Gecko) Chrome/36.0.843.0 Mobile Safari/5350',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8 rv:3.0; sl-SI) AppleWebKit/531.50.3 (KHTML, like Gecko) Version/5.1 Safari/531.50.3',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0) AppleWebKit/533.20.5 (KHTML, like Gecko) Version/5.0.3 Safari/533.20.5']

def init_browser(url):
    rantime = random.randint(1,2)/3
    user_agent = random.choice(user_agent_list) 
    headers = {'User-Agent': user_agent}
    time.sleep(rantime)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    return page, soup

def scrape_many_reviews(urls):
    #intialize dataframe
    cols = ['Store_Name', 'Reviewer_Name', 'Rating_Date', 'Review', 'Rating']
    lst = []
    
    for url in urls:
        print('scraping reviews for : ', url)

        nextPage = True
        while nextPage:
            #initialize browser
            driver.get(url)
            time.sleep(random.randint(1,2)/3)

            #display more
            more = driver.find_elements_by_xpath("//span[contains(text(),'Plus')]")
            for x in range(0,len(more)):
                try:
                    driver.execute_script("arguments[0].click();", more[x])
                    time.sleep(random.randint(1,2)/2)
                except:
                    pass
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            #Store name
            try:
                storeName = soup.find('h1', class_='_3a1XQ88S').text
            except:
                storeName = 'None'

            #Reviews
            results = soup.find('div', class_='listContainer hide-more-mobile')
            try:
                reviews = results.find_all('div', class_='prw_rup prw_reviews_review_resp')
            except Exception:
                continue

            #to Dataframe
            try:
                lst_dict = []
                for review in reviews:
                    ratingDate = review.find('span', class_='ratingDate').get('title')
                    text_review = review.find('p', class_='partial_entry')
                    if len(text_review.contents) > 2:
                        reviewText = str(text_review.contents[0][:-3]) + ' ' + str(text_review.contents[1].text)
                    else:
                        reviewText = text_review.text
                    reviewerUsername = review.find('div', class_='info_text pointer_cursor')
                    reviewerUsername = reviewerUsername.select('div > div')[0].get_text(strip=True)
                    rating = review.find('div', class_='ui_column is-9').findChildren('span')
                    rating = str(rating[0]).split('_')[3].split('0')[0]
                    lst.append([storeName, reviewerUsername, ratingDate, reviewText, rating])              
            except:
                pass

            #Go to next page if exists
            try:
                unModifiedUrl = str(soup.find('a', class_ = 'nav next ui_button primary',href=True)['href'])
                url = 'https://www.tripadvisor.fr' + unModifiedUrl
                if url == 'https://www.tripadvisor.fr':
                    nextPage = False
            except:
                nextPage = False

    #create dataframe
    data = pd.DataFrame(lst, columns=cols)
    return data

def scrape_reviews(url):
    #intialize dataframe
    cols = ['Store_Name', 'Reviewer_Name', 'Rating_Date', 'Review', 'Rating']
    lst = []
    
    print('scraping reviews for : ', url)

    nextPage = True
    while nextPage:
        #initialize browser       
        driver.get(url)
        time.sleep(random.randint(1,2)/3)

        #display more
        more = driver.find_elements_by_xpath("//span[contains(text(),'Plus')]")
        for x in range(0,len(more)):
            try:
                driver.execute_script("arguments[0].click();", more[x])
                time.sleep(random.randint(1,2)/2)
            except:
                pass
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        #Store name
        try:
            storeName = soup.find('h1', class_='_3a1XQ88S').text
        except:
            storeName = 'None'

        #Reviews
        results = soup.find('div', class_='listContainer hide-more-mobile')
        try:
            reviews = results.find_all('div', class_='prw_rup prw_reviews_review_resp')
        except Exception:
            continue

        #to Dataframe
        try:
            lst_dict = []
            for review in reviews:
                ratingDate = review.find('span', class_='ratingDate').get('title')
                text_review = review.find('p', class_='partial_entry')
                if len(text_review.contents) > 2:
                    reviewText = str(text_review.contents[0][:-3]) + ' ' + str(text_review.contents[1].text)
                else:
                    reviewText = text_review.text
                reviewerUsername = review.find('div', class_='info_text pointer_cursor')
                reviewerUsername = reviewerUsername.select('div > div')[0].get_text(strip=True)
                rating = review.find('div', class_='ui_column is-9').findChildren('span')
                rating = str(rating[0]).split('_')[3].split('0')[0]
                lst.append([storeName, reviewerUsername, ratingDate, reviewText, rating])              
        except:
            pass

        #Go to next page if exists
        try:
            unModifiedUrl = str(soup.find('a', class_ = 'nav next ui_button primary',href=True)['href'])
            url = 'https://www.tripadvisor.fr' + unModifiedUrl
            if url == 'https://www.tripadvisor.fr':
                nextPage = False
        except:
            nextPage = False

    #create dataframe
    data = pd.DataFrame(lst, columns=cols)
    return data

def scrape_restaurant_info(url):
    #intialize dataframe
    cols = ['Store_Name', 'Avg_Rating', 'Price_Range', 'Num_Review', 'Store_Adress', 'Store_Url']
    lst = []
    pricesCat = ['€€€€', '€', '€€-€€€']

    #intialize browser
    page, soup = init_browser(url)
    
    #scrap
    storeName = soup.find('h1', class_='_3a1XQ88S').text
    avgRating = soup.find('span', class_='r2Cf69qf').text.strip()
    priceRange = soup.find('span', class_ = '_13OzAOXO _34GKdBMV').find('a', class_='_2mn01bsa').text
    if priceRange not in pricesCat:
        priceRange = "Unknown"
    storeAddress = soup.find('div', class_= '_2vbD36Hr _36TL14Jn').find('span', class_='_2saB_OSe').text.strip()
    noReviews = soup.find('a', class_='_10Iv7dOs').text.strip().split()[0]
    lst.append([storeName, avgRating, priceRange, noReviews, storeAddress, url])

    #create dataframe
    data = pd.DataFrame(lst, columns=cols)
    return data

def scrap_zone(url, full=False):
    #initialize dataframe
    cols = ['Store_Name', 'Price_Range']
    lst = []
    data = pd.DataFrame(columns=cols)

    #init for loop
    nextPage=True
    while nextPage:

        #initialize browser
        page, soup = init_browser(url)

        #scrap
        links = soup.find_all('div', class_='wQjYiB7z')
        storesUrls = []
        for urlunique in links:
            storeUrl = 'https://www.tripadvisor.fr' + urlunique.find('a', class_='_15_ydu6b', href = True)['href']
            storesUrls.append(storeUrl)

        for url1 in storesUrls:
            print(url1)
            try:
                data = data.append(scrape_restaurant_info(url1), ignore_index=True)
            except:
                pass

        if full:
        #Go to next page if exists
            try:
                unModifiedUrl = str(soup.find('a', class_ = 'nav next rndBtn ui_button primary taLnk',href=True)['href'])
                url = 'https://www.tripadvisor.fr' + unModifiedUrl
                if url == 'https://www.tripadvisor.fr':
                    nextPage = False
            except:
                nextPage = False
        else:
            nextPage=False

    return data
    
#initialize webdriver
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)