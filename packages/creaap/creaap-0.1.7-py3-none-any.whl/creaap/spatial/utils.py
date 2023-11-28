from io import BytesIO
import numpy as np
import pandas as pd
import os
import shapefile

import shapely as sp
import ssl
import urllib.request
import zipfile

from shutil import rmtree
from sklearn.neighbors import NearestNeighbors, BallTree
from pyproj import Proj, Transformer, transform

from math import *

# important helper function
pRad = 6356.7523142
EqRad = 6378.137

def get_earth_radius(siteLatitude):
    '''
    Returns the Earth's radius at a certain latitude

    Parameters
    ----------
    siteLatitude: float
        the latitude (in degrees) of your location
    '''
    return pRad + (90 - abs(siteLatitude)) / 90 * (EqRad - pRad)

def distance_to_bounds(lon, lat, boundaries):
    '''
    This function will create a numpy array of distances
    to a certain boundary, like a shore. It will contain and ID for AIS points and
    the distance to the nearest coastline point.
    '''
    coastline_coords = boundaries
    tree = BallTree(np.radians(coastline_coords), metric='haversine')
    coords = pd.concat([np.radians(lon), np.radians(lat)], axis=1)
    dist, ind = tree.query(coords, k=1)
    # dists is in rad; convert to km
    df_distance_to_shore = pd.Series(dist.flatten()*get_earth_radius(lat), name='distance_to_bound')
    df_lat = pd.Series(coastline_coords[ind].flatten()[1], name='nearest_bound_point_lat')
    df_lon = pd.Series(coastline_coords[ind].flatten()[0], name='nearest_bound_point_lon')
    return pd.concat([df_distance_to_shore, df_lat, df_lon], axis=1)


def convert_goem(geom, input_projection, output_projection = 'epsg:4326', names=None, shp =None, shx = None, dbf = None, flip_coords=False):
    '''Converts geometries from one projection to another with acceptable error. 
    In the process fixes also a few geometry errors.
    
    Parameters
    ----------
    geom: shapefile.Reader
        The shepefile you need to sanitize.
    
    input_projection: string
        an epsg identifier for the input datum, like 'epsg:4326'
    
    output_projection: string, default
        an epsg identifier for the output datum, like 'epsg:4326'.
        It defaults to 'epsg:4326' because it is WGS-84, aka the GPS
        cooridnates, so it's you are most likely to desire as output.
    
    names: list, default None
        labels you'd like the output gemetries to have in the output
        shapefile object. If None, the output shapefile will have items
        identified by incremental numbers.
    
    shp: File-like object, default None
        The file object you expect your shapefile's shp object
        to be written to. If None, a new BytesIO will be created.
    
    shx: File-like object, default None 
        The file object you expect your shapefile's shx object
        to be written to. If None, a new BytesIO will be created.
    
    dbf: File-like object, default None
        The file object you expect your shapefile's dbf object
        to be written to. If None, a new BytesIO will be created.
    
    flip_coords: bool default False
        if set to True, the function will return mirrored geometries.
        Why? Because -sometimes- shapefile geometries are flipped
        for unfathomable reasons and we may need to fix that.

    Returns
    -------
    shp , shx , dbf
        three file-like objects that collectively make for a new
        Shapefile. You may serialize them or open them with pyshp

    '''
    if shp is None:
        print('Creating shp BytesIO object')
        shp = BytesIO()
    if shx is None:
        print('Creating shp BytesIO object')
        shx = BytesIO()
    if dbf is None:
        print('Creating shp BytesIO object')
        dbf = BytesIO()
    wgs_shp = shapefile.Writer(shp=shp, shx=shx, dbf=dbf)
    wgs_shp.field('name', 'C')
    transformer = Transformer.from_crs(input_projection, output_projection)
    for idx, feature in enumerate(geom):
        # if there is only one part
        if len(feature.parts) == 1:
            print('Converting Polygon')
            # create empty list to store all the coordinates
            poly_list = []
            # get each coord that makes up the polygon
            for coords in feature.points:
                x, y = coords[0], coords[1]
                # tranform the coord
                new_x, new_y = transformer.transform(x, y)
                # put the coord into a list structure
                if flip_coords:
                    poly_coord = [float(new_y), float(new_x)]
                else:
                    poly_coord = [float(new_x), float(new_y)]
                # append the coords to the polygon list
                poly_list.append(poly_coord)
            # add the geometry to the shapefile.
            wgs_shp.poly([poly_list])
        else:
            print('Converting MultiPolygon of ' + str(len(feature.parts)) + ' parts')
            # append the total amount of points to the end of the parts list
            #feature.parts.append(len(feature.points))
            # enpty list to store all the parts that make up the complete feature
            poly_list = []
            # keep track of the part being added
            parts_counter = 0

            # while the parts_counter is less than the amount of parts
            while parts_counter < len(feature.parts) - 1:
                # keep track of the amount of points added to the feature
                coord_count = feature.parts[parts_counter]
                # number of points in each part
                no_of_points = abs(feature.parts[parts_counter] - feature.parts[parts_counter + 1])
                # create list to hold individual parts - these get added to poly_list[]
                part_list = []
                # cut off point for each part
                end_point = coord_count + no_of_points

                # loop through each part
                while coord_count < end_point:
                    for coords in feature.points[coord_count:end_point]:
                        x, y = coords[0], coords[1]
                        # tranform the coord
                        new_x, new_y = transformer.transform(x, y)
                        # put the coord into a list structure
                        if flip_coords:
                            poly_coord = [float(new_y), float(new_x)]
                        else:
                            poly_coord = [float(new_x), float(new_y)]
                        # append the coords to the part list
                        part_list.append(poly_coord)
                        coord_count = coord_count + 1
                # append the part to the poly_list
                poly_list.append(part_list)
                parts_counter = parts_counter + 1
            # add the geometry to to new file
            wgs_shp.poly(poly_list)
        if names is None:
            wgs_shp.record(str(idx))
        else:
            wgs_shp.record([names[idx]])
    wgs_shp.close()
    return shp , shx , dbf

def read_shape_from_zip(package:zipfile.ZipFile, name:str):
	'''SHP files are often packaged as ZIP files, so this function extracts
	Shapes from Zipfiles.
    
    Parameters
    ----------
    package: zipfile.ZipFile
        the zip file, already openend with the zipfile package
    
    name:   string
        the relative base path of your shapefile components, like 'bounds/nuts0'

    Returns
    -------
    shapefile.Reader
        a shapefile object that can be handled with the pyshp package
    '''
	myshp = package.open(name + '.shp')
	mydbf = package.open(name + '.dbf')
	return shapefile.Reader(shp=myshp, dbf=mydbf)

