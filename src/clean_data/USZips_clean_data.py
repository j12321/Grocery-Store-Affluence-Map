#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv("../../data/raw/UsZips.csv")


# In[3]:


data_la = data[data['place name']=='Los Angeles']


# In[4]:


data_la


# In[5]:


data_la = data_la.drop(['country code', 'admin name1', 'admin name2', 'admin code2'], axis=1)


# In[6]:


data_la.to_csv('../../data/processed/LA_zip_LatLong.csv', index=False)


# In[ ]:




