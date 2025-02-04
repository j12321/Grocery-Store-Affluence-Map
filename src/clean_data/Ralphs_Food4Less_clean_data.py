#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


raw_data = pd.read_csv("../../data/raw/ralphs_food4less_raw_data.csv")


# In[3]:


raw_data


# In[10]:


zip_code_ls = []
for row in range(raw_data.shape[0]):
    address = raw_data.iloc[row][2]
    zip_code = address.split('<svg')[0][-5:]
    zip_code_ls.append(zip_code)


# In[12]:


new_columns = {"zip code": zip_code_ls}
processed_data = raw_data.assign(**new_columns)


# In[13]:


processed_data


# In[16]:


ralphs_data = processed_data[processed_data['Ralphs or Food 4 Less']=='Ralphs']
food4less_data = processed_data[processed_data['Ralphs or Food 4 Less']=='Food 4 Less']


# In[19]:


ralphs_data = ralphs_data.drop(['address', 'Ralphs or Food 4 Less'], axis=1)


# In[20]:


food4less_data = food4less_data.drop(['address', 'Ralphs or Food 4 Less'], axis=1)


# In[23]:


path = '../../data/processed/'
ralphs_data.to_csv(path+'ralphs_processed_data.csv')
food4less_data.to_csv(path+'food4less_processed_data.csv')


# In[ ]:




