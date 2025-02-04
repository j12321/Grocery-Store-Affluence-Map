#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


# In[2]:


# Web scraping data from Erewhon's official website, extracting location data

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://erewhon.com/locations")

time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

stores = soup.find_all('div', class_="all-locations-list")

# Extract location data (name of the store and its zip code)
data = []
for store in stores:
    name = store.find("div", class_="title").find("p").get_text(strip=True)
    address = store.find("div", class_="address").find("p").get_text(strip=True)
    data.append({"name": name, "address": address})

driver.quit()


# In[3]:


# Create a DataFrame for easy analysis
df = pd.DataFrame(data)
print(df)


# In[4]:


# Save data to csv file
df = pd.DataFrame(data)
path = '../../data/raw/'
df.to_csv(path+'erewhon_raw_data.csv')


# In[ ]:




