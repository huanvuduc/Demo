# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/geemap/tree/master/examples/template/template.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/geemap/blob/master/examples/template/template.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/geemap/blob/master/examples/template/template.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://github.com/giswqs/geemap). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.

**Important note**: A key difference between folium and ipyleaflet is that ipyleaflet is built upon ipywidgets and allows bidirectional communication between the front-end and the backend enabling the use of the map to capture user input, while folium is meant for displaying static data only ([source](https://blog.jupyter.org/interactive-gis-in-jupyter-with-ipyleaflet-52f9657fa7a)). Note that [Google Colab](https://colab.research.google.com/) currently does not support ipyleaflet ([source](https://github.com/googlecolab/colabtools/issues/60#issuecomment-596225619)). Therefore, if you are using geemap with Google Colab, you should use [`import geemap.eefolium`](https://github.com/giswqs/geemap/blob/master/geemap/eefolium.py). If you are using geemap with [binder](https://mybinder.org/) or a local Jupyter notebook server, you can use [`import geemap`](https://github.com/giswqs/geemap/blob/master/geemap/geemap.py), which provides more functionalities for capturing user input (e.g., mouse-clicking and moving).
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# Checks whether this notebook is running on Google Colab
try:
    import google.colab
    import geemap.eefolium as geemap
except:
    import geemap

# Authenticates and initializes Earth Engine
import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()  

# %%
"""
## Create an interactive map 
The default basemap is `Google Maps`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
"""

# %%
Map = geemap.Map(center=[40,-100], zoom=4)
Map

# %%
"""
## Add Earth Engine Python script 
"""

# %%
# Add Earth Engine dataset
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


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map