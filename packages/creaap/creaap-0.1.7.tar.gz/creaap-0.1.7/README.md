# CREA Applications in Python kit
This package is a toolkit meant to speed up Python application development in Azure.
At its core, it is a collection of frequently re-used classes and functions that emerged from in-house projects developed at [CREA](https://www.crea.gov.it/), but we guessed that it may be helpful for anyone who has to deal with Azure and Python.

# Is CREAAP good for my project?

If you work at CREA and you are tasked with developing a Python application of sort that goes beyond a simple *hello world* or a one-shot wonder that is supposed to work only on yor laptop, then it *pretty darn obvious* that you *should really* use CREAAP.
If you don't work at CREA, you may still find it useful to deal with the following problems:

1.	Use Azure Table Storage as database
2.	Manage app users with Azure Active Directory
3.	Read and write files from Blob storages and File shares
4.	Manage geo-localized data

# Set up an application with CREAAP

## Azure Storage
The Azure Storage comes with four types of persistence for your data:
+ **[blobs](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction)** to store any object, including very large ones, in a file system-ish way.
+ **[file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-introduction)** to store files on an actual file system, that can be mounted on a machine or used as storage for ftp services.
+ **[tables](https://learn.microsoft.com/en-us/azure/storage/tables/table-storage-overview)** to store tabular data in no-sql fashion.
+ **[queues](https://learn.microsoft.com/en-us/azure/storage/queues/storage-queues-introduction)** to store messages (i.e. JSON objects that weight less than 64 KB), queues are Azure Functions' turf.

Each type of storage comes with a dedicated Python library provided by Microsoft itself, however we felt that we could provide a higher degree of abstraction than that and thus CREAAP comes with a `storage` module that simplifies the access to such services.
As a general rule, all the objects herein provided expect an Azure Storage connection string as a parameter in their constructor method, and provide data access and manipulation methods that return [Generators](https://wiki.python.org/moin/Generators) to keep memory footprint low, especially when queries are large, and to allow control on execution. 

### Blob Client
CREAAP provides you with an AzureBlobClient object that abstracts over the interation with an Azure Blob container. To create one, you need to pass a valid storage connection string and the name of an existing blob container.
```
from creaap.storage.blob import AzureBlobClient

client = AzureBlobClient(storage_key,"your-blob-container-name")
```
The AzureBlobClient provides methods to explore the container's contents that retrun *Generator* objects to allow you to process retrieved elements one by one in a lazy way.
```
for file_name in client.ls_files('myfolder/', recursive=Tue)
	print(file_name)
```
Along with methods to upload and download files, either from or to physical fils on your file system, or from/to byte objects
```
# download to file system (works also for directories)
client.download('myfolder/myfile', 'my_local_path/my_file')
# download byte object
data_stream = client.download_to_bytes('myfolder/myfile')

# upload from file system
client.upload('my_local_path/my_file', 'my_blob_path/my_file')
# upload from byte object
client.upload_stream(data_stream, 'my_blob_path/my_file')
```

### File Client
Similarly to the AzureBlobClient, the AzureShareClient object provides abstraction over the File Share storage. Each client is connected to a single share and allows to list, upload, and download files.
```
from creaap.storage.file import AzureShareClient

storage_key =  os.environ['AzureWebJobsStorage'] # fetch your storage account's connection string
client = AzureShareClient(storage_key,"your-file-share-name") 
for remote_file in client.ls_files("your-folder-name",<optional prefix>)):
	print(remote_file)
```
Additionally, the AzureShareClient provides you with a method to check for updates on files, which allows you to implement a File Share trigger.
```
for new_file in client.get_updates('your/base/path', datetime(time you last checked)):
	print(new_file)
```
This method returns a generator of azure.storage.fileshare.ShareFileClient objects, which can be seamlessly passed to the download method.
```
for new_file in client.get_updates('your/base/path', datetime(time you last checked)):
	file_data = client.download_to_stream(new_file)
	# do stuff
```
### Table Persister
Objects and methods defined in `creaap.storage.table` provide you with a simplified interface to flush objects into the table storage and to retrieve them.
You have to define entities you want to persist to the Table Storage as CREAAP *Domain Entities*, by extending the `DomainEntity` class provided in `creaap.models`, like in the following example.
```
from creaap.models import DomainEntity

class MyEntity(DomainEntity):
	table = 'mytable'
	partition_key = 'foo'
    row_key = 'bar'

	def __init__(self, foo, bar, baz = None):
		self.foo = foo
		self.bar = bar
		self.baz = baz
```
Domain Entities must have three class-attributes:
+ `table`: identifing the table to which instances of the class will be persisted
+ `partition_key`: the variable to be used as Partition Key
+ `row_key`: the variable to be used as Row Key

The signature of the DomainEntity's `__init__` method identifies all the columns that can be persisted for that entity, and parameters without default values stand for mandatory fields, while parameters with `None` as default value identify nullable fields.
CREAAP's DomainEntity objects may contain other DomainEntity objects to represent relationships among said entities, like in the minimal example below:

```
class MyComposite(DomainEntity):
	table = 'mycomposite'
	partition_key = 'foo'
    row_key = 'bar'

	def __init__(self, foo, bar, components = []):
		self.foo = foo
		self.bar = bar
		self.components = components

mc = MyComposite('foo', 'bar', [MyEntity('foo', 'bar', 'baz')])
```
Composite entities can include as many child entities as you like, and when persisted
Speaking of persistence, the `TablePersister` class allows you to persist an entity and all its DomainEntity components in a single shot with its `insert_entity` method, as shown below.
```
from creaap.storage.table import TablePersister

dba = TablePersister(os.environ['AzureWebJobsStorage'])
dba.init_tables()
for out in dba.insert_entity(MyEntity('foo', 'bar', 'baz')):
	pass # logging/control logic here
```
Similarly you can update and upsert entities with the `update_entity` and `upsert_entity` methods, that share the same interface. It is important to note how all these methods return *generator* objects to allow you to keep track of each object that ends up in your table storage and to check for eventual errors.

To retrieve your DomainEntities, the `TablePersister` provides two methods: a brutish one to fetch all entries in a given table:
```
dba = TablePersister(os.environ['AzureWebJobsStorage'])
for entity in dba.get_all_entities(MyEntity.table):
	print(entity)
```
And another one to perform queries that takes the following arguments:
+ `table`: a reference to the Azure Tables table name.
+ `query`: an Azure Tables [filter expression](https://learn.microsoft.com/en-us/visualstudio/azure/vs-azure-tools-table-designer-construct-filter-strings?view=vs-2022) to be used as query. While writing filters, mind that these expression have to be resolved by the Table Storage, hence you should refer to the partition and row key attributes as ParitionKey and RowKey.
+ `parameters`: a dictionary of query paramters and their values.

Here follows a minimal usage example:
```
for r in dba.query_entity(MyEntity.table, 'PartitionKey eq @pk and RowKey eq @rk', {'pk':'foo', 'rk':'bar'}):
	print(r.to_json())
```
As for insert, update, and upsert, query methods return always generator objects.


## Azure Active Directory
To use Azure Active Directory as identity provider for your application, you'll first need to create a dedicated *Enterprise Application* from the Azure Portal. Mind to specify valid callback URLs during the Enterprise Application configuration (*localhost* ones are acceptable) and remember that you can always edit them from the Portal using the *Authentication* blade in the Enterprise Application's own page.

If you are working on an Azure Functions application, the Enterprise Application will be automatically created and properly configured once you set in the *Authentication* blade Azure Active Directry as Identity Provider. 

Once the Enterprise Application is created, go to its page in the Portal, edit it by adding the user roles your project will use, then add the following permissions:
```
Application.Read.All
Directory.Read.All
User.Read
User.Read.All
User.ReadBasic.All
offline_access
openid
profile
```

Save the whole thing (some app premissions may require approval from your AD Admin to work though), and you should be done with AAD configuration.
Now it's time to get a few *sensitive* information, to allow CREAAP's AAD module to work properly you will need:
+ **Application ID** (appId): you will find this in the Enterprise Application's *Overview* blade as well as in its *Manifest file*, where you should look for the `appId` key and get its value.
+ **Client Secret**: you have to generate this through the Azure Portal. Mind that it may last two years at best, so you *will* have to refresh it sooner or later.
+ **Tenant ID**: this is the Azure Tenant identifier, and a wrong value can cause [cryptic errors](https://stackoverflow.com/questions/37151346/authorization-identitynotfound-error-while-accessing-graph-api), it can be found in the the *Overview* blade in the AAD application's page in the Portal.
+ **Object ID**: you will find this in the Enterprise Application's *Overview* blade.


### Passing AAD parameters
The best way to include AAD parameters into you application would be to store them as *Environment Variables*, in fact CREAAP will try to read:
+ The *Application ID* from `MICROSOFT_PROVIDER_AUTHENTICATION_CLIENT_ID`;
+ the *Client Secret* from `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET`;
+ the *Tenant ID* from `MICROSOFT_PROVIDER_AUTHENTICATION_TENANT_ID`;
+ the *Object ID* from `MICROSOFT_PROVIDER_AUTHENTICATION_APPLICATION_OBJECT_ID`

If these variables are properly set, CREAAP's `aad` module will get them on its own whenever they are needed.
Otherwise, you can pass them explicitly as arguments to any function in the `creaap.users.aad` module, like in the following example:

```
read_user_authorization(your-request,
			clientID = 'your-application-id',
			clientSecret = 'your-client-secret',
			tenantID = 'your-tenant-id')
```