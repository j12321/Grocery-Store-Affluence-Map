[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7A__rrid)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=17479245&assignment_repo_type=AssignmentRepo)
# DCSI 510 Final Project 
## Grocery Store Affluence Map: Correlating Store Locations with LA Property Prices

This is the final project for DSCI 510.

This project aims to examine whether the locations of certain grocery stores are linked to rental costs in Los Angeles.
The code is divided into four parts: get_data, clean_data, analyze_data, and visualize_results. Below are detailed instructions on how to set up and run the project.

## Prerequisites
### Required Packages
Please install the following Python packages: pandas, numpy, time, random, crawlbase, request, beautifulsoup, selenium, webdriver-manager, geopy, json, functools, matplotlib, plotly, and geopandas.

### Notes on ChromeDriver and Selenium
For web scraping involving Selenium, a Chrome browser is required. This project uses ChromeDriverManager() from the webdriver-manager package to manage compatibility between ChromeDriver and the version of Chrome due to a mismatch between the version of my ChromeDriver and the version of my Google Chrome.

## Project Structure
1. ### get_data

This folder contains 5 .py files for web scraping 5 different websites: [Apartments.com](https://www.apartments.com/los-angeles-ca/1-bedrooms/), [Erewhon](https://erewhon.com/locations), [Whole Foods](https://www.wholefoodsmarket.com/stores), [Trader Joe's](https://locations.traderjoes.com/ca/los-angeles/), and [Ralphs](https://www.ralphs.com/stores/search?referrer=link_hub&searchText=los%20angeles&selectedPage=1).

Note that Crawlbase / CrawlingAPI is used for web scraping for Apartments.com and Trader Joe's, please fill in your user token. For more information, please visit https://crawlbase.com/docs/crawling-api/. 

In addition, due to a mismatch between the version of ChromeDriver and the version of my Google Chrome, I used ChromeDriverManager() before using webdriver. There may be a difference between users.


2. ### clean_data
   
This folder contains 6 .py files.

To run the USZips_clean_data.py, please download USZips.csv file manually from https://www.kaggle.com/datasets/joeleichter/us-zip-codes-with-lat-and-long.

In addition, please download LA County ZIP Codes GeoJSON file from https://geohub.lacity.org/datasets/lacounty::la-county-zip-codes/about before running further code.


3. ### analyze_data

This folder contains 1 .py file and a resulting .json file.

The json file is created after running analyze_data.py.



4. ### visualize_results
   
This folder contains 1 .py file.

The results after running visualize_results.py will be saved to results/images/. 

Note that if you can't see grocery_store_heatmap_max_price.html and grocery_store_heatmap_min_price.html, please view the following link [grocery_store_heatmap_max_price](https://drive.google.com/uc?id=1YCcC8m_Q0JR1qUcR4VDY7ZHNHn-_Ymbv) and [grocery_store_heatmap_min_price](https://drive.google.com/uc?id=1Ri1xk29L77VATXFKVBTk1id__l2D1SGH). You can see the interactive heat maps after downloading and opening them.

## Data Files
1. Raw and Processed data
   
The raw data and processed data will automatically be saved after running get_data.py and clean_data.py.

2. Maunally Downloaded Files
   
Please download USZips.csv and LA_County_ZIP_Codes.geojson manually as mentioned above.


Thank you so much!
