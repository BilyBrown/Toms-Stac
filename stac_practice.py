from pystac_client import Client
from pystac import ItemCollection
from odc.stac import stac_load
from pyproj import CRS
import logging
import sys
from xarray import Dataset
from pyproj import Proj
import rioxarray
import geopandas as gpd

# Bring in geometry I want to analyze
toms_run = gpd.read_file("TomsRun.geojson")
toms_bbox = toms_run.total_bounds

# The product and product location I want to search through
api_url = "https://earth-search.aws.element84.com/v0"
collection = "sentinel-s2-l2a-cogs"

# Opening and searching through the satellite imagery
client = Client.open(api_url)
search = client.search(
    collections=[collection],
    bbox=toms_bbox,
    datetime=['2023-01-01', '2023-03-20'],
    max_items=10,
    query={"eo:cloud_cover": {"lt": 20, "gte":0}}
)

# Collecting the items that match the search criteria
items = search.get_all_items()

output_crs = CRS.from_epsg(items[0].properties["proj:epsg"])

dc = stac_load(
    items=items.items,
    bands=["B02", "B03", "B04"],
    resolution=10,
    crs=output_crs,
    bbox=toms_bbox
)

print(dc)