import os
import configparser

import pandas as pd
import sqlalchemy
from folium import Map
from folium import plugins
from folium.plugins import HeatMap
from folium import Marker
from folium import Icon

# set the directory
path = os.path.dirname(__file__)
os.chdir(path)

# read in the program variables
config = configparser.ConfigParser()
config.read("gps_config.ini")

# read in the DB variables
user = config["DATABASE"]["user"]
password = config["DATABASE"]["password"]
servername = config["DATABASE"]["servername"]
database = config["DATABASE"]["database"]
gps_query = config['DATABASE']['gps_query']

# read in the folium variables
rad = config["FOLIUM"]["rad"]
hmb = config["FOLIUM"]["hmb"]
hmo = config["FOLIUM"]["hmo"]
hmz = config["FOLIUM"]["hmz"]

# create the sql connection string
connection_string = f'mssql+pymssql://{user}:{password}@{servername}/{database}'
engine = sqlalchemy.create_engine(connection_string)
conn = engine.connect()

# create a pandas dataframe from each query
df = pd.read_sql(gps_query, conn)


#df = pd.read_csv(r'C:\Users\wmayne\Envs\practice\MyPyFiles\gps.csv', dtype=object)

# set the starting location, map type and zoom levels
map_hooray = Map(location=[-28.1750,137.2924],
                        tiles = "Stamen Toner",
                        zoom_start = 4.5)

# add depot markers
Marker([-37.68,144.9538], 
              popup='Campbellfield LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-38.0417,145.1378], 
              popup='Chelsea LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-32.0013,115.9288], 
              popup='Bentley LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-34.9383,138.5726], 
              popup='Adelaide LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-34.7813,138.6365], 
              popup='Salisbury LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)  

Marker([-33.8908,151.0475], 
              popup='Chullora LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray) 

Marker([-33.748,150.6907], 
              popup='Penrith LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-33.3326,151.4055], 
              popup='Berkley Vale LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-32.8316,151.6884], 
              popup='Hexham LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-31.4506,152.8876], 
              popup='Port Macquarie LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-34.9102,150.5813], 
              popup='South Nowra LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-27.4207,153.0851], 
              popup='Eagle Farm LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray) 

Marker([-27.6194,152.726], 
              popup='Wulkaraka LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)  

Marker([-20.7222,139.4908], 
              popup='Mt Isa LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-19.2769,146.6993], 
              popup='Townsville LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray) 

Marker([-42.861,147.2868], 
              popup='Hobart LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray) 

Marker([-41.2059,146.3527], 
              popup='Devonport LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)  

Marker([-41.0398,145.8298], 
              popup='Devonport 2 LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)

Marker([-41.54,147.1917], 
              popup='Launceston LRT',
              icon=Icon(color='red',icon='map-pin', prefix='fa') 
             ).add_to(map_hooray)



# add a logo to the map
from folium.plugins import FloatImage
url = ('https://www.lioncareers.com/wp-content/themes/lion_careers/images/Lion_logo.png')
FloatImage(url, bottom=5, left=85).add_to(map_hooray)

# Ensure you're handing it floats
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)

# Filter the DF for rows, then columns, then remove NaNs
heat_df = df[['Latitude', 'Longitude']]
heat_df = heat_df.dropna()

# List comprehension to make out list of lists
heat_data = [[row['Latitude'],row['Longitude']] for index, row in heat_df.iterrows()]


# Plot it on the map
HeatMap(heat_data,radius=10,heatmap_blur=2,heatmap_min_opacity=0.6,heatmap_max_zoom=4).add_to(map_hooray)

# Display the map
map_hooray.save(outfile= "test.html")