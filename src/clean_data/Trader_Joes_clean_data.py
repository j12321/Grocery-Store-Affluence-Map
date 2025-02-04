#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
from bs4 import BeautifulSoup


# In[4]:


raw_data = pd.read_csv("../../data/raw/trader_joes_raw_data.csv")


# In[5]:


raw_data


# In[17]:


zip_code_ls = []
for row in range(raw_data.shape[0]):
    address = raw_data.iloc[row][2]
    spans = address.split("span")
    zip_code = spans[9].replace('>', '').replace('</', '')
    zip_code_ls.append(zip_code)


# In[19]:


new_columns = {"zip code": zip_code_ls}
processed_data = raw_data.assign(**new_columns)


# In[21]:


processed_data = processed_data.drop(['address'], axis=1)


# In[23]:


path = '../../data/processed/'
processed_data.to_csv(path+'trader_joes_processed_data.csv')


# In[ ]:




