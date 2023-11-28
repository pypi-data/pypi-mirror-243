'''Contains classes and functions to handle spatial queries'''
from io import BytesIO
import pickle
from typing import Collection
import shapely
import shapefile
import os
from shapely.geometry import shape
from shapely.strtree import STRtree
from shapely.geometry import Polygon
from shapely import wkt
import pygeoif
import pickle
from pkg_resources import resource_filename

from creaap.spatial.utils import convert_goem
from collections.abc import Iterable

class SpatialMatcher:
    '''Allows you to perform spatial queries over a set of geometries
    This objects "reasons" with WKT geometries, if you don't know what
    WKT is, check this out:
    https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry 
    
    Attributes
    ----------
    index: shapely.geometry.STRtree
        the internal spatial index. Don't fuck with it.

    g: list of shapely.geometry.base.BaseGeometry
        the plottable representation of stored geometries

    labels: list of string
        the labels associated to each geometry object

    '''
    
    def __init__(self):
        '''creates a new, empty, object. No spatial index is built, build it with
        the build_spatial_index method or load it from file/stram with load/loads method'''
        self.index = None
        self.g = []
        self.labels =[]
          
    def build_spatial_index(self, shapefile = None, geometries = None, labels=None):
        '''Builds the spatial index. Takes as input either a shapefile or a list of geometries
        and indexes them allowing to perform queries on such elements.
        Each geometry object should have an associated label that identifies it that can be
        provided either embedded in the shapefile or in a separated list.

        Parameters
        ----------
        shapefile: shapefile.Reader, default None
            a shepefile object containiang the geometries you'd like to index

        geometries: list of shapely.geometry.base.BaseGeometry or WKT strings, defualt None
            a list of Shapely geometries or WKT strings in the likes of 'POINT(11.01 42.67)'

        labels: string or list of string
            either the shapefile attribute you want to use as label, or an actual list of string labels;
            if you provide labels as a list, its lenght must match the number of indexed geometry objects

        Returns
        -------
        None
        
        '''
        self.g=[]
        if shapefile:
            for s in shapefile.shapes():
                self.g.append(shape(s))
        else:
            if geometries is not None:
                for gm in geometries:
                    if isinstance(gm, str):
                        try: 
                            self.g.append(wkt.loads(gm))
                        except:
                            raise ValueError("geometries must be valid WKT strings, found " + str(gm))
                    elif isinstance(gm, shapely.geometry.base.BaseGeometry):
                        # just shove the bastard in
                        self.g.append(gm)
                    else:
                        raise TypeError("geometries must be either WKT strings or Shapely geometries, found " + str(type(gm)))
        # build the index
        self.index = STRtree(self.g)
        if isinstance(labels, str):
            for record in shapefile.records():
                self.labels.append(record.as_dict()[labels])
        elif isinstance (labels, list):
            self.labels = labels
        elif isinstance(labels, Iterable) or isinstance(labels, Collection):
            self.labels = list(labels)
        else:
            raise TypeError("labels can be either a field in the Shapefile or a list of values")
              

    def get_intersection(self, geometry_wkt):
        '''
        Returns the labels of the indexed geometries which intesrect the query geometry

        Parameters
        ----------
        geometry_wkt: string
            a WKT representation of the query geometry

        Returns
        -------
        list
            labels of intersecting geometries
        '''
        query_geom =wkt.loads(geometry_wkt)
        result = self.index.query(query_geom)
        out_idxs=[]
        for r in result:
            res_geom = self.g[r]
            if res_geom.intersects(query_geom):
                out_idxs.append(r)
        return [self.labels[i] for i in out_idxs]
    
    def get_intersection_percentages(self, geometry_wkt, areas=None):
        '''
        Returns the labels of the indexed geometries which intesrect the query geometry
        and their intersection percentages.

        Parameters
        ----------
        geometry_wkt: string
            a WKT representation of the query geometry.

        areas: list of strings, default None
            a filtering paramter, allows to restrict the query to a subset of the index 
            by specifiying the set of labels of interest; if left to None, the query 
            will run on all indexed geometries.
       
        Returns
        -------
        dict
            a label -> percentage dictionary; the percentage value represents
            how much of the geometry identified by the label intersercts with 
            the query geometry.
        '''

        if areas is None:
            areas = self.labels
        target_shape = wkt.loads(geometry_wkt)
        target_area = target_shape.area
        out = {}
        for l in areas:
            intersection=target_shape.intersection(self.g[self.labels.index(l)])
            out[l] = intersection.area / target_shape.area 
        return out
    
    def get_nearest_geom(self, geometry_wkt):
        '''
        Returns the label of the nearest indexed geometry

        Parameters
        ----------
        geometry_wkt: string
            a WKT representation of the query geometry

        Returns
        -------
        string
            label of the nearest geometry
        '''
        query_geom =wkt.loads(geometry_wkt)
        result = self.index.nearest(query_geom)
        return self.labels[result]
    
    def save(self, path):
        '''serializes the SpatialMatcher instance to a file
        
        Parameters
        ----------
        path: string
            the fielsystem location of the destination file

        Returns
        -------
        None
        '''
        file = open(path, 'wb')
        pickle.dump((self.index, self.g, self.labels), file)
        file.close()
    
    def load(self, path):
        '''loads the SpatialMatcher's index and labels from a file
        
        Parameters
        ----------
        path: string
            the fielsystem location of the target file

        Returns
        -------
        None
        '''
        file = open(path, 'rb')
        self.index, self.g, self.labels = pickle.load(file)
        file.close()
    
    def dumps(self):
        '''
        serializes the SpatialMatcher instance to a bytes object
        
        Parameters
        ----------
        None

        Returns
        -------
        bytes
            all the relevant data in the current SpatialMatcher instance
            pacakged in a nice byte string
        '''
        return pickle.dumps((self.index, self.g, self.labels))
    
    def loads(self, stream):
        '''loads the SpatialMatcher's index and labels from a bytes object
        
        Parameters
        ----------
        stream: bytes
            the byte object that contains the SpatialMatcher's index and labels

        Returns
        -------
        None
        '''
        self.index, self.g, self.labels = pickle.loads(stream)


class NoNutsError(Exception):
    """Exception raised when you are totally out of NUTs boundaries.

    Attributes
    ----------
    message: string
        Explanation of the error
    """

    def __init__(self, message="I came to get NUTs and raise exceptions, and I am totally out of NUTs"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.salary} -> {self.message}'

def get_nuts_matcher(level = 0):
    '''Loads a pre-computed NUTS matcher. Quick and dirty, expect little detail.

    Parameters
    ----------
    level: int in range 0-3
        The NUTS level you want to load, where 0 is nations,
        1 is macro-regions (e.g. Central Italy), 2 is 
        administrative regions (e.g. Lazio), and 3 is districts
        (e.g. Rome) 

    '''
    try:
        matcher = SpatialMatcher()
        matcher.load(resource_filename(__name__, 'data' + os.sep + 'nuts' + str(level)))
        return matcher
    except:
        raise NoNutsError('No level '+ str(level) + ' NUTS boundaries. Please use 0, 1, 2, or 3.')


def _get_nuts_level(nuts_shapefile, nuts_level = 0, attribute = 'NAME_LATN'):
    '''Helper function that extracts a NUTs level geography from a shapefile'''
    shapes =[]
    names = []
    all_records = nuts_shapefile.records() # this rat bastard is a labelled list of some sort that looks like a dictionary but ain't a dictionary
    all_shapes = nuts_shapefile.shapes() # and this is a Shapes object which is really a list
    for idx in range(len(all_shapes)):
        record = all_records[idx]
        if record.as_dict()['LEVL_CODE'] == nuts_level:
            names.append(record.as_dict()[attribute].rstrip('\x00'))
            shapes.append(all_shapes[idx])
    return shapefile.Shapes(shapes), names


def build_nuts_matcher(nuts_shapefile, nuts_level = 0, input_projection = "epsg:4326",output_projection = "epsg:4326", attribute = 'NAME_LATN'):
    '''
    Converts the official EU NUTs shapefie into a practical matcher.

    Get you NUTS shapefile here
    https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts
    ad find a way to unzip it and load it (spoiler: look for read_shape_from_zip in creaap.spatial.utils)

    Parameters
    ----------
    nuts_shapefile: a shapefile object
    '''
    shapes, names = _get_nuts_level(nuts_shapefile, nuts_level, attribute) # get correct level shapefile
    shp , _ , dbf = convert_goem(shapes,input_projection, output_projection, names, flip_coords=False)
    wgs84_shapes = shapefile.Reader(shp=shp, dbf=dbf)
    matcher = SpatialMatcher()
    matcher.build_spatial_index(wgs84_shapes, labels = names)
    return matcher
