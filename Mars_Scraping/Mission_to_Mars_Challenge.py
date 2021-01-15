#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import requests

import pandas as pd


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[3]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# This code used to work but the website has since been reformatted and the module code doesn't work anymore (as of 1/14/21)
# I am going to comment out this section for now


# In[10]:


# Visit URL
#url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#browser.visit(url)


# In[11]:


# Find and click the full image button
#full_image_elem = browser.find_by_id('full_image')
#full_image_elem.click()


# In[12]:


# Find the more info button and click that
#browser.is_element_present_by_text('more info', wait_time=1)
#more_info_elem = browser.links.find_by_partial_text('more info')
#more_info_elem.click()


# In[13]:


# Parse the resulting html with soup
#html = browser.html
#img_soup = soup(html, 'html.parser')


# In[14]:


# Find the relative image url
#img_url_rel = img_soup.select_one('figure.lede a img').get("src")
#img_url_rel


# In[15]:


# Use the base URL to create an absolute URL
#img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
#img_url


# ### Mars Facts

# In[16]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()


# In[17]:


df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[18]:


df.to_html()


# ### Mars Weather

# In[19]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[20]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[21]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[22]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[23]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# HTML Object
html = browser.html

# Parse HTML with Beautiful Soup
img_soup = soup(html, 'html.parser')

# Retreive all items that contain mars hemispheres information
images = img_soup.find_all('div', class_='item')

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for i in images: 
    
    hemispheres ={}
    
    # get link to each image page
    image_url = hemispheres_main_url + i.find('a').get('href')
    browser.visit(image_url)
    
    # from each image page get full resolution image url and title
    html_hemispheres = soup(browser.html, 'html.parser')
    link = hemispheres_main_url + html_hemispheres.find('img', class_='wide-image').get('src')
    
    hemispheres['img_url'] = link
    
    # get title
    title = html_hemispheres.find('h2', class_='title').text
    hemispheres['title'] = title
    
    hemisphere_image_urls.append(hemispheres)
    browser.back()
    


# In[24]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[25]:


# 5. Quit the browser
browser.quit()


# In[ ]:




