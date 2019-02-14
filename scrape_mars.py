from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\selenium\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


listings={}

    # NASA Mars News
def scrape_mars_news():
    try: 
       # Initialize browser 
        browser = init_browser()
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)
        time.sleep(2)
        #using bs to write it into html
        html = browser.html
        soup = bs(html,"html.parser")

        news_title=soup.body.find('div',class_="content_title").text
        listings["news_title"]=news_title
        news_p=soup.body.find('div',class_="article_teaser_body").text
        listings["news_p"]=news_p
        return listings
    
    finally:
        browser.quit()

    # # JPL Mars Space Images - Featured Image
def scrape_mars_image():
    try: 
        # Initialize browser 
        browser = init_browser()
        url = "https://www.jpl.nasa.gov/spaceimages/"
        base_url="https://www.jpl.nasa.gov/"
        browser.visit(url)
        time.sleep(2)
        #using bs to write it into html
        html = browser.html
        soup = bs(html,"html.parser")
        img_url=soup.find('li',class_='slide').a['data-fancybox-href']
        print(img_url)
        featured_image_url=base_url+img_url
        listings["featured_image_url"]=featured_image_url
        return listings
    
    finally:
        browser.quit()
 # Mars Weather
def scrape_mars_weather():
    try: 
        # Initialize browser 
        browser = init_browser()
        url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url)
        time.sleep(2)
        #using bs to write it into html
        html = browser.html
        soup = bs(html,"html.parser")
        listings["mars_weather"]=soup.find('li', id='stream-item-tweet-1092605878094696448').p.text
        return listings
    
    finally:
        browser.quit()

    # # Mars Facts
def scrape_mars_facts():
    url="https://space-facts.com/mars/"
    table=pd.read_html(url)
    type(table)
    df=table[0]
    df.columns=['Description','Value']
    df.set_index('Description', inplace=True)
    listings["mars_facts"]=df.to_html()
    return listings
    
    # # Mars Hemispheres
def scrape_mars_hemispheres():
    try: 
        # Initialize browser 
        browser = init_browser()
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        base_url="https://astrogeology.usgs.gov/"
        browser.visit(url)
        time.sleep(2)
        #using bs to write it into html
        html = browser.html
        soup = bs(html,"html.parser")
        soup.find('div',class_='description').a
        hemisphere_image_urls=[]
        results=soup.find_all('div',class_='description')
        for result in results:
            title = result.a.text
            link=result.a['href']
            browser.visit( base_url+link)
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')
            # Retrieve full image source 
            img_url = base_url + soup.find('img', class_='wide-image')['src']
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        listings["hemisphere_image_urls"]=hemisphere_image_urls

        return listings
    
    finally:
        browser.quit()