###############################################################
# pip install .; pytest -v --capture=no -v --nocapture tests/test_cloud_openapi_azure_storage.py:Test_cloud_openapi_azure_storage.test_001
# pytest -v --capture=no tests/test_cloud_openapi_azure_storage.py
# pytest -v  tests/test_cloud_openapi_azure_storage.py
###############################################################

from __future__ import print_function

import os
import time

import pytest
from cloudmesh.common.run.file import run
from cloudmesh.common.util import banner


# noinspection PyPep8
@pytest.mark.incremental
class Test_cloud_installer:
    """
    
    see: https://github.com/cloudmesh/cloudmesh-common/blob/master/cloudmesh/common/run/background.py
    the code in thel link has not bean tested

    make this s function execute the server in the back ground not in a termina, 
    get the pid and kill it after the test is done

    UNAME := $(shell uname)
    ifeq ($(UNAME), Darwin)
    define terminal
      osascript -e 'tell application "Terminal" to do script "cd $(PWD); $1"'
    endef
    endif
    ifeq ($(UNAME), Linux)
    define terminal
      gnome-terminal --command 'bash -c "cd $(PWD); $1"'
    endef
    endif
    """
    
    def test_setup():
        self.variables = Variables()
        self.storage = Parameter.expand(variables['storage'])
        self.storage = storage[0]
        self.p = Provider(service=storage)
          
        self.openapi = run(command).execute()
        time.sleep(5)
        #self.service = "azureblob"
        #service.kill()
    
        
    
    
    def test_create_dir(self):
        path = "tmp"
        try:
            os.mkdir(path)
        except OSError:
            print(f"Creation of the directory {path} failed")
        else:
            print(f"Successfully created the directory {path}")

        assert True

    def test_install(self):
        # $(call terminal, python server.py)
        time.sleep(3)

    def test_openapi_azure_storage_put(self):
        banner('Upload blobs')
        result = run(
            'curl -H "Content-Type:application/json" -X POST -d \'{"service": "azureblob", "source": "~/sample/mp1.jpg", "destination": "/test", "recursive": "False"}\' http://localhost:8080/cloudmesh/put_blob')
        print(result)
        print()

    def test_openapi_azure_storage_list(self):
        banner('list the blobs')
        storage = self.storage
        #result = run(
        #    "curl http://localhost:8080/cloudmesh/list_blob?service=azureblob'&'directory=%2ftest'&'recursive=True")
        result = run(
            f"curl http://localhost:8080/cloudmesh/list_blob?service={storage}'&'directory=%2ftest'&'recursive=True")
        print(result)
        print()

    def test_openapi_azure_storage_search(self):
        banner('search the blobs')
        result = run(
            "curl http://localhost:8080/cloudmesh/search_blob?service=azureblob'&'directory=%2ftest'&'filename=mp1%2ejpg'&'recursive=True")
        print(result)
        print()

    def test_openapi_azure_storage_get(self):
        banner('Get the blobs')
        result = run(
            "curl http://localhost:8080/cloudmesh/get_blob?service=azureblob'&'source=%7e%2fsample'&'destination=%2ftest%2fmp1%2ejpg'&'recursive=True")
        print(result)
        print()

    def test_openapi_azure_storage_delete(self):
        banner('delete the blobs')
        result = run(
            "curl http://localhost:8080/cloudmesh/delete_blob?service=azureblob'&'source=%2ftest%2fmp1%2ejpg'&'recursive=False")
        print(result)
        print()

    def test_openapi_azure_storage_createdir(self):
        banner('Create a Directory')
        result = run(
            "curl http://localhost:8080/cloudmesh/create_dir?service=azureblob'&'directory=%2fapi")
        print(result)
        print()
        assert "xyz" in r
