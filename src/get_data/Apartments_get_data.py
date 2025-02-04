#!/usr/bin/env python
# coding: utf-8

# In[1]:


from crawlbase import CrawlingAPI
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random


# In[2]:


# Web scraping data from apartments.com, focusing on the 1 bedroom housings located in Los Angeles

api = CrawlingAPI({'token': 'user_token'})
targetURL = 'https://www.apartments.com/los-angeles-ca/1-bedrooms/'
response = api.get(targetURL, {'timeout': 60})

if response['status_code'] == 200:
    soup = BeautifulSoup(response['body'], 'lxml')
else:
    print("failed")


# In[3]:


listings = soup.find_all("li", class_="mortar-wrapper")

data = []
for listing in listings:
    try:
        name = listing.find("span", class_="js-placardTitle title").get_text(strip=True)
        price = listing.find("p", class_="property-pricing").get_text(strip=True)
        address = listing.find("div", class_="property-address").get_text(strip=True)
        
        data.append({"Name": name, "Price": price, "Address": address})
    except:
        # Skip listings without complete info
        continue

# Create a DataFrame for easy analysis
df = pd.DataFrame(data)
print(df)


# In[4]:


# Web Scrape for the rest of the pages
# Total 18 pages
for page in range(2, 19):
    
    time.sleep(random.uniform(2, 5))
    
    api = CrawlingAPI({'token': 'HqTAGDe71BhwgouiVcbaeA'})
    targetURL = f'https://www.apartments.com/los-angeles-ca/1-bedrooms/{page}/'
    response = api.get(targetURL, {'timeout': 60})
    
    for attempt in range(5):
        try:
            response = api.get(targetURL)
            if response['status_code'] == 200:
                print(f"start scraping page{page}")
                break
        except Exception as e:
            time.sleep(2 ** attempt)
            
    if response['status_code'] != 200:
        print(f"scraping page{page} failed")
        continue

    listings = soup.find_all("li", class_="mortar-wrapper")
    
    for listing in listings:
        try:
            name = listing.find("span", class_="js-placardTitle title").get_text(strip=True)
            price = listing.find("p", class_="property-pricing").get_text(strip=True)
            address = listing.find("div", class_="property-address").get_text(strip=True)
            
            data.append({"Name": name, "Price": price, "Address": address})
        except:
            # Skip listings without complete info
            continue


# In[5]:


df = pd.DataFrame(data)
print(df)


# In[6]:


# Save data to csv file
path = '../../data/raw/'
df.to_csv(path+'apartments_raw_data.csv') 

