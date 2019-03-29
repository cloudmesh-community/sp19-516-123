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
import cloudmesh.storage.provider.azureblob.Provider

# nosetest -v --nopature
# nosetests -v --nocapture tests/test_storage_azure.py
# nosetests -v --nocapture tests.test_storage_azure:TestName.test_01_get_blob (for specific function)

class TestName:

    def setup(self):
        config = Config()
        self.block_blob_service = BlockBlobService(account_name=config['cloudmesh.storage.azure-1.credentials.account_name'],
                                                    account_key=config['cloudmesh.storage.azure-1.credentials.account_key'])
        self.container = config['cloudmesh.storage.azure-1.credentials.container']
        self.provider = cloudmesh.storage.provider.azureblob.Provider.Provider()
        self.service = "azureblob"
        self.source = "~/sample/mp1.jpg"    #Local filename
        self.src_path = "~/sample"          #local Directory
        self.destination = "/test/mp1.jpg"  #Cloud Service folder/file
        self.destfile = "mp1.jpg"           #Cloud Service file
        self.directory = "/test"            #Cloud Service Directory

    def test_01_get_blob(self):
        HEADING()
        d = self.provider.get(self.src_path, self.destination, recursive=False)
        pprint(d)

    def test_02_get_recur(self):
        HEADING()
        d = self.provider.get(self.src_path, self.directory, recursive=True)
        pprint(d)

    def test_03_put_blob(self):
        HEADING()
        d = self.provider.put(self.source, self.directory, recursive=False)
        pprint(d)

    def test_04_put_recur(self):
        HEADING()
        d = self.provider.put(self.src_path, self.directory, recursive=True)
        pprint(d)

    def test_05_list_blob(self):
        HEADING()
        d = self.provider.list(self.directory, recursive=False)
        pprint(d)

    def test_06_list_recur(self):
        HEADING()
        d = self.provider.list(self.directory, recursive=True)
        pprint(d)

    def test_07_search_blob(self):
        HEADING()
        d = self.provider.search(self.directory, self.destfile, recursive=False)
        pprint(d)

    def test_08_search_recur(self):
        HEADING()
        d = self.provider.search(self.directory, self.destfile, recursive=True)
        pprint(d)

    def test_09_create_dir(self):
        HEADING()
        d = self.provider.create_dir(self.directory)
        pprint(d)

    def test_10_delete_blob(self):
        HEADING()
        d = self.provider.delete(self.directory)
        pprint(d)
