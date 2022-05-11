# Dependencies
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': 'C:/Users/toluw/Downloads/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    browser=init_browser()
    mars_dict={}

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    articles = soup.find_all('div', class_='list_text')
    article = articles[0]
    for news in article:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        news_title = soup.find('div', class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text


    feat_img_url = 'https://spaceimages-mars.com/'
    browser.visit(feat_img_url)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    photos =soup.find_all('div', class_='floating_text_area')
    for photo in photos:
        #Use Beautiful Soup's find() method to navigate and retrieve attributes
        feat_pho = photo.find('a')
        feat_photo = feat_pho['href']
        featured_image_url = feat_img_url+feat_photo


    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    fact_df = tables[1]
    fact_df=fact_df.rename(columns={0:"Features",1:"Value"})
    Mars_facts = fact_df.to_html()


    im_url='https://marshemispheres.com/'
    browser.visit(im_url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    mars_result=soup.find('div',class_='collapsible results')
    items_in_result=mars_result.find_all('div',class_='item')
    hemisphere_img_urls=[]
    for item in items_in_result:
        try:
            hemisphere = item.find('div',class_='description')
            title = hemisphere.h3.text    
            hem_url = hemisphere.a['href']
            browser.visit(im_url + hem_url)
            html = browser.html
            soup = BeautifulSoup(html,'html.parser')
            img_url = im_url + (soup.find('li').a['href'])
            mars_hem_dict = {
                'title':title,
                'image_url':img_url
            }
            hemisphere_img_urls.append(mars_hem_dict)
        except Exception as e:
            print(e)


    mission_mars={
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "Mars_facts":Mars_facts,
    "hemisphere_images":hemisphere_img_urls
    }

    browser.quit()
    return mission_mars