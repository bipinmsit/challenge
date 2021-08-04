* Required Python Package:
	- ogr
	- osr
	- matplotlib
	- rasterio
	- geopandas

* Use case:

usage: challenge.py [-h] [--input_feature INPUT_FEATURE]
                    [--input_dsm INPUT_DSM] [--buffer_dist BUFFER_DIST]

Positively affected physical features by the introduction of a new highway
tunnel

optional arguments:
  -h, --help            show this help message and exit
  --input_feature INPUT_FEATURE
                        Input Vector File
  --input_dsm INPUT_DSM
                        Input Digital Surface Model
  --buffer_dist BUFFER_DIST
                        Buffer Distance From Input Feature