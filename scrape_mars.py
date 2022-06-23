# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_web():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    #  Latest News from Mars Website
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    #  Create the html object
    html = browser.html

    #  use Beautiful soup to parse and find required titles, dates etc.
    soup = bs(html, 'html.parser')
    Latest_news_title = soup.find_all('div', class_='content_title')[0].text
    Latest_news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
    Latest_News_Date = soup.find_all('div', class_='list_date')[0].text

    # =====================================================================
    #  Get latest Featued image from spaceimage-mars website

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)  
    time.sleep(1)
    #  Create the html object
    html = browser.html

#  use Beautiful soup to parse and find required titles, dates etc.
    soup = bs(html, 'html.parser')
    floating_txt_area = soup.find_all('div', class_='floating_text_area')
    for img in floating_txt_area:
        a = img.find('a')
        image = a['href']
        print(image)
    featured_image_url = 'https://spaceimages-mars.com/' + image

    # ============================================================================

    # Obtain Mars facts table from galaxyfacts-mars website
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Mars', 'Earth']
    dfa = df.set_index('Description')
    # mars_facts_html = df.to_html(header = False, index = False)
    mars_facts_html = dfa.to_html(classes="table table-striped")

    # =============================================================================

    # Scraping Mars Hemisphere pictures from marshemisphere website

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html

    time.sleep(1)

    #  use Beautiful soup to parse and find required titles, dates etc.
    soup = bs(html, 'html.parser')
    descrp = soup.find_all('div', class_='description')
    mars_pics_url = []

    # making a for loop to pull title & image_urls

    for data in descrp: 
    #     error handling
        try: 
            title = data.find('h3').text
            link = data.a['href']
            url_link = f"https://marshemispheres.com/" + link
            browser.visit(url_link)
            html = browser.html
            soup = bs(html, 'html.parser')
            pg_all = soup.find('img', class_="wide-image")
            pic_link = pg_all['src']
            img_url = f"https://marshemispheres.com/" + pic_link
            
            if (title and pic_link):
            
                mars_pic_dict = {
                    'Title':title, 
                    'img_url': img_url
                }

                mars_pics_url.append(mars_pic_dict)
        except Exception as e:
            print(e)

    Mars_dict = {
        "Latest_news_Title": Latest_news_title,
        "Latest_news_Paragraph": Latest_news_paragraph,
        "Latest_news_Date": Latest_News_Date,
        "Featured_image_url": featured_image_url,
        "Mars_facts_html_table": mars_facts_html,
        "Hemisphere_images": mars_pics_url
    }
    print(Mars_dict)
    browser.quit()
    return Mars_dict
    
    


