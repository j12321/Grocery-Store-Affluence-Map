#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.io as pio

import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


# In[2]:


pio.renderers.default = 'browser'


# In[3]:


with open("../analyze_data/analyze_result.json", "r") as file:
    data = json.load(file)


# In[4]:


erewhon_data = pd.read_csv("../../data/processed/erewhon_processed_data.csv")
whole_foods_data = pd.read_csv("../../data/processed/whole_foods_processed_data.csv")
trader_joes_data = pd.read_csv("../../data/processed/trader_joes_processed_data.csv")
ralphs_data = pd.read_csv("../../data/processed/ralphs_processed_data.csv")
food4less_data = pd.read_csv("../../data/processed/food4less_processed_data.csv")


# In[5]:


def plot_bar_chart(store_name, store_data, store_json):
    '''
    plot the average min/ max rent for each location of thr grocery store (bar chart)
    '''
    price_data = []
    locations = []
    for i in range(len(store_json)):
        if store_json[i] != 'No listings around this location':
            price_data.append(store_json[i])
            if store_name == "Trader Joe's":
                locations.append(list(store_data['name'])[i].split('(')[0].replace("Trader Joe's", ''))
            else:
                locations.append(list(store_data['name'])[i])
    
    min_prices = [item[0] for item in price_data]
    max_prices = [item[1] for item in price_data]
    
    x = np.arange(len(locations))
    width = 0.4
    
    fig, ax = plt.subplots(figsize=(28, 8))
    
    ax.bar(x - width / 2, min_prices, width, label='Min Price', color='skyblue')
    ax.bar(x + width / 2, max_prices, width, label='Max Price', color='orange')
    
    ax.set_xlabel('Location Name')
    ax.set_ylabel('Average Rent Around the Location')
    ax.set_title(f'Min and Max Rent for {store_name} Locations')
    ax.set_xticks(x)
    ax.set_xticklabels(locations)
    ax.legend()

    path = '../../results/images/'
    filename = store_name.lower().replace(' ', '').replace("'", '')
    plt.savefig(path+filename+'.jpg')
    plt.show()


# In[6]:


plot_bar_chart('Erewhon', erewhon_data, data['Erewhon'])


# In[7]:


plot_bar_chart('Whole Foods', whole_foods_data, data['Whole Foods'])


# In[8]:


plot_bar_chart("Trader Joe's", trader_joes_data, data["Trader Joe's"])


# In[9]:


plot_bar_chart("Ralphs", ralphs_data, data["Ralphs"])


# In[10]:


plot_bar_chart("Food 4 Less", food4less_data, data["Food 4 Less"])


# In[11]:


# Calculate average min/ max of all locations for each grocery store
def avg_all_locs(store_json):
    min_price = []
    max_price = []
    for item in store_json:
        if item != 'No listings around this location':
            min_price.append(item[0])
            max_price.append(item[1])
    return [np.mean(min_price), np.mean(max_price)]


# In[12]:


store_ls = ['Erewhon', 'Whole Foods', "Trader Joe's", 'Ralphs', 'Food 4 Less']


# In[13]:


# Plot a bar chart showing the average rent price between 5 grocery stores
min_prices = []
max_prices = []
for store in store_ls:
    min_prices.append(avg_all_locs(data[store])[0])
    max_prices.append(avg_all_locs(data[store])[1])

x = np.arange(len(store_ls))
width = 0.4
    
fig, ax = plt.subplots(figsize=(12, 8))
    
ax.bar(x - width / 2, min_prices, width, label='Min Price', color='skyblue')
ax.bar(x + width / 2, max_prices, width, label='Max Price', color='orange')
    
ax.set_xlabel('Grocery Store')
ax.set_ylabel('Average Rent Around the Location')
ax.set_title('Rent Near Grocery Stores')
ax.set_xticks(x)
ax.set_xticklabels(store_ls)
ax.legend()

path = '../../results/images/'
plt.savefig(path+'compare_all_stores'+'.jpg')
plt.show()


# In[14]:


apartments_data = pd.read_csv('../../data/processed/apartments_processed_data.csv')


# In[15]:


# Merge locations from all grocery store to a file
df_ls = [erewhon_data, whole_foods_data, trader_joes_data, ralphs_data, food4less_data]
result_ls = [data['Erewhon'], data['Whole Foods'], data["Trader Joe's"], data["Ralphs"], data["Food 4 Less"]]
store_ls = []
zip_code_ls = []
for i in range(len(df_ls)):
    for j in range(df_ls[i].shape[0]):
        if result_ls[i][j] != 'No listings around this location':
            zip_code_ls.append(df_ls[i].iloc[j]['zip code'])
            if i == 0:
                store_ls.append('Erewhon')
            elif i == 1:
                store_ls.append('Whole Foods')
            elif i == 2:
                store_ls.append("Trader Joe's")
            elif i == 3:
                store_ls.append('Ralphs')
            else:
                store_ls.append('Food 4 Less')
grocery_data = {'Store': store_ls, 'Zip Code':zip_code_ls}
grocery_df = pd.DataFrame(grocery_data)


# In[16]:


# Calculate average rent price by zip code
avg_min_price_by_zip = apartments_data.groupby('Zip Code')['Min Price'].mean()
avg_max_price_by_zip = apartments_data.groupby('Zip Code')['Max Price'].mean()


# In[17]:


avg_min_price_df = avg_min_price_by_zip.reset_index()
avg_max_price_df = avg_max_price_by_zip.reset_index()


# In[18]:


geolocator = Nominatim(user_agent="zip_distance_calculator")
def get_coordinates(zip_code):
    '''
    The function return the coordinate of zip code
    '''
    location = geolocator.geocode({"postalcode": zip_code, "country": "US"})
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"Coordinates for ZIP code {zip_code} not found.")


# In[19]:


geo_df = gpd.read_file('../../data/raw/LA_County_ZIP_Codes.geojson')


# In[20]:


zip_to_latlong = pd.read_csv('../../data/processed/LA_zip_LatLong.csv')


# In[21]:


zip_coords_dict = zip_to_latlong.set_index('postal code')[['latitude', 'longitude']].apply(tuple, axis=1).to_dict()


# In[22]:


coords_df = pd.DataFrame(zip_coords_dict.items(), columns=['Zip Code', 'Coordinates'])
coords_df[['latitude', 'longitude']] = pd.DataFrame(coords_df['Coordinates'].to_list(), index=coords_df.index)
grocery_coords_df = pd.merge(grocery_df, coords_df[['Zip Code', 'latitude', 'longitude']], on='Zip Code', how='left').dropna()
min_merged_df = pd.merge(avg_min_price_df, coords_df[['Zip Code', 'latitude', 'longitude']], on='Zip Code', how='left')
max_merged_df = pd.merge(avg_max_price_df, coords_df[['Zip Code', 'latitude', 'longitude']], on='Zip Code', how='left')


# In[23]:


with open('../../data/raw/LA_County_ZIP_Codes.geojson') as f:
    geojson_data = json.load(f)

# Define colors for each grocery store (for the map)
color_map = {
    'Erewhon': 'red',
    'Whole Foods': 'green',
    'Trader Joe\'s': 'blue',
    'Ralphs': 'purple',
    'Food 4 Less': 'orange'
}
grocery_coords_df['color'] = grocery_coords_df['Store'].map(color_map)

# Plot the heat map for average min price
fig = px.choropleth_mapbox(
    min_merged_df,
    geojson=geojson_data,
    locations='Zip Code',
    featureidkey="properties.ZIPCODE",
    color='Min Price',
    color_continuous_scale='blues',
    mapbox_style="carto-positron",
    center={"lat": 34.05, "lon": -118.25},
    zoom=10,
    title="Heatmap of Minimum Rent Prices by ZIP Code in Los Angeles"
)

# Mark the grocery store on the map
grocery_marker = px.scatter_mapbox(
        grocery_coords_df,
        lat='latitude',
        lon='longitude',
        hover_name='Store',
        title="Grocery Store Locations"
)

fig.add_trace(grocery_marker.data[0])

fig.update_traces(marker=dict(
    size=10, 
    color=grocery_coords_df['color'],
), selector=dict(type='scattermapbox'))

fig.write_html("../../results/images/grocery_store_heatmap_min_price.html")


# In[24]:


# Plot the heat map for average max price
fig = px.choropleth_mapbox(
    max_merged_df,
    geojson=geojson_data,
    locations='Zip Code',
    featureidkey="properties.ZIPCODE",
    color='Max Price',
    color_continuous_scale='blues',
    mapbox_style="carto-positron",
    center={"lat": 34.05, "lon": -118.25},
    zoom=10,
    title="Heatmap of Maximum Rent Prices by ZIP Code in Los Angeles"
)

# Mark the grocery store on the map
grocery_marker = px.scatter_mapbox(
        grocery_coords_df,
        lat='latitude',
        lon='longitude',
        hover_name='Store',
        title="Grocery Store Locations"
)

fig.add_trace(grocery_marker.data[0])

fig.update_traces(marker=dict(
    size=10, 
    color=grocery_coords_df['color'],
), selector=dict(type='scattermapbox'))

fig.write_html("../../results/images/grocery_store_heatmap_max_price.html")


# In[ ]:




