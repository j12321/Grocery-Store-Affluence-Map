#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


raw_data = pd.read_csv("../../data/raw/apartments_raw_data.csv")


# In[3]:


# Drop rows that do not have price but call for rent
raw_data = raw_data[raw_data['Price']!='Call for Rent']


# In[4]:


raw_data


# In[5]:


min_price_ls = []
max_price_ls = []
zip_code_ls = []
for row in range(raw_data.shape[0]):
    min_price = None
    max_price = None
    price = raw_data.iloc[row][2]
    price_ls = price.split(' - ')  
    # There might be a price range(e.g. $1,270 - $1,850) or just a price(e.g. $2,200)
    if len(price_ls) == 2:
        min_price = int(price_ls[0].replace('$', '').replace(',', ''))
        max_price = int(price_ls[1].replace('$', '').replace(',', ''))
    else:
        min_price = int(price_ls[0].replace('$', '').replace(',', ''))
    min_price_ls.append(min_price)
    max_price_ls.append(max_price)

    address = raw_data.iloc[row][3]
    zip_code = address[-5:]
    zip_code_ls.append(zip_code)


# In[6]:


new_columns = {"Min Price": min_price_ls, "Max Price": max_price_ls, "Zip Code": zip_code_ls}
processed_data = raw_data.assign(**new_columns)


# In[7]:


processed_data = processed_data.drop(['Price', 'Address'], axis=1)


# In[8]:


processed_data = processed_data.dropna()


# In[13]:


path = '../../data/processed/'
processed_data.to_csv(path+'apartments_processed_data.csv')


# In[ ]:




