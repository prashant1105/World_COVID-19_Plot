# World_COVID-19_Plot
This repository contains Jupyter Notebook for plotting of real time data on COVID-19 cases around the world.


Libraries Used: numpy for Math related Operations (very less used) pandas for DataFrame and reading the DatasEt. Folium: for creating Maps of India and plotting number of current cases against each state. Folium is a powerful Python library that helps us to create several types of Leaflet maps. The fact that the Folium results are interactive makes this library is very useful for dashboard building. requests: for getting the data from the URL. urllib.request BeautifulSoup: for Scraping the data from Google News page about COVID-19 cases and transforming it to Pandas Dataframe Matplotlib Seaborn: For creating Piechart and Histograms.

DataSet Columns: Country_Code : This column includes the Country Codes of the Countries around the World. (Less Important) Latitude : Latitude of each country. (Most Important)*** Longitude : Longitude of each country of the world. (Most Important)*** Country_Name : This column includes the Country Names of the Countries around the World. (Most Important)

*** From the dataset I have used only 3 columns namely, 'Country_Name', 'Latitude', 'Longitude'. 

For number of cases I have used the Google News statistics with source being Wikipedia. Link of Source: https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
