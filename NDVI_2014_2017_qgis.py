import ee 
from ee_plugin import Map 

# To find the images that are available in a specific date in a specific time, we need to create an image collection first.

# The image collection can filtered with location of the points and dates of two time periods.
# In this example, I have chosen first image during the month of July in 2014 and 2017
# # Creating Image Collection of July 2014
imageCol2014 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(ee.Geometry.Point(98.5265, 20.4715)) \
    .filterDate('2014-07-01', '2014-07-30')

# # Creating Image Collection of July 2017
imageCol2017 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(ee.Geometry.Point(98.5265, 20.4715)) \
    .filterDate('2017-07-01', '2017-07-30')

# Checking the image collection
print(imageCol2014)

# The first image can be selected with .first() command. However, to do with more flexible calling of
# an image from a image collection, I did it with list.

# Converting the list and selecting the first image
# for 2014
listCol2014 = imageCol2014.toList(50)
img2014 = ee.Image(listCol2014.get(0))
# for 2017
img2017 = ee.Image(imageCol2017.first())

# Checking the image
print(img2017)


# NDVI can be calculated using expression
# # NDVI for 2014
ndvi2014 = img2014.expression(
'(NIR - RED) / (NIR + RED)' , {
'NIR' : img2014.select('B4'),
'RED' : img2014.select('B3')
} ) 

# NDVI can be calculated using math operation
# # NDVI for 2017
ndvi2017 = img2017.select('B4').subtract(img2017.select('B3')) \
.divide(img2017.select('B4').add(img2017.select('B3')))

# Load the land mask from the SRTM DEM.
landMask = ee.Image('CGIAR/SRTM90_V4').mask()

# Analyzing the difference
ndviChange = ndvi2017.subtract(ndvi2014)

# Updating the land mask
ndviUp = ndviChange.updateMask(landMask)

# Ploting in map layer
Map.centerObject(ndvi2017, 9)
Map.addLayer(ndviUp, { 'min':-0.3, 'max': 0.3, 'palette': [ 'FFFFFF', '0000FF', 'FF0000']}, "Changes of NDVI  from 2014 to 2017" )
