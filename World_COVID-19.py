#!/usr/bin/env python
# coding: utf-8

# ### INTRODUCTION

# In this notebook, I have studied the current cases of COVID-19 from around the world and mapped them with respective number of Confirmed Cases and number of Deaths for each country around the world. To do that, I have used a Python visualization library, namely Folium. The main point behind using Folium is that it was developed for the sole purpose of visualizing geospatial data. While other libraries are available to visualize geospatial data, such as plotly, they might have a cap on how many API calls we can make within a defined time frame. Folium, on the other hand, is completely free.

# ### Exploring Datasets with pandas

# For this particular problem I have used the CSV file "counties-geographic-coordinates" as the dataset. This file contains total of 4 columns namely 'Country_Code' i.e. The Country Code, 'Latitude', 'Longitude' and 'Country_Name' i.e. the Country Name. Each row represents a Country. For this problem, however we will be using only three columns namely 'Name', 'Latitude' and 'Longitude'. As, for COVID-19 cases we will be scrapping the Google News website to get latest data everytime we run this notebook.

# In[1]:


# Importing the NumPy and the Pandas Library.
import numpy as np
import pandas as pd


# In[2]:


# The location of the file on the Device (or on the server). 
# After that we are storing the data from the csv file into the variable 'data'.
location = '/home/prashant_pk/Desktop/PK/World_COVID19/countries.csv'
data = pd.read_csv(location)


# In[3]:


data.head()


# In[4]:


# Now, I have reduced the columns of the data, so as to contain only necessary information that I require.
df = data[['Country_Name', 'Latitude', 'Longitude']]


# In[5]:


df.head()


# In[6]:


# Setting the name of the State or Union Territory as the index of the Dataframe.
df.set_index(['Country_Name'], inplace = True)


# In[7]:


df.head()


# ### Using Folium

# Folium is a powerful Python library that helps us to create several types of Leaflet maps. The fact that the Folium results are interactive makes this library is very useful for dashboard building.

# In[8]:


#!conda install -c conda-forge folium=0.5.0 --yes
import folium
print('Folium successfully imported!')


# Generating the world map is straigtforward in Folium. We simply create a Folium Map object with parameters 'location', 'zoom_start' or any other and then display it. What is attactive about Folium maps is that they are interactive, so we can very easily zoom into any region of interest despite the initial zoom level.

# In[9]:


# Defining the world map.
world_map = folium.Map(zoom_start = 2)


# In[10]:


world_map


# ### Scraping the data from Google News page about COVID-19 cases and transforming it to Pandas Dataframe

# In[11]:


import requests
import urllib.request
import time
from bs4 import BeautifulSoup


# Getting the URL of the page and creating a request using requests.get() to get the data from the page.

# In[12]:


url = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
response = requests.get(url)


# In[13]:


response  # Here in the output [200] means that it went through


# Scraping the Google News Page content with the help of BeautifulSoup

# In[14]:


soup_data = BeautifulSoup(response.text, "html.parser")


# Now we will clean the Data so as to get desired data only. After that we will convert the content of the Google News page into a table.

# In[15]:


web_data = []
for tr in soup_data.tbody.find_all('tr'):
    web_data.append([ td.get_text().strip() for td in tr.find_all('td')])


# In[16]:


web_data


# Now, we will create the dataframe of the 'web_data' table that contains our data values.

# In[17]:


cases_df = pd.DataFrame(web_data, columns = ['Cases', 'Death', 'Recovered', 'Ref'])


# In[18]:


cases_df.dropna(axis = 0, inplace = True)
cases_df = cases_df.iloc[0 : , : ]
cases_df


# In[19]:


cases_df.reset_index(inplace = True)
cases_df.drop(columns = ['index', 'Ref'], axis = 0, inplace = True)
cases_df.head()


# In[20]:


cases_df.shape


# In[21]:


country_name = []
for th in soup_data.tbody.find_all('th'):
    country_name.append([ a.get_text().strip() for a in th.find_all('a')])


# In[22]:


country_name


# In[23]:


country_df = pd.DataFrame(country_name, columns = ['Country_Name', 'None'])
country_df


# In[24]:


country_df.dropna(axis = 0, how = 'all', inplace = True)
country_df


# In[25]:


country_df = country_df.iloc[5 : , :]
country_df


# In[26]:


country_df.reset_index(inplace = True)
country_df.drop(columns = ['index', 'None'], axis = 0, inplace = True)
country_df.head()


# In[27]:


country_df.shape


# In[ ]:





# In[28]:


country_cases_df = country_df.merge(cases_df, left_index = True, right_index = True)


# In[29]:


country_cases_df


# In[30]:


country_cases_df.set_index(['Country_Name'], inplace = True)
country_cases_df.head()


# In[ ]:





# After that I have merged the Countries dataFrame that contains the Country Name, Latitude and Longitude of all the states of India with the Cases DataFrame that contains the number of cases with respect to the Country names. This is the final DataFrame that I have used in the notebook.

# In[31]:


final_cases_df = df.merge(country_cases_df, left_index = True, right_index = True)


# In[32]:


final_cases_df.head()


# In[33]:


final_cases_df.reset_index(inplace = True)


# In[34]:


final_cases_df.rename(columns = {'index' : 'Country_Name'}, inplace = True)


# In[35]:


final_cases_df.head()


# In[36]:


folium_cases_df = final_cases_df[['Country_Name', 'Latitude', 'Longitude', 'Cases', 'Death', 'Recovered']]


# In[37]:


final_cases_df.head()


# In[38]:


folium_cases_df.head()


# In[39]:


final_cases_df['Cases'] = final_cases_df['Cases'].str.replace(',', '')
final_cases_df['Death'] = final_cases_df['Death'].str.replace(',', '')
final_cases_df['Recovered'] = final_cases_df['Recovered'].str.replace(',', '')

final_cases_df['Cases'] = final_cases_df['Cases'].str.replace('—', '0')
final_cases_df['Death'] = final_cases_df['Death'].str.replace('—', '0')
final_cases_df['Recovered'] = final_cases_df['Recovered'].str.replace('—', '0')

final_cases_df['Cases'] = final_cases_df['Cases'].str.replace('No data', '0')
final_cases_df['Death'] = final_cases_df['Death'].str.replace('No data', '0')
final_cases_df['Recovered'] = final_cases_df['Recovered'].str.replace('No data', '0')


# In[40]:


final_cases_df[['Cases', 'Death', 'Recovered']] = final_cases_df[['Cases', 'Death', 'Recovered']].astype(int)


# In[41]:


final_cases_df


# In[42]:


total_cases_worldwide = final_cases_df['Cases'].sum(axis = 0, skipna = True)
total_death_worldwide = final_cases_df['Death'].sum(axis = 0, skipna = True)
total_recovered_worldwide = final_cases_df['Recovered'].sum(axis = 0, skipna = True)


# In[43]:


total_cases = f'{total_cases_worldwide:,}'
print('Total Number of COVID-19 Cases around the World are: ', total_cases)


# In[44]:


total_deaths = f'{total_death_worldwide : ,}'
print('Total Number of Deaths due to COVID-19 around the World are: ', total_deaths)


# In[45]:


total_recovered = f'{total_recovered_worldwide : ,}'
print('Total Number of Recovered Cases due to COVID-19 around the World are: ', total_recovered)


# In[ ]:





# In[46]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[47]:


count, bin_edges = np.histogram(final_cases_df['Cases'])

final_cases_df['Cases'].plot(kind='hist', figsize=(8, 5), xticks = bin_edges)

plt.title('Number of Countries with a particular range of cases') # add a title to the histogram
plt.ylabel('Number of Countries') # add y-label
plt.xlabel('Number of Cases') # add x-label

plt.show()


# In the above plot, the x-axis represents the range of Confirmed Cases in intervals of 1151. The y-axis represents the number of states that contributed to the aforementioned cases.
# 
# From the plot we can conclude that almost 25 countries have cases between 1 to 1152, while only one state of India has greater than 10000 number of cases.

# In[48]:


max_cases_df = final_cases_df.sort_values(['Cases'], ascending = False).head(10)
max_cases_df


# In[49]:


explode_list = [0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1]
max_cases_df['Cases'].plot(
                            kind = 'pie',
                            figsize = (15, 6),
                            autopct = '%1.1f%%', 
                            startangle = 45,    
                            shadow = True,       
                            labels = None,         # turn off labels on pie chart
                            pctdistance = 1.12,    # the ratio between the center of each pie slice and the start of the text generated by autopct 
                            explode = explode_list
                            )

plt.title('Confirmed Cases around the World w.r.t. each Country')
plt.axis('equal')

# add legend
plt.legend(labels = max_cases_df['Country_Name'], loc='upper right') 

plt.show()


# In[ ]:





# In[50]:


max_deaths_df = final_cases_df.sort_values(['Death'], ascending = False).head(10)
max_deaths_df


# In[51]:


explode_list1 = [0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1]

max_deaths_df['Death'].plot(
                            kind = 'pie',
                            figsize = (15, 6),
                            autopct = '%1.1f%%', 
                            startangle = 45,    
                            shadow = True,       
                            labels = None,         # turn off labels on pie chart
                            pctdistance = 1.12,    # the ratio between the center of each pie slice and the start of the text generated by autopct 
                            explode = explode_list
                            )

plt.title('Confirmed Deaths around the World w.r.t. each Country')
plt.axis('equal')

# add legend
plt.legend(labels = max_cases_df['Country_Name'], loc='upper right') 

plt.show()


# In[ ]:





# In[ ]:





# In[52]:


# Defining the world map.
world_map = folium.Map(location = [0, 0], zoom_start = 2)
world_map


# In[53]:


# Instantiating a feature group for the cases in the dataframe.

cases = folium.map.FeatureGroup()


for lat, lng, in zip(folium_cases_df.Latitude, folium_cases_df.Longitude):
    cases.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius = 2, # define how big you want the circle markers to be
            color = 'yellow',
            fill = True,
            fill_color = 'blue',
            fill_opacity = 0.6
        )
    )


# In[54]:


# Adding Cases to the map of India
world_map.add_child(cases)


# In[55]:


# Instantiating a feature group for the cases in the dataframe.
cases = folium.map.FeatureGroup()

# Looping through the cases and adding each to the cases feature group
for lat, lng, in zip(folium_cases_df.Latitude, folium_cases_df.Longitude):
    cases.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius = 2, # define how big you want the circle markers to be
            color = 'yellow',
            fill = True,
            fill_color = 'blue',
            fill_opacity = 0.2
        )
    )
    
# Adding a pop-up text for each marker on the map
latitudes = list(folium_cases_df.Latitude)
longitudes = list(folium_cases_df.Longitude)
labels = list(folium_cases_df.Cases)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(world_map)    
    
# Adding Cases to the map of the World
world_map.add_child(cases)


# In[56]:


# Instantiating a feature group for the deaths in the dataframe.
deaths = folium.map.FeatureGroup()

# Looping through the cases and adding each to the cases feature group
for lat, lng, in zip(folium_cases_df.Latitude, folium_cases_df.Longitude):
    deaths.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=2, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# Adding a pop-up text for each marker on the map
latitudes = list(folium_cases_df.Latitude)
longitudes = list(folium_cases_df.Longitude)
labels = list(folium_cases_df.Death)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(world_map)    
    
# Adding Cases to the map of the world
world_map.add_child(deaths)


# show map
world_map


# In[ ]:





# In[ ]:





# In[ ]:





# In[57]:


# download countries geojson file
#!wget --quiet https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/world_countries.json -O world_countries.json
    
print('GeoJSON file downloaded!')


# In[ ]:





# In[58]:


world_geo = r'world_countries.json' # geojson file

# create a plain world map
world_map = folium.Map(location=[0, 0], zoom_start=2)

threshold_scale = np.linspace(final_cases_df['Cases'].min(),
                              final_cases_df['Cases'].max(),
                              6, dtype = int)
threshold_scale = threshold_scale.tolist() # change the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1 # make sure that the last value of the list is greater than the maximum immigration


# let Folium determine the scale.

world_map.choropleth(
    geo_data = world_geo,
    data = final_cases_df,
    columns = ['Country_Name', 'Cases'],
    key_on = 'feature.properties.name',
    threshold_scale = threshold_scale,
    fill_color = 'YlOrRd', 
    fill_opacity = 0.7, 
    line_opacity = 0.2,
    legend_name = 'Total Number of Cases around the World'
)

world_map


# In[ ]:




