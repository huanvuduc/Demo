import ee 
from ee_plugin import Map 



# Create the title label.
title = ui.Label('Nitrogen dioxide CONCENTRATIONS Map as of February 2020')
title.style().set('position', 'top-center')
Map.add(title)
# get the data
y2019 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2").filterDate("2019-02-01","2019-02-28")
y2020 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2").filterDate("2020-02-01","2020-02-28")

# get the layer with all countries
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq("country_na", "Thailand"))

# add layers to map
Map.setCenter(107.013905, 16.566622,5)
Map.addLayer(y2019.max().select("NO2_column_number_density").clip(countries),{'min':0.00002, 'max':0.0005, 'palette':"lightblue,orange,yellow,red,purple"},"Feb 2019")
Map.addLayer(y2020.max().select("NO2_column_number_density").clip(countries),{'min':0.00002, 'max':0.0005, 'palette':"lightblue,orange,yellow,red,purple"},"Feb 2020")

