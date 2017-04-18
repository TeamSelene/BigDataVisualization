# PyMongo for MongoDB queries
from pymongo import MongoClient
from collections import OrderedDict

# import gsconfig stuff
import geoserver
import geoserver.util
from geoserver.catalog import Catalog

# MatPlotLib for colors and basic plotting
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Numpy for super fast arrays
import numpy as np
import pymongo
import pandas as pd
import json

from osgeo import gdal
from osgeo import osr

# Bokeh + Datashader
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import export_image

from pygs.utils.utils import hash_string
from pygs.utils._spectralprofiler import wavelengths

class SpectralProfiler(object):

    def __init__(self, host, port=27017, user=None, password=None):
        """
        Attributes
        ----------

        host : string
               The hostname for the database

        port : integer
               The port number for the database

        user : string
               Database user

        client : connection
                 Connection object to the database

        images : collection
                Collection object for sp images

        image_angles : collection
                       collection for sp images index on (incidence, emission)

        raster : image
                 The raster image generated from the dataframe
        """

        self.host = host
        self.port = port
        self.user = user

        self.client = MongoClient(host, port)
        self.db = self.client["selene"]

        if user and password:
            self.client.selene.authenticate(user, password)

        self.images = self.client.selene.images
        self.image_angles = self.client.selene.image_angles

    def compute_dataframe(self, query, projection=None, field="ref1", collection = "images", wavelengths = wavelengths, *args, **kwargs):
        """
        Parameters
        ----------

        query : dict
                dictionary representing the query

        projection : dict
                     dictionary representing the projection

        field : string
                Collection field used to generate dataframe

        collection : string
                     Collection to query on

        wavelengths : list
                      Wavelengths to generate dataframe on
        """
        if not projection:
            projection = {"_id" : False, "loc": True}
        else:
            projection["_id"] = False
            projection["loc"] = True

        results = self.db[collection].find(query, projection, *args, **kwargs)
        result_list = list(results)

        points = []
        for i in range(len(result_list)):
            data_dict = result_list[i]
            if collection == 'images':
                data_list = [data_dict['loc']['coordinates'][0], data_dict['loc']['coordinates'][1]]
            else:
                data_list = [data_dict['coords'][0], data_dict['coords'][1]]
            data_list.extend(list(np.frombuffer(data_dict[field], dtype='f4')))
            points.append(data_list)

        refs = np.asarray(points)
        header = np.asarray(['long', 'lat'] + wavelengths)
        self.dataframe = pd.DataFrame(data=refs, columns=header)
        return self.dataframe


    def compute_image(self, w, h, map_scheme='bone', wavelength='770.7', bg=None):
        """
        Parameters
        ----------

        w : integer
            width of the image

        h : integer
            height of the image

        map_scheme : string
                     matplotlib color scheme

        wavelength : string
                     which wavelength to select for the image

        bg : string
             Hex string representing the background color for the image, None = transperent

        """
        # Use the bone color map to make it look more moon-like
        cmap = plt.get_cmap(map_scheme)

        canvas = ds.Canvas(plot_width=w, plot_height=h)

        agg = canvas.points(self.dataframe, 'long', 'lat', ds.mean(wavelength))
        img = tf.shade(agg, cmap=cmap)
        self.raster = ds.transfer_functions.set_background(img, bg)
        return self.raster

    def save_image(self, filename):
        """
        Jacked from Pablo on StackOverflow
        (http://gis.stackexchange.com/questions/58517/python-gdal-save-array-as-raster-with-projection-from-other-file)

        Parameters
        ----------

        filename : string
                   The path to save the image to
        """
        dst_filename = filename
        array = np.asarray(self.raster.to_pil())
        x_pixels = self.raster.shape[1]  # number of pixels in x
        y_pixels = self.raster.shape[0]  # number of pixels in y
        PIXEL_SIZE = 1  # size of the pixel...
        lon = self.dataframe["long"]
        lat = self.dataframe["lat"]  # x_min & y_max are like the "top left" corner.
        wkt_projection = 'WGS84'

        driver = gdal.GetDriverByName('GTIFF')

        dataset = driver.Create(
            dst_filename,
            x_pixels,
            y_pixels,
            1,
            gdal.GDT_Byte)

        xmin, ymin, xmax, ymax = [min(lon), min(lat), max(lon), max(lat)]
        xres = (xmax - xmin) / float(x_pixels)
        yres = (ymax - ymin) / float(y_pixels)
        geotransform = (xmin, xres, 0, ymax, 0, -yres)

        srs = osr.SpatialReference()            # establish encoding
        srs.ImportFromEPSG(3857)                # WGS84 lat/long
        # dataset.SetProjection(srs.ExportToWkt()) # export coords to file
        dataset.SetGeoTransform(geotransform)

        dataset.GetRasterBand(1).WriteArray(array[:,:,0])
        # dataset.GetRasterBand(2).WriteArray(array[:,:,1])
        # dataset.GetRasterBand(3).WriteArray(array[:,:,2])
        dataset.FlushCache()  # Write to disk.
        dataset = None
