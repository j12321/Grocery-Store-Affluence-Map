#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


# In[3]:


# Web scraping data from Ralphs' official website, extracting location data in Los Angeles
# Since the website includes Food 4 Less's locations, count them as well! 

data = []
for page in [1, 2]:  # Total 2 pages
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(f"https://www.ralphs.com/stores/search?referrer=link_hub&searchText=los%20angeles&selectedPage={page}")
    
    time.sleep(10)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    stores = soup.find_all('div', class_="SearchResults-storeResult")
    
    # Extract location data (name of the store, its zip code, and which store it is)
    for store in stores:
        name = store.find("h3", class_="kds-Heading kds-Heading--s").get_text(strip=True)
        address = store.find("a", class_="kds-Link kds-Link--m text-primary")

        # Since the locations of Ralphs and Food 4 Less are in the same page, define which store it is
        try:
            # If the store is Food 4 Less, there will be a link of "shop Food 4 Less"
            shop_name = store.find("a", class_="kds-Link kds-Link--m").get_text(strip=True)
            data.append({"name": name, "address": address, "Ralphs or Food 4 Less": "Food 4 Less"})
        except:
            data.append({"name": name, "address": address, "Ralphs or Food 4 Less": "Ralphs"})
    
    driver.quit()


# In[4]:


# Create a DataFrame for easy analysis
df = pd.DataFrame(data)
print(df)


# In[5]:


# Save data to csv file
df = pd.DataFrame(data)
path = '../../data/raw/'
df.to_csv(path+'ralphs_food4less_raw_data.csv')


# In[ ]:




