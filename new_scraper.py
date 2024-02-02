from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver



time.sleep(10)

new_planets_data = []

def scrape_more_data(url):
    print(url)
    
    ## ADD CODE HERE ##
    try: 
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        star_table = soup.find_all('table')
        table_rows = star_table[7].find_all('tr')
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class":"Headersort"}):
            th_tags = tr_tag.find_all("td")
            for th_tag in th_tags:
                try:
                    temp_list.append(th_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)                   
        scrape_more_data(url) 

planet_df_1 = pd.read_csv("bright_stars.csv")

# Call method
for index, row in planet_df_1.iterrows():

     ## ADD CODE HERE ##
    print(row["url"])
    scrape_more_data(row["url"])
     # Call scrape_more_data(<hyperlink>)

    print(f"Data Scraping at url {index+1} completed")

print(new_planets_data)

# Remove '\n' character from the scraped data
bright_stars_data = []

for row in new_planets_data:
    replaced = []
    ## ADD CODE HERE ##
    for el in row:
        el = el.replace("\n","")
        replaced.append(el) 

    bright_stars_data.append(replaced)

print(bright_stars_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(bright_stars_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")