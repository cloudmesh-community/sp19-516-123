import os, sys, re
from azure.storage.blob import BlockBlobService, PublicAccess

from pprint import pprint
from cloudmesh.common.util import HEADING
from cloudmesh.compute.libcloud.Provider import Provider
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.Printer import Printer
from cloudmesh.common.FlatDict import FlatDict, flatten
from cloudmesh.management.configuration.SSHkey import SSHkey
from cloudmesh.common.util import path_expand


class Provider(object):

    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))
        config = Config()
        self.block_blob_service = BlockBlobService(account_name=config['cloudmesh.storage.azure-1.credentials.account_name'],
                                                   account_key=config['cloudmesh.storage.azure-1.credentials.account_key'])
        self.container = config['cloudmesh.storage.azure-1.credentials.container']

    def get(self, filename, destdir):
        HEADING()
        if re.search('/', filename) is None:
            sourcefile = filename
        else:
            sourcefile = filename.split("/")[-1]
        download_path = os.path.join(path_expand(destdir), sourcefile)
        print("\nDownloading blob to " + download_path)
        blob = self.block_blob_service.get_blob_to_path(self.container, filename, download_path)
        pprint(blob.__dict__)
        pprint(blob.properties.__dict__)
        blob.properties = blob.properties.__dict__
        blob_copy = blob.properties["copy"]
        blob_cs = blob.properties["content_settings"]
        blob_ct = blob.properties["creation_time"]
        blob_mt = blob.properties["last_modified"]
        blob_dt = blob.properties["deleted_time"]
        pprint(blob_copy.__dict__)
        print(blob_ct, '\n', blob_mt, '\n', blob_dt)
        pprint(blob.__dict__)
        #blob.cm = {
        #    "kind": "azure-1"
        #}
        return blob

    def put(self, filename, sourcedir):
        HEADING()
        if re.search('/', filename) is None:
            destfile = filename
        else:
            destfile = filename.split("/")[-1]
        upload_path = os.path.join(path_expand(sourcedir), destfile)
        obj = self.block_blob_service.create_blob_from_path(self.container, filename, upload_path)
        print("put", filename)
        return obj.__dict__

    def delete(self, filename):
        HEADING()
        if self.block_blob_service.exists(self.container, filename):
            self.block_blob_service.delete_blob(self.container, filename)
            print("delete", filename)
        else:
            print("Blob does not exist")

    def listfiles(self, dirname):
        HEADING()
        if self.block_blob_service.exists(self.container):
            blob_generator = self.block_blob_service.list_blobs(self.container)
            for blob in blob_generator:
                if re.search('/', blob.name):
                    if dirname in blob.name.split("/")[-2]:
                        print("\t Blob name: " + blob.name.split("/")[-1])
                else:
                    print("\t Blob name: " + blob.name)
            print("list", self.container)
        else:
            print("Container does not Exist")

    def info(self, filename):
        HEADING()
        blob_prop = self.block_blob_service.get_blob_properties(self.container, filename)
        blob_size = self.block_blob_service.get_blob_properties(self.container, filename).properties.content_length
        print("Info", blob_prop.__dict__, "\nBlob Size:", blob_size, "Bytes")
        print(self.block_blob_service.get_blob_properties(self.container, filename))

    def createdir(self, dirname):
        HEADING()
        if self.block_blob_service.exists(self.container):
            data = b' '
            blob_name = dirname + '/' + 'dummy'
            self.block_blob_service.create_blob_from_bytes(self.container, blob_name, data)
            blob_by = self.block_blob_service.get_blob_to_bytes(self.container, blob_name)
            pprint(blob_by.__dict__)

    def listdir(self):
        HEADING()
        if self.block_blob_service.exists(self.container):
            blob_generator = self.block_blob_service.list_blobs(self.container)
            folder_list = []
            for blob in blob_generator:
                if re.search('/', blob.name):
                    folder_list.append(blob.name.split("/")[0])
            print("Folder List:", set(folder_list))
        else:
            print("Container does not Exist")

    def deletedir(self, dirname):
        HEADING()
        if self.block_blob_service.exists(self.container):
            print("1st IF")
            generator = self.block_blob_service.list_blobs(self.container)
            for blob in generator:
                if re.search('/', blob.name):
                    print("in re")
                    if dirname in blob.name.split("/")[-2]:
                        self.block_blob_service.delete_blob(self.container, blob.name)
                        print("delete", blob.name)
        else:
            print("Container does not exist")

    def search(self, directory, filename, recursive):
        srch_gen = self.block_blob_service.list_blobs(self.container)
        print("searching...")
        if recursive == 'N':
            srch_file = os.path.join(directory[1:], filename)
            print(srch_file)
            for blob in srch_gen:
                if blob.name == srch_file:
                    print('File found:' + blob.name)
        else:
            file_found = 'N'
            for blob in srch_gen:
                if re.search('/', blob.name) is not None:
                    if os.path.basename(blob.name) == filename:
                        if os.path.commonpath([blob.name, directory[1:]]) == directory[1:]:
                            file_name = blob.name
                            file_found = 'Y'
            if file_found == 'Y':
                print('File Found:' + file_name)
            else:
                print('File not found ')





