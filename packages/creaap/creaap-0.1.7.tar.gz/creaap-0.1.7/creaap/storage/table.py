'''Classes and functions to store and query data from Azure Tables'''
# Reference: https://docs.microsoft.com/en-us/python/api/overview/azure/data-tables-readme?view=azure-python
import logging
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from creaap.models import DomainEntity

from creaap.utils import get_all_subclasses, id_generator, first


class TablePersister():
	'''
	Allows to handle data on Table Storage like it was on a
	object-based DB. Sort of. BAsically allows you to use 
	Table Storage as a DB replacement.
	'''


	def __init__(self, connection_string):
		'''Intantiates a Table Storage connection client
		
		Parameters
        ----------
        conenction_string: string
            the Azure Storage connection string. Grab it in the Azure Portal
		'''
		self.table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
		# this is a list of classes in the Models module
		clsmembers = get_all_subclasses(DomainEntity)
		# and now we turn it into a dictionary of DB table -> DomainEntity associations
		self.class_index={}
		for model_class in clsmembers:
			if issubclass(model_class, DomainEntity):
				if model_class.table:
					self.class_index[model_class.table] = model_class

	def _to_domain_entity(self, dictionary, table):
		'''Helper method to turn an Azure Tables row into a Domain Entity'''
		domain_class = self.class_index[table]
		try:
			dictionary[domain_class.partition_key] =  dictionary.pop("PartitionKey")
		except:
			dictionary[domain_class.partition_key] = None
		try:
			dictionary[domain_class.row_key] =  dictionary.pop('RowKey')
		except:
			dictionary[domain_class.row_key] = None
		return domain_class.from_dict(dictionary)

	def init_tables(self):
		'''
		Considers all defined DomainEntities in our project and creates
		a brand new table for each one of them.

		Returns
		-------
		None
		'''
		for table, _ in self.class_index.items():
			try:
				self.create_table(table)
			except ResourceExistsError:
				logging.warning("Nice try, but table " + table + ' already exists, asshole!')


	def create_table(self, table_name):
		'''creates a new table.
		
		Parameters
		----------
		table_name: string
			the name of the new table. Don't worry if it already esists

		Returns
		-------
		None
		'''
		return self.table_service_client.create_table(table_name=table_name)

	def insert_entity(self, domain_entity):
		'''inserts a new entity and all its components
		
		Parameters
		----------
		domain_entity: creaap.models.DomainEntity
			the object you need to be persisted

		Returns
		-------
		generator
			a generator of azure.data.tables.TableItem objects, returning a TableItem
			for each table row affected by the operation.
		'''
		for table, entity in domain_entity.to_table_entities():
			with self.table_service_client.get_table_client(table_name=table) as table_client:
				yield table_client.create_entity(entity=entity)

	def update_entity(self, domain_entity):
		'''updates a new entity and all its components
		
		Parameters
		----------
		domain_entity: creaap.models.DomainEntity
			the object you need to be persisted
		
		Returns
		-------
		generator
			a generator of azure.data.tables.TableItem objects, returning a TableItem
			for each table row affected by the operation.
		'''
		for table, entity in domain_entity.to_table_entities():
			with self.table_service_client.get_table_client(table_name=table) as table_client:
				yield table_client.update_entity(entity=entity)

	def upsert_entity(self, domain_entity):
		'''upserts a new entity and all its components
		
		Parameters
		----------
		domain_entity: creaap.models.DomainEntity
			the object you need to be persisted
		
		Returns
		-------
		generator
			a generator of azure.data.tables.TableItem objects, returning a TableItem
			for each table row affected by the operation.
		'''
		for table, entity in domain_entity.to_table_entities():
			with self.table_service_client.get_table_client(table_name=table) as table_client:
				yield table_client.upsert_entity(entity=entity)

	def query_entity(self, table, query, parameters = {}, **kwargs):
		'''Executes Azure Table queries
		
		Parameters
		----------
		table: string
			the table you intend to query.

		query: string
			the Azure Tables query string.

		paramentries: dict, default {}
			optional parameters dictionary for the above query
		
		Returns
		-------
		generator
			a generator of creaap.models.DomainEntity, returning a DomainEntity
			for each table row retireved by the operation.
		'''
		with self.table_service_client.get_table_client(table) as tc:
			for x in tc.query_entities(
						query_filter=query, parameters=parameters, **kwargs
					):
				yield self._to_domain_entity(x, table)
	
	def get_all_entities(self, table):
		'''Retrieves all records from a given table. 
		It's like a SELECT * FROM table

		Parameters
		----------
		table: string
			the table you intend to retrive in its interity.
		
		Returns
		-------
		generator
			a generator of creaap.models.DomainEntity, returning a DomainEntity
			for each table row retireved by the operation.
		'''
		with self.table_service_client.get_table_client(table_name=table) as table_client:
			for _, row in enumerate(table_client.list_entities()):
				yield self._to_domain_entity(row, table)

	def delete_entity(self, table, partition_key, row_key):
		'''Permanently deletes an entiy from a table
		
		Parameters
		----------
		partition_key: string
			the PartitionKey of the object you want to delete

		row_key: string
			the RowKey of the object you want to delete
		
		Returns
		-------
		generator
			a generator of azure.data.tables.TableItem objects, returning a TableItem
			for each table row affected by the operation.
		'''
		with self.table_service_client.get_table_client(table_name=table) as table_client:
			yield table_client.delete_entity(partition_key, row_key)

	def commit_large(self, domain_entity, operation = "insert", options ={}):
		'''This commits bulk operations on big entities with a truckload of smaller entities inside.
		
		Parameters
		----------
		domain_entity: creaap.models.DomainEntity
			the object you need to be persisted

		operation: string
			the operation you'd like to perform, one of the following: 'insert', 'upsert',
			'update', 'delete'
		
		options: dict, default {}
			the optional parameter dictionary to adderss thing such as the merge mode 
			for update/upsert operations.
		
		Returns
		-------
		generator
			a generator of azure.data.tables.TableItem objects, returning a TableItem
			for each table row affected by the operation.
		'''
		# BIG problem: batches MUST have the same Partition Key
		to_commit = {}
		for table, entity in domain_entity.to_table_entities():
			if to_commit.get(table):
				# update the existing dictionary
				to_commit[table]= self._separate_pks(entity['PartitionKey'], (operation, entity, options), to_commit[table])
			else:
				# create a whole new one
				to_commit[table]= self._separate_pks(entity['PartitionKey'], (operation, entity, options), {})
		for table, pks in to_commit.items():
			print('[INFO] Committing on Table ' + table)
			with self.table_service_client.get_table_client(table_name=table) as table_client:
				for _, operations in pks.items():
					# Apparently Azure tables can handle a maximum of 100 lines per batch update
					for op_chunk in self.__chunks(operations, 99):
						try:
							yield table_client.submit_transaction(op_chunk)
						# Apparently some large operation chunks may fail because of transactionerrors
						# the solution is to subdivide the batch and to retry
						except Exception as ex:
							logging.warning(ex)
							for operation in op_chunk:
								try:
									if first(operation, None) == 'upsert':
										# ooooh shit, it's him again
										yield self._unfuck_upsert_error(table_client, *operation)
									else:
										yield table_client.submit_transaction([operation])
								except Exception as ex:
									logging.error(ex)
	
	def _unfuck_upsert_error(self, table_client, operation, entity={}, options={}):
		'''helper method that, for lack of better words, unfucks
		 the fuckery an Upsert operation may cause in Azure Tables'''
		# UPSERT is never transactional, so here we have to try update 
		# and if it fails, we try insert
		try:
			return table_client.update_entity(entity=entity)
		except:
			return table_client.create_entity(entity=entity)

	def _separate_pks(self, pk, in_tuple, dictionary):
		'''helper method to pidgeonhole entities by Partition Key value'''
		if dictionary.get(pk):
			dictionary[pk].append(in_tuple)
		else:
			dictionary[pk] = [in_tuple]
		return dictionary

	def __chunks(self, lst, n):
		"""Yield successive n-sized chunks from lst."""
		for i in range(0, len(lst), n):
			yield lst[i:i + n]

	def is_unique(self, table, value, field='RowKey'):
		'''Tests if a certain value is unique within registered entities

		Parameters
		----------
		table: string
			the table you want to check upon
		
		value: object
			the value you want to checo its uniqueness
		
		field: string, default 'RowKey'
			the table field where the value belongs to, defaults
			to 'RowKey'
		
		Returns
		-------

		bool
			wheter or not the value is unique
		'''
		with self.table_service_client.get_table_client(table) as tc:
			if len(list(tc.query_entities(
						query_filter= str(field)+ ' eq @value', parameters={'value':value}
					))) >0:
				return False
			else:
				return True
	
	def generate_unique_value(self, table, field = 'RowKey', **kwargs):
		'''suggests a unique (not registered yet) value for a given field for a given entity
		
		Parameters
		----------
		table: string
			the table you want to generate a value for
		
		field: string, default 'RowKey'
			the table field where the value would belongs to, defaults
			to 'RowKey'
		
		Returns
		-------

		string
			a unique string value for the considered field
		'''
		temp_id = id_generator(**kwargs)
		while not self.is_unique(table, temp_id, field):
			temp_id = id_generator(**kwargs)
		return temp_id



