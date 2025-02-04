#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd


# In[2]:


# Web scraping data from Whole Foods' official website, extracting location data in Los Angeles

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.wholefoodsmarket.com/stores")
time.sleep(3)


# In[3]:


# Since the URL doesn't change during searches, simulate interaction with the webpage by manipulating the input fields
search_box = driver.find_element(By.ID, "store-finder-search-bar")
search_box.clear()
search_box.send_keys('Los Angeles')
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)


# In[4]:


page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')


# In[5]:


stores = soup.find_all("div", class_="w-store-finder-core-info")

# Extract location data (name of the store and its zip code)
data = []
for store in stores:
    name = store.find("div", class_="w-store-finder-store-name").get_text(strip=True)
    address = store.find("div", class_="storeAddress").get_text(strip=True)
    data.append({"name": name, "address": address})
driver.quit()


# In[6]:


# Create a DataFrame for easy analysis
df = pd.DataFrame(data)
print(df)


# In[7]:


# Save data to csv file
df = pd.DataFrame(data)
path = '../../data/raw/'
df.to_csv(path+'whole_foods_raw_data.csv')


# In[ ]:




