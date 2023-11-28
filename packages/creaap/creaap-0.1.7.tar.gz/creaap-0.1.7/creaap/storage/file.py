'''Classes and functions to upload and download stuff from Azure File shares'''
import io
from azure.storage.fileshare import ShareServiceClient, ShareFileClient
from datetime import datetime
import pytz

from creaap.formats import denaive_datetime, to_tz_aware_datetime

class AzureShareClient:
    '''A simple client to perform upload and download operations from file share'''
    def __init__(self, connection_string,share_name):
        '''
        Creates a connection client to a specific Azure File Share

        Parameters
        ----------
        conenction_string: string
            the Azure Storage connection string. Grab it in the Azure Portal
        
        share_name: string
            the name of the File Share you want to connect to
        '''
        share_client = ShareServiceClient.from_connection_string(connection_string)
        self.client = share_client.get_share_client(share_name)

    def ls_files(self, path, namestart = None, recursive = False):
        '''
        List files under a path, optionally recursively.

        Paramters
        ---------
        path: string
            where to start file system exploration

        namestart: string, default None
            a prefix to filter files.

        recursive: bool, default False
            whether or not you want your ls to be recursive, i.e.
            traverse all subdirectories as well.

        Returns
        -------
        generator
            strings that represent File Share paths

        '''
        if not namestart == '':
            namestart == namestart
        share_path = self.client.get_directory_client(path)
        share_iter = share_path.list_directories_and_files(name_starts_with=namestart)
        for file in share_iter:
            yield file.name
            # in case we want a recursive ls
            if recursive and file.get('is_directory'):
                yield from self._ls_subdir(share_path.get_subdirectory_client(file['name']), namestart)
            

    def _ls_subdir(self, subdir_client, namestart = None):
        '''helper method to implement recursive LS'''
        share_iter = subdir_client.list_directories_and_files(name_starts_with=namestart)
        for file in share_iter:
            yield file.name
            # in case we want a recursive ls
            if file.get('is_directory'):
                yield from self._ls_subdir(subdir_client.get_subdirectory_client(file['name']), namestart)


    def get_updates(self, base_path = '', start_date = datetime.utcnow()):
        '''returns all the files that have been updated/added down the specified base_path after the start_time.
        Useful to poll file shares as currently Azure provides no "file share trigger"
        
        Parameters
        ----------
        base_path: string, default ''
            the directory where to look for updates. By default it's the root directory, so
            it will get any update in the whole file share.

        start_date: datetime.datetime, default right now in UTC time
            the first datetime that qualifies a file as "updated". It should be the
            datetime you last checked for updates.

        Returns
        -------
        generator
            a generator of azure.storage.fileshare.ShareFileClient objects
            to handle the updated files.
        
        '''
        # a little work on inputs...
        try:
            root_dir_client = self.client.get_directory_client(base_path)
        except:
            raise ValueError('Specified base path does not exist')
        # check if we have a legit datetime object
        if isinstance(start_date, datetime):
            # just to be sure it has a timezone attached
            start_date = denaive_datetime(start_date)
        else:
            start_date = to_tz_aware_datetime(start_date)
        # now on to fetching 
        yield from self._recursive_dir_updates(root_dir_client, start_date)
                
    def _recursive_dir_updates(self, dir_client, start_date):
        '''support method to recursively traverse the remote file system and get updated files'''
        for x in dir_client.list_directories_and_files():
            if x.get('is_directory'):
                yield from self._recursive_dir_updates(dir_client.get_subdirectory_client(x['name']), start_date)
            else:
                file_client = dir_client.get_file_client(file_name=x['name'])
                # get file's last upudate. Azure file sharesa work in UTC.
                load_time = denaive_datetime(file_client.get_file_properties()['creation_time'], timezone = pytz.utc)
                # tz-aware datetime can be compared even if in different timezones, so there is no need to
                # convert everything to UTC
                if (load_time > start_date):
                    yield file_client

    def download_to_stream(self, file):
        '''Downloads a File Share file into a BytesIO object
        
        Parameters
        ----------
        source: string or azure.storage.fileshare.ShareFileClient
            file path of the target resource, or ShareFileClient object connected to it

        Returns
        -------
        BytesIO
            byte-object representation of the blob resource
        '''
        
        if isinstance(file, ShareFileClient):
            file_client = file
        elif isinstance(file, str):
            file_client = self.client.get_file_client(file_path = file)
        else:
            raise ValueError('the *file* parameter has to be either a string representing a path to a file in the share or a ShareFileClient object')
        data = file_client.download_file()
        stream = io.BytesIO()
        data.download_to_stream(stream, max_concurrency=1)
        # go back to the beginning of the data stream
        stream.seek(0)
        return stream

    def upload_stream(self, data, dest):
        '''uploads a bytes object to the specified File Share path
        
        Parameters
        ----------
        data: bytes
            the object you want to upload

        dest: string
            te file share path where you want to slap the file
        '''
        file_client = self.client.get_file_client(file_path = dest)
        file_client.upload_file(data)

    def upload(self, source, dest):
        '''uploads a local file to the specified File Share path
        
        Parameters
        ----------
        source: string
            the local filepath

        dest: string
            te file share path where you want to slap the file
        '''
        with open(source, "rb") as source_file:
            self.upload_stream(source_file, dest)