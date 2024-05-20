# Solution: 36613
# Correct!

import rasterio
from rasterio.plot import show
import numpy as np

file = "excercises/intel_7/Hyperspectral Reflectance/input.tif"
band = 90

img = rasterio.open(file)
target_band = img.read(band)
target_band.shape

height = target_band.shape[0]
width = target_band.shape[1]
cols, rows = np.meshgrid(np.arange(width), np.arange(height))
xs, ys = rasterio.transform.xy(img.transform, rows, cols)
lons= np.array(xs)
lats = np.array(ys)

lats = lats[:, 0]
lons = lons[0]


target_cords = [
    (52.2601,5.5738),
    (52.2531,5.9273),
    (52.1301,5.5675),
    (52.0385,5.9261),
    (52.1618,5.7203)
]

values = []
for lat, long in target_cords:    
    # calculate the difference array
    difference_array = np.absolute(lats-lat)
    # find the index of minimum element from the array
    lat_index = difference_array.argmin()
    difference_array = np.absolute(lons-long)
    long_index = difference_array.argmin()
    values.append(target_band[lat_index, long_index])

sum(values)

