import pandas as pd
import geojson
from shapely.geometry import shape, Point

# Load the drone data
df = pd.read_csv("opdrachten\intel3_Hostiledrone\input\input.csv")
# We are only interested in the cases where the drones reported being in NL.
df = df[df.Inside_NL == False]

# Load in the geo data and get the edge.
geo_json_path = "opdrachten\intel3_Hostiledrone\input\polygon_NL.geojson"
with open(geo_json_path) as f:
    gj = geojson.load(f)
features = gj['features'][0]["geometry"]
nl_polygon = shape(features)

def in_nl(row, nl_polygon):
    """
    Function that checks if the observation is within
    the NL polygon.
    """
    point = Point(row.Longitude, row.Latitude)
    if nl_polygon.contains(point):
        print(row.ID_num)
    
# Loop across the rows - print the drone ID of the drone in NL 
_ = df.apply(in_nl, axis=1, nl_polygon=nl_polygon)

# Answer was printed in the previous step.
314426
# Correct!