#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


raw_data = pd.read_csv("../../data/raw/erewhon_raw_data.csv")


# In[3]:


raw_data


# In[4]:


zip_code_ls = []
for row in range(raw_data.shape[0]):
    address = raw_data.iloc[row][2]
    zip_code = address[-5:]
    zip_code_ls.append(zip_code)


# In[5]:


new_columns = {"zip code": zip_code_ls}
processed_data = raw_data.assign(**new_columns)


# In[6]:


processed_data = processed_data.drop(['address'], axis=1)


# In[7]:


path = '../../data/processed/'
processed_data.to_csv(path+'erewhon_processed_data.csv')


# In[ ]:




