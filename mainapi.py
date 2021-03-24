from fastapi import FastAPI
from typing import Optional
import pandas as pd

import IntegratedScraper
import IntegratedSA

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get('/text')
def textSA(text):
    text = IntegratedSA.preprocess_text(text)
    return text

@app.get('/restaurant/{cityid}')
def city(cityid, review : bool = False, full : bool = False):
    if review == False and full == False:
        url = 'https://www.tripadvisor.fr/Restaurants-' + cityid
        scrap = IntegratedScraper.scrap_zone(url=url, full=False)
    if review and full == False:
        url = 'https://www.tripadvisor.fr/Restaurants-' + cityid
        prescrap = IntegratedScraper.scrap_zone(url=url, full=False)
        scrap = IntegratedScraper.scrape_many_reviews(urls=prescrap['Store_Url']) 
    if review == False and full:
        url = 'https://www.tripadvisor.fr/Restaurants-' + cityid
        scrap = IntegratedScraper.scrap_zone(url=url, full=True)
    if review and full:
        url = 'https://www.tripadvisor.fr/Restaurants-' + cityid
        prescrap = IntegratedScraper.scrap_zone(url=url, full=True)
        scrap = IntegratedScraper.scrape_many_reviews(urls=prescrap['Store_Url'])
    return scrap

@app.get('/restaurant/{cityid}/{restoid}')
def resto(cityid, restoid, review: bool = False, full: bool = False):
    if review and full == False:
        url = 'https://www.tripadvisor.fr/Restaurants_review-' + cityid +'-' + restoid
        scrap = IntegratedScraper.scrape_reviews(url=url)
    elif review == False and full == False:
        url = 'https://www.tripadvisor.fr/Restaurants_review-' + cityid +'-' + restoid
        scrap = IntegratedScraper.scrape_restaurant_info(url=url)
    elif review == False and full:
        url = 'https://www.tripadvisor.fr/Restaurants-' + cityid
        scrap = IntegratedScraper.scrap_zone(url=url, full=True)
    elif review and full:
        url = 'https://www.tripadvisor.fr/Restaurants-' + cityid
        prescrap = IntegratedScraper.scrap_zone(url=url, full=True)
        scrap = IntegratedScraper.scrape_many_reviews(urls=prescrap['Store_Url'])
    return scrap

@app.get('/restaurant/{cityid}/{restoid}/dashboard')
def dashboard(cityid, restoid):
    url = 'https://www.tripadvisor.fr/Restaurants_review-' + cityid +'-' + restoid
    scrap = IntegratedScraper.scrape_reviews(url=url)
    title = IntegratedScraper.scrape_restaurant_info(url=url)
    scrap.drop(columns=['Store_Name'], inplace=True)

    top10coms = scrap.sort_values(by='Rating', ascending = False)
    worst10coms = scrap.sort_values(by='Rating')

    review_list = []
    for review in scrap['Review']:
        review = IntegratedSA.preprocess_text(review)
        review_list.append(review.split())
    
    words = pd.Series(review_list).sort_values(ascending=False)
    
    data = {'wordcloud' : words,
            'Restaurant Info': title,
            'top 10 comments': top10coms.head(10),
            'Worst 10 comments': worst10coms.head(10)}
    return data