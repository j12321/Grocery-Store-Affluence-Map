#!/usr/bin/env python
# coding: utf-8

# In[1]:


from crawlbase import CrawlingAPI
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[2]:


# Web scraping data from Trader Joe's official website, extracting location data in Los Angeles

api = CrawlingAPI({'token': 'user_token'})
targetURL = 'https://locations.traderjoes.com/ca/los-angeles/'
response = api.get(targetURL)

if response['status_code'] == 200:
    soup = BeautifulSoup(response['body'], 'lxml')
else:
    print("failed")


# In[4]:


stores = soup.find_all("div", class_="itemlist")

# Extract location data (name of the store and its zip code)
data = []
for store in stores:
    try:
        name = store.find("span", class_="ga_w2gi_lp").get_text(strip=True)
        address_div = store.find("div", class_="address-left")
        #spans = address_div.find_all("span")
        #zip_code = spans[-2].get_text(strip=True) 
        
        data.append({"name": name, "address": address_div})
    except AttributeError:
        # Skip listings without complete info
        continue

# Create a DataFrame for easy analysis
df = pd.DataFrame(data)
print(df)


# In[5]:


# Save data to csv file
df = pd.DataFrame(data)
path = '../../data/raw/'
df.to_csv(path+'trader_joes_raw_data.csv')


# In[ ]:




