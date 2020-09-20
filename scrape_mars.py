import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup

def scrape():
    scraping_results = {}
    # Mac for Splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    first_item = soup.find('div', class_='list_text')
    first_headline = first_item.find('div', class_='content_title')
    news_title = first_headline.text.strip()
    scraping_results['news-title'] = news_title
    first_content = first_item.find('div', class_='article_teaser_body')
    news_p = first_content.text.strip()
    scraping_results['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_id('full_image')
    browser.links.find_by_partial_text('more info').click()
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    links = jpl_soup.find_all('div', class_='download_tiff')
    featured_image_url = 'http' + links[1].a.get('href')
    scraping_results['featured_image_url'] = featured_image_url

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    scraping_results['mars_facts'] = tables[0]

    # Mars Hemispheres
    hemispheres = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    for hems in range(4):
        browser.visit(url)
        browser.find_by_css('.thumb')[hems].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # Get the title
        title = soup.find('h2', class_='title')
        title = title.text.strip().replace(' Enhanced', '')
        # Get the url
        downloads = soup.find('div', class_='downloads')
        href = downloads.a.get('href')
        # Add them to a dictionary
        hemisphere = {}
        hemisphere['title'] = title
        hemisphere['img_url'] = href
        # Add dictionary to list
        hemispheres.append(hemisphere)

    scraping_results['hemispheres'] = hemispheres
    browser.quit()
    return scraping_results

results = scrape()
print(results)