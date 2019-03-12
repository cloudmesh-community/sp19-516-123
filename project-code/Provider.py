import os, sys
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
        #container_name = config['cloudmesh.storage.azure-1.credentials.container']

    def get(self, container_name, filename, destdir):
        HEADING()
        download_path = os.path.join(path_expand(destdir), filename)
        print("\nDownloading blob to " + download_path)
        blob = self.block_blob_service.get_blob_to_path(container_name, filename, download_path)
        print(blob.__dict__)

    def put(self, container, filename, sourcedir):
        HEADING()
        upload_path = os.path.join(path_expand(sourcedir), filename)
        self.block_blob_service.create_blob_from_path(container, filename, upload_path)
        print("put", filename)

    def delete(self, container, filename):
        HEADING()
        if self.block_blob_service.exists(container, filename):
            self.block_blob_service.delete_blob(container, filename)
            print("delete", filename)
        else:
            print("Blob does not exist")

    def list(self, container):
        HEADING()
        if self.block_blob_service.exists(container):
            blob_generator = self.block_blob_service.list_blobs(container)
            for blob in blob_generator:
                print("\t Blob name: " + blob.name)
            print("list", container)
        else:
            print("Container does not Exist")

    def info(self, container, filename):
        HEADING()
        blob_prop = self.block_blob_service.get_blob_properties(container, filename)
        blob_size = self.block_blob_service.get_blob_properties(container, filename).properties.content_length
        print("Info", blob_prop.__dict__, "\nBlob Size:", blob_size, "Bytes")
        print(self.block_blob_service.get_blob_properties(container, filename))

    def createdir(self, container):
        HEADING()
        if self.block_blob_service.exists(container):
            print("Container already exists")
        else:
            container_new = self.block_blob_service.create_container(container)
            print("Createdir", container_new.__dict__)

    def listdir(self):
        HEADING()
        container_gen = self.block_blob_service.list_containers()
        for container in container_gen:
            print("\t Container name: " + container.name)
        print("Listdir")

    def deletedir(self, container):
        HEADING()
        if self.block_blob_service.exists(container):
            container_del = self.block_blob_service.delete_container(container)
            print("Deletedir", container_del.__dict__)
        else:
            print("Container does not exist")
