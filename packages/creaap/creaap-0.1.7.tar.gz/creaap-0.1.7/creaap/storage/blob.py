'''Classes and functions to upload and download stuff from Azure Blob containers'''
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError
import sys, inspect
import os
import logging


class AzureBlobClient:
    '''A simple client to perform upload and download operations from blob storage'''
    def __init__(self, connection_string, container_name):
        '''Creates a new connection client for a Blob Container.

        Parameters
        ----------
        conenction_string: string
            the Azure Storage connection string. Grab it in the Azure Portal
        
        container_name: string
            the name of the container you want to connect to
        '''
        service_client = BlobServiceClient.from_connection_string(connection_string)
        self.client = service_client.get_container_client(container_name)

    def upload(self, source, dest):
        '''Upload a file or directory to a path inside the container
        Use this method if you don't know what the source path points at.

        Parameters
        ----------
        source: string
            file system path of the target resource, can be a file or a directory
        
        dest: string
            blob path for the uploaded resouces

        Returns
        -------
        None
        '''
        if (os.path.isdir(source)):
            self.upload_dir(source, dest)
        else:
            self.upload_file(source, dest)

    def upload_file(self, source, dest):
        '''
        Upload a single file to a path inside the container

        Parameters
        ----------
        source: string
            file system path of the target resource
        
        dest: string
            blob path for the uploaded file

        Returns
        -------
        None
        '''
        logging.info(f'Uploading {source} to {dest}')
        with open(source, 'rb') as data:
            self.upload_stream(data=data, dest=dest)

    def upload_stream(self, data, dest):
        '''
        Upload a Bytes stream to a path inside the container

        Parameters
        ----------
        data: bytes
            the resource you want to upload, represented as a bytes object
        
        dest: string
            blob path for the uploaded file

        Returns
        -------
        None
        '''
        self.client.upload_blob(name=dest, data=data, overwrite=True)

    def upload_dir(self, source, dest):
        '''
        Upload a directory to a path inside the container

        Parameters
        ----------
        source: string
            file system path of the target resource
        
        dest: string
            blob path for the uploaded resouces

        Returns
        -------
        None
        '''
        prefix = '' if dest == '' else dest + '/'
        prefix += os.path.basename(source) + '/'
        for root, _, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = '' if dir_part == '.' else dir_part + '/'
                file_path = os.path.join(root, name)
                blob_path = prefix + dir_part + name
                self.upload_file(file_path, blob_path)

    def download(self, source, dest):
        '''
        Download a file or directory to a path on the local filesystem.
        Use this method if you are not sure if the blob path points at
        a file or a directory.

        Parameters
        ----------
        source: string
            blob path of the target resource
        
        dest: string
            file system path of the output directory/file

        Returns
        -------
        None
        '''
        if not dest:
            raise Exception('A destination must be provided')

        blobs = self.ls_files(source, recursive=True)
        if blobs:
        # if source is a directory, dest must also be a directory
            if not source == '' and not source.endswith('/'):
                source += '/'
            if not dest.endswith(os.sep):
                dest += os.sep
        # append the directory name from source to the destination
        dest += os.path.basename(os.path.normpath(source)) + os.sep

        blobs = [source + blob for blob in blobs]
        for blob in blobs:
            blob_dest = dest + os.path.relpath(blob, source)
            self.download_file(blob, blob_dest)
        else:
            # in this branch we are delaing witha  single file
            self.download_file(source, dest)
        
    def download_file(self, source, dest):
        '''
        Download a single file to a path on the local filesystem.

        Parameters
        ----------
        source: string
            blob path of the target resource
        
        dest: string
            file system path of the output file

        Returns
        -------
        None
        '''
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        if dest.endswith('.'):
            dest += '/'
            blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest
        logging.info(f'Downloading {source} to {blob_dest}')
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.client.get_blob_client(blob=source)
        with open(blob_dest, 'wb') as file:
            data = bc.download_blob()
            file.write(data.readall())
    
    def download_to_bytes(self, source):
        '''download a single blob to a byte array.
        
        Parameters
        ----------
        source: string
            blob path of the target resource

        Returns
        -------
        bytes
            byte-object representation of the blob resource
        '''
        logging.info(f'Downloading {source} to byte array')
        bc = self.client.get_blob_client(blob=source)
        data = bc.download_blob()
        return data.readall()

    def ls_files(self, path, recursive=False):
        '''
        List files under a path, optionally recursively

        Parameters
        ----------
        path: string
            the base path in the container to ls

        recursive: bool, default False
            whether or not to go recursive on "directories" and get
            the whole file tree

        Returns
        generator
            strings that represent items in the container
        '''
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        for blob in blob_iter:
            relative_path = blob.name.lstrip(path)
            if recursive or not '/' in relative_path:
                yield blob.name

    def ls_dirs(self, path, recursive=False):
        '''
        List directories under a path, optionally recursively.
        Mind that in Azure Blob Storage directories are not "real" directories
        like in a file system, but rather prefeixes you use to better organize
        your blobs.

        Parameters
        ----------
        path: string
            the base path in the container to ls

        recursive: bool, default False
            whether or not to go recursive on "directories" and fetch
            all sub-subdirectories as well

        Returns
        generator
            strings that represent "directories" in the container
        -------
        '''
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        dirs = set()
        for blob in blob_iter:
            # here we just have to strip the filename
            relative_dir = '/'.join(blob.name.split('/')[:-1])
            if relative_dir and (recursive or not '/' in relative_dir) and not relative_dir in dirs:
                yield relative_dir
                dirs.add(relative_dir)
    
    def delete_file(self,path):
        '''
        Delete a single file inside the container

        Parameters
        ----------
        path: string
            blob path for the file to delete
        
        Returns
        -------
        None
        '''
        bc = self.client.get_blob_client(blob=path)
        bc.delete_blob()