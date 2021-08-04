from osgeo import ogr
import osr
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd
import subprocess
import argparse
import os

"""
Automated script to find positively affected physical features by the introduction of a new highway tunnel.

Author: Bipin kumar
Date: 04th August 2021
"""


def get_args():
    parser = argparse.ArgumentParser(
        description="Positively affected physical features by the introduction of a new highway tunnel"
    )
    parser.add_argument("--input_feature", type=str, help="Input Vector File")
    parser.add_argument("--input_dsm", type=str, help="Input Digital Surface Model")
    parser.add_argument(
        "--buffer_dist", type=float, help="Buffer Distance From Input Feature"
    )

    return parser.parse_args()


def createBuffer(inputfn, bufferDist):
    print(os.path.dirname(os.path.dirname(inputfn)))
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'\python_code_outputs')

    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    outputBufferfn = os.path.join(final_directory, "buffer_{}m.shp".format(bufferDist))
    inputds = ogr.Open(inputfn)
    inputlyr = inputds.GetLayer()

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3857)

    shpdriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outputBufferfn):
        shpdriver.DeleteDataSource(outputBufferfn)
    outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
    bufferlyr = outputBufferds.CreateLayer(
        outputBufferfn, srs, geom_type=ogr.wkbPolygon
    )
    featureDefn = bufferlyr.GetLayerDefn()

    for feature in inputlyr:
        ingeom = feature.GetGeometryRef()
        geomBuffer = ingeom.Buffer(bufferDist)

        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geomBuffer)
        bufferlyr.CreateFeature(outFeature)
        outFeature = None

    return outputBufferfn


def createHillShade(input_dsm):
    output_dir = os.path.join(os.getcwd(), r'/python_code_outputs')
    output_name = os.path.basename(input_dsm).split(".")[0]
    hillshade = os.path.join(output_dir, output_name + "_hillshade.tif")
    subprocess.run(
        ["gdaldem", "hillshade", "-z", "5", input_dsm, hillshade,]
    )

    return os.path.abspath(hillshade)


def main(inputfn, bufferDist, input_dsm):
    outputBufferfn = createBuffer(inputfn, bufferDist)
    hillshade_path = createHillShade(input_dsm)

    print("YOUR FINAL OUTPUT IS CREATED AT {}".format(os.path.join(os.getcwd(), r'/python_code_outputs')))

    #     Plot the outputs

    # Digital Surface Model
    dsm = rasterio.open(hillshade_path)

    # Buffer Boundary
    buffer_boundary = gpd.read_file(outputBufferfn)

    fig, ax = plt.subplots(1, figsize=(8, 12))

    # Plot dsm & buffer boundary
    show((dsm, 1), ax=ax)
    buffer_boundary.boundary.plot(
        edgecolor="red", ax=ax, label="350 meters buffer line"
    )

    # Plot up to the extent of buffer boundary
    plt.locator_params(nbins=4)
    plt.xlim([484500, 486400])
    plt.ylim([6786700, 6790600])

    plt.title(
        "Positively affected buildings by the introduction of a new highway tunnel"
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    args = get_args()
    main(args.input_feature, args.buffer_dist, args.input_dsm)
