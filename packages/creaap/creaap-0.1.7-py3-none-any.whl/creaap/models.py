from datetime import datetime
import pytz
import json
import inspect
from creaap.formats import datetime_to_tables_string, json_serial, unfuck_numpy_formats

class DomainEntity:
    '''Parent class for all domain entities, allows rapid serialization of objects
    
     Class Attributes
    ----------------
    table: string
        the name of the correnspondig table in the Azure Tables persistence scheme.
        If set to None, the entity is not persisted to Table Storage

    row_key: string
        the name of the entity's attribute that will be used as RowKey

    partition_key: string
        the name of the entity's attribute that will be used as PartitionKey
    '''
    table = 'Entity'
    partition_key = 'PartitionKey'
    row_key = 'RowKey'

    @classmethod
    def from_dict(cls, env):      
        return cls(**{
            k: v for k, v in env.items() 
            if k in inspect.signature(cls).parameters
        })

    def __eq__(self, other):
        '''Two domain entities are to be considered equal if they clash once put in the table storage'''
        if isinstance(other, DomainEntity):
            if other.table == self.table:
                    return (self.__dict__[self.row_key] == other.__dict__[other.row_key]) & (self.__dict__[self.partition_key] == other.__dict__[other.partition_key])
        return False
    
    def to_json(self):
        '''returns a JSON representaion of the current object'''
        return json.dumps(self, default=json_serial, 
            sort_keys=True, indent=4)

    def to_table_entities(self):
        '''Return a generator containing DB-manageable objects that represent the current domain entity'''
        out= {}
        for key, value in self.__dict__.items():
            if key == self.partition_key:
                out['PartitionKey'] = str(value)
            elif key == self.row_key:
                if isinstance(value, datetime):
                    out['RowKey'] = datetime_to_tables_string(value)
                else:
                    out['RowKey'] = str(value)
            elif isinstance(value, DomainEntity):
                yield from value.to_table_entities()
            elif isinstance(value, list) |  isinstance(value, tuple):
                for elem in value:
                    try:
                        yield from elem.to_table_entities()
                    except:
                        print(' Object ' + str(elem) + ' in field ' + str(key) + ' is not a valid domain entity')
            else:
                # here we are dealing with "anything else". Which can be some Numpy fuckery
                # that Table Storage won't be able to digest. Luckily we have a failsafe 
                # method to prevent that.
                out[key]= unfuck_numpy_formats(value)
        yield self.table, out
    
    def expand(self):
        '''fetches all possible connected information'''
        pass


class DataBatch(DomainEntity):
    '''
    Commodity entity to move around batches of Domain Entities.

    DomainEntities in the DataBatch can be of different types and the 
    Databatch can be flushed to the Table Storage like any other 
    DomainEntity object and all its components will be inserted/update/
    upserted.

    By default, the 'table' class attribute is set to None to prevent
    the DataBatch itself from being persisted, however, if you need to,
    you can subclass it into persistable entities.
    '''
    table = None
    def __init__(self):
        self.batch = []

    def append(self,data):
        '''Adds a data object to the container'''
        if isinstance(data, DomainEntity):
            self.batch.append(data)
        else:
            raise TypeError("Only valid DomainEntity types can be added to a DataBatch")
    
    def to_table_entities(self):
        '''Translates the container into table entites'''
        for x in self.batch:
            yield from x.to_table_entities()
	
    def __iter__(self):
        for i in self.batch:
            yield i

    def __len__(self):
        return len(self.batch)

class SpatialEntity(DomainEntity):
    '''
    Class of geo-referenced entities
    This class should be regareded as an abstract one and used as base for defining 
    your own entities that come with an associated geographical information
    
    Class Attributes
    ----------------
    table: string
        the name of the correnspondig table in the Azure Tables persistence scheme.
        If set to None, the entity is not persisted to Table Storage

    row_key: string
        the name of the entity's attribute that will be used as RowKey

    partition_key: string
        the name of the entity's attribute that will be used as PartitionKey

    geometry: string
        the name of the entity's attribute that will be used to build the spatial index
    '''
    table = None
    partition_key = 'PartitionKey'
    row_key = 'RowKey'
    geometry_attribute = 'geometry'

class BlobEntity(DomainEntity):
    '''
    Class for entities with attached blob objects.
    This class should be regareded as an abstract one and used as base for defining 
    your own entities that come with an associated Blob file
    
    Class Attributes
    ----------------
    table: string
        the name of the correnspondig table in the Azure Tables persistence scheme

    row_key: string
        the name of the entity's attribute that will be used as RowKey
        If set to None, the entity is not persisted to Table Storage

    partition_key: string
        the name of the entity's attribute that will be used as PartitionKey

    blob_path_attribute: string
        the name of the entity's attribute that will be used as PartitionKey

    '''
    table = None
    partition_key = 'PartitionKey'
    row_key = 'RowKey'
    blob_path_attribute = 'blob'

