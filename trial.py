from pystac_client import Client
from pystac import ItemCollection, Item
from odc.stac import stac_load
from pyproj import CRS
import logging
import sys
from xarray import Dataset
from pyproj import Proj
import rioxarray
import geopandas as gpd
from branca.element import Figure
import folium
import folium.plugins
import shapely.geometry
import matplotlib.pyplot as plt
from os import makedirs
import os.path as op
import requests

def s3_to_local(item: dict, dl_folder: str) -> dict:
    """Take in pystac item, download its assets, and update the asset href to point
    to dl location.
    Args:
        item (pystac.Item): the item to download the assets for
        dl_folder (str): the path to put the files
    Returns:
        item (pystac.Item): the item with downloaded assets and updated asset hrefs
        
    """

    for k in item["assets"].keys():
        if k in bands:
            fn = op.basename(item["assets"][k]["href"])
            f_path = op.join(dl_folder, fn)
            if not op.exists(f_path):
                with requests.get(item["assets"][k]["href"], timeout=60, stream=True) as r:
                    r.raise_for_status()
                    with open(f_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
            item["assets"][k]["href"] = f_path

    return item

def download_items_to_local(item_col: ItemCollection, bands: list, wkdir: str) -> ItemCollection:
    """Download items locally, using appropriate download method.
    Args:
        item_col (pystac.ItemCollection): item collection with remote asset hrefs to download
        wkdir (str): local working dir to use, make if not exist
    Returns:
        local_ic (pystac.ItemCollection): item collection with local asset hrefs
    """

    makedirs(wkdir, exist_ok=True)

    items_local = []

    for item in item_col:
        logging.info("Downloading assets for item: %s", item.id)
        dl_dir = op.join(wkdir, item.id)
        makedirs(dl_dir, exist_ok=True)
        item = Item.from_dict((s3_to_local(item=item.to_dict(), dl_folder=dl_dir)))
        items_local.append(item)

    local_ic = ItemCollection(items=items_local)

    return local_ic

toms_run = gpd.read_file("TomsRun.geojson")
toms_bbox = toms_run.total_bounds

api_url = "https://earth-search.aws.element84.com/v0"
collection = "sentinel-s2-l2a-cogs"
# Opening and searching through the satellite imagery
client = Client.open(api_url)
search = client.search(
    collections=[collection],
    bbox=toms_bbox,
    datetime=['2022-07-01', '2023-03-22'],
    max_items=25,
    query=["eo:cloud_cover<10"]
)

print(f"Scenes matching search: {search.matched()}")
# Collecting the items that match the search criteria
items = search.get_all_items()
bands = ["B02", "B03", "B04"]
print(f"Number of items: {len(items)}")
item = items[22]
item = item.to_dict()
output_crs = CRS.from_epsg(items[0].properties["proj:epsg"])

assets = items[9].assets
print(assets["overview"].href)
print(assets["B08"].href)

b08 = rioxarray.open_rasterio(assets["B08"].href)
print(b08)
b08.rio.to_raster("BO8.tif")
# dc = stac_load(
#     items=items,
#     resolution=10,
#     groupby="solar_day",
#     crs=output_crs,
#     bbox=toms_bbox
# )


# items = download_items_to_local(items, bands, "./sat_image")
