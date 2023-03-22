# Toms-Stac

### Overview
This repo is a playground where I am trying to understand how to use `pystac-client`: https://pystac-client.readthedocs.io/en/stable/usage.html, `odc-stac`: https://odc-stac.readthedocs.io/en/latest/intro.html, and `rasterio`/ `xarray`: https://rasterio.readthedocs.io/en/latest/quickstart.html.

So far I am just bashing my head on my keyboard and seeing what sticks. I currently have an issue where I cannot access the data from the searched stac items. This rears its head when I try to create a datacube as well as save a tif file with `rio.to_raster()` with the href of a scene.

### Goals:
- To search for satellite imagery for a given project area
- Perform basic land cover analysis on the project area
- Determine if there has been land cover change over time (de-forestation is my main interest)
- Track the change over time and display it over time (with animations)

#### Future Goals:
- to leverage machine learning on the images to determine site quality changes to forests over time (thinnings/natural disturbances) and how this affects the biomass of the area.


#### Resources used so far:
- PyStac tutorial - https://carpentries-incubator.github.io/geospatial-python/05-access-data/index.html
- ODC tutorial - https://odc-stac.readthedocs.io/en/latest/notebooks/stac-load-e84-aws.html
- Time Series Observation Data Cubes - https://github.com/e-sensing/sits
