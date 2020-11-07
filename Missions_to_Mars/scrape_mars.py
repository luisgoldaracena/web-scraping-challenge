#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

mars_data={}

def scrape():
    browser = init_browser()

    #NASA NEWS
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news = soup.find('div', class_='list_text')
    news_title=news.find('div', class_="content_title").text
    news_p=news.find("div", class_="article_teaser_body").text
    mars_data["title"]=news_title
    mars_data["news_paragraph"]=news_p

    #Featured Image
    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    base_url="https://www.jpl.nasa.gov"
    background=soup.find("article", class_="carousel_item")
    link1=base_url+background.find("a", class_="button fancybox")["data-link"]
    browser.visit(link1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image=soup.find("figure", class_="lede")
    featured_image_url=base_url+image.find("a")["href"]
    mars_data["featured_image"]=featured_image_url

    #Mars Weather
    twitter_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather_string=soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather=mars_weather_string.span.text
    mars_data["weather"]=mars_weather

    #Mars Facts
    facts_url="https://space-facts.com/mars/"
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    mars_table=tables[0]
    mars_table.rename(columns={0:"Mars charachteristics",1:"Measurments"}, inplace=True)
    mars_table.set_index("Mars charachteristics", inplace=True)
    html_table = mars_table.to_html()
    html_table=html_table.replace('\n', '')
    mars_data["table"]=html_table

    #Mars Hemispheres
    hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hem_url_base="https://astrogeology.usgs.gov/"
    browser.visit(hem_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_titles=soup.find_all("h3")
    titles=[]
    links=[]
    pics_page=soup.find_all("div",class_="description")
    for x in range(4):
        pic_page=hem_url_base+pics_page[x].find("a")["href"]
        browser.visit(pic_page)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_link=soup.find_all("li")[0].a
        links.append(img_link["href"])
        titles.append(img_titles[x].text)
        browser.visit(hem_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []
    for x in range(4):
        hemisphere_image_urls.append({"title":titles[x],"img_url":links[x]})
    mars_data["hemispheres"]=hemisphere_image_urls

    return mars_data    
