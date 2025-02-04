#!/usr/bin/env python
# coding: utf-8

# In[1]:


from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
from functools import lru_cache
import json


# In[2]:


geolocator = Nominatim(user_agent="zip_distance_calculator")


# In[3]:


def get_coordinates(zip_code):
    '''
    The function return the coordinate of zip code
    '''
    location = geolocator.geocode({"postalcode": zip_code, "country": "US"})
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"Coordinates for ZIP code {zip_code} not found.")


# In[4]:


@lru_cache(maxsize=10000)
def get_distance(zipcode_1, zipcode_2):
    '''
    The function calculates the distance between zip codes. 
    input: 2 zip codes; return: distance(miles)
    '''
    coords_1 = get_coordinates(zipcode_1)
    coords_2 = get_coordinates(zipcode_2)
    distance = geodesic(coords_1, coords_2).miles
    return distance


# In[6]:


apartments_data = pd.read_csv("../../data/processed/apartments_processed_data.csv")
erewhon_data = pd.read_csv("../../data/processed/erewhon_processed_data.csv")
whole_foods_data = pd.read_csv("../../data/processed/whole_foods_processed_data.csv")
trader_joes_data = pd.read_csv("../../data/processed/trader_joes_processed_data.csv")
ralphs_data = pd.read_csv("../../data/processed/ralphs_processed_data.csv")
food4less_data = pd.read_csv("../../data/processed/food4less_processed_data.csv")


# In[83]:


def get_avg_price_ls(store_data):
    '''
    The function calculate the average min/ max price of the listings around locations of the grocery story.
    Consider all listings where the distance is under 5 miles.
    The return will be a list of average min/max price corresponding to the locations.
    The lenghth of the return will be the same as the numbers of locations for each grocery story.
    output: [[min_avg_price_1, max_avg_price_1], [min_avg_price_2, max_avg_price_2], ...]
    If there is no listing around the store, return "No listings around this location"
    '''
    max_mile = 5
    all_avg_price_ls = []  # the return list
    store_zipcode_ls = list(store_data['zip code'])
    
    apt_zip_codes = apartments_data['Zip Code']
    apt_min_prices = apartments_data['Min Price']
    apt_max_prices = apartments_data['Max Price']
    
    for store_zipcode in store_zipcode_ls:
        distances = apt_zip_codes.apply(lambda apt_zip: get_distance(store_zipcode, apt_zip))
        
        # Filter apartments within the distance threshold
        within_5_miles = distances <= max_mile
        filtered_min_prices = apt_min_prices[within_5_miles]
        filtered_max_prices = apt_max_prices[within_5_miles]

        if len(filtered_min_prices) == 0:
            all_avg_price_ls.append('No listings around this location')
        else:
            avg_min_price = np.mean(filtered_min_prices)
            avg_max_price = np.mean(filtered_max_prices)
            all_avg_price_ls.append([avg_min_price, avg_max_price])
    
    return all_avg_price_ls


# In[84]:


erewhon_price_ls = get_avg_price_ls(erewhon_data)
whole_foods_price_ls = get_avg_price_ls(whole_foods_data)
trader_joes_price_ls = get_avg_price_ls(trader_joes_data)
ralphs_price_ls = get_avg_price_ls(ralphs_data)
food4less_price_ls = get_avg_price_ls(food4less_data)


# In[99]:


# Results for Erewhon
for i in range(len(erewhon_price_ls)):
    name = erewhon_data['name'][i]
    zip_code = erewhon_data['zip code'][i]
    if erewhon_price_ls[i] != 'No listings around this location':
        print(f"The average min rent around Erewhon {name}({zip_code}): {erewhon_price_ls[i][0]}")
        print(f"The average max rent around Erewhon {name}({zip_code}): {erewhon_price_ls[i][1]}\n")
    else:
        print(f"No listings around Erewhon {name}({zip_code})\n")


# In[100]:


# Results for Whole Foods
for i in range(len(whole_foods_price_ls)):
    name = whole_foods_data['name'][i]
    zip_code = whole_foods_data['zip code'][i]
    if whole_foods_price_ls[i] != 'No listings around this location':
        print(f"The average min rent around Whole Foods {name}({zip_code}): {whole_foods_price_ls[i][0]}")
        print(f"The average max rent around Whole Foods {name}({zip_code}): {whole_foods_price_ls[i][1]}\n")
    else:
        print(f"No listings around Whole Foods {name}({zip_code})\n")


# In[104]:


# Results for Trader Joe's
for i in range(len(trader_joes_price_ls)):
    name = trader_joes_data['name'][i].split('(')[0]
    zip_code = trader_joes_data['zip code'][i]
    if trader_joes_price_ls[i] != 'No listings around this location':
        print(f"The average min rent around {name}({zip_code}): {trader_joes_price_ls[i][0]}")
        print(f"The average max rent around {name}({zip_code}): {trader_joes_price_ls[i][1]}\n")
    else:
        print(f"No listings around {name}({zip_code})\n")


# In[105]:


# Results for Ralphs
for i in range(len(ralphs_price_ls)):
    name = ralphs_data['name'][i]
    zip_code = ralphs_data['zip code'][i]
    if ralphs_price_ls[i] != 'No listings around this location':
        print(f"The average min rent around Ralphs {name}({zip_code}): {ralphs_price_ls[i][0]}")
        print(f"The average max rent around Ralphs {name}({zip_code}): {ralphs_price_ls[i][1]}\n")
    else:
        print(f"No listings around Ralphs {name}({zip_code})\n")


# In[106]:


# Results for Food 4 Less
for i in range(len(food4less_price_ls)):
    name = food4less_data['name'][i]
    zip_code = food4less_data['zip code'][i]
    if food4less_price_ls[i] != 'No listings around this location':
        print(f"The average min rent around Food 4 Less {name}({zip_code}): {food4less_price_ls[i][0]}")
        print(f"The average max rent around Food 4 Less {name}({zip_code}): {food4less_price_ls[i][1]}\n")
    else:
        print(f"No listings around Food 4 Less {name}({zip_code})\n")


# In[110]:


# Save results to a json file
data = {"Erewhon": erewhon_price_ls, "Whole Foods": whole_foods_price_ls, "Trader Joe's": trader_joes_price_ls, 
        "Ralphs": ralphs_price_ls, "Food 4 Less": food4less_price_ls}
with open("analyze_result.json", "w") as file:
    json.dump(data, file)


# In[ ]:




