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

    def dict(self, elements, kind=None):
        # this is an internal function for building dict object
        d = []
        for element in elements:
            entry = element.__dict__
            entry["cm"] = {}
            entry["cm"]["kind"] = "storage"
            entry["cm"]["cloud"] = "azure"
            entry["cm"]["name"] = element.name
            element.properties = element.properties.__dict__
            entry["cm"]["created"] = element.properties["creation_time"].isoformat()
            entry["cm"]["updated"] = element.properties["last_modified"].isoformat()
            entry["cm"]["size"] = element.properties["content_length"]
            del element.properties["copy"]
            del element.properties["lease"]
            del element.properties["content_settings"]
            del element.properties["creation_time"]
            del element.properties["last_modified"]
            if element.properties["deleted_time"] is not None:
                entry["cm"]["deleted"] = element.properties["deleted_time"].isoformat()
                del element.properties["deleted_time"]
            d.append(entry)
        return d

    def get(self, source, destination, recursive):
        #Download file from Destination(Service) to Source(local)
        HEADING()
        #Determine service path - file or folder
        if re.search("\.", os.path.basename(destination)) is None:
            blob_folder = destination[1:]
            blob_file = None
        else:
            blob_file = os.path.basename(destination)
            if re.search('/', destination) is None:
                blob_folder = None
            else:
                blob_folder = os.path.dirname(destination)[1:]
        # Determine local path i.e. download-to-folder
        if source.startswith('~'):
            src_path = path_expand(source)
        elif source.startswith('/'):
            src_path = source
        elif source == '.':
            src_path = os.getcwd()
        else:
            src_path = os.path.join(os.getcwd(), source)

        if not os.path.isdir(src_path):
            print('Not a valid local directory')
        else:
            obj_list = []
            if blob_folder is None:
                #file only specified
                if recursive == False:
                    if self.block_blob_service.exists(self.container, blob_file):
                        download_path = os.path.join(src_path, blob_file)
                        obj_list.append(self.block_blob_service.get_blob_to_path(self.container, blob_file, download_path))
                        #pprint(blob.__dict__)
                        #build dict object
                    else:
                        print('file does not exist')
                else:
                    file_found = 'N'
                    get_gen = self.block_blob_service.list_blobs(self.container)
                    for blob in get_gen:
                        if os.path.basename(blob.name) == blob_file:
                            print('IF-loop')
                            pprint(blob.__dict__)
                            download_path = os.path.join(src_path, blob_file)
                            obj_list.append(self.block_blob_service.get_blob_to_path(self.container, blob.name, download_path))
                            file_found = 'Y'
                            pprint(blob.__dict__)
                            # Build dict Object
                    if file_found == 'N':
                        print('File does not exist')
            else:
                if blob_file is None:
                    #Folder only specified
                    if recursive == False:
                        file_found = 'N'
                        get_gen = self.block_blob_service.list_blobs(self.container)
                        for blob in get_gen:
                            if os.path.dirname(blob.name) == blob_folder:
                                download_path = os.path.join(src_path, os.path.basename(blob.name))
                                obj_list.append(self.block_blob_service.get_blob_to_path(self.container, blob.name, download_path))
                                pprint(blob.__dict__)
                                file_found = 'Y'
                                # Build dict Object
                        if file_found == 'N':
                            print('Directory does not exist on Azure storage')
                    else:
                        file_found = 'N'
                        srch_gen = self.block_blob_service.list_blobs(self.container)
                        for blob in srch_gen:
                            if (os.path.dirname(blob.name) == blob_folder) or \
                                (os.path.commonpath([blob.name, blob_folder]) == blob_folder):
                                download_path = os.path.join(src_path, os.path.basename(blob.name))
                                obj_list.append(self.block_blob_service.get_blob_to_path(self.container, blob.name, download_path))
                                #pprint(blob.__dict__)
                                file_found = 'Y'
                                # Build dict Object
                        if file_found == 'N':
                            print('Directory does not exist on Azure storage')
                else:
                    # SOURCE is specified with Directory and file
                    if recursive == False:
                        # if recursive == 'N':
                        if self.block_blob_service.exists(self.container, destination[1:]):
                            download_path = os.path.join(src_path, blob_file)
                            obj_list.append(self.block_blob_service.get_blob_to_path(self.container, destination[1:], download_path))
                            # Build dict Object
                        else:
                            print('File does not exist')
                    else:
                        print('Invalid arguments, recursive not applicable')
        dict_obj = self.dict(obj_list)
        pprint(dict_obj)
        return dict_obj

    def put(self, source, destination, recursive):
        #Upload file from Source(local) to Destination(Service)
        HEADING()
        #Determine service path - file or folder
        if re.search("\.", os.path.basename(destination)) is None:
            blob_folder = destination[1:]
            blob_file = None
        else:
            print('Not a valid service folder')

        # Determine local path i.e. upload-from-folder
        if source.startswith('~'):
            src_path = path_expand(source)
        elif source.startswith('/'):
            src_path = source
        elif source == '.':
            src_path = os.getcwd()
        else:
            src_path = os.path.join(os.getcwd(), source)

        if os.path.isdir(src_path) or os.path.isfile(src_path):
            dict_obj = []
            if (re.search('\.', os.path.basename(src_path))) and \
                (not os.path.basename(src_path).startswith('.')):
                #File only specified
                upl_path = src_path
                upl_file = blob_folder + '/' + os.path.basename(src_path)
                obj = self.block_blob_service.create_blob_from_path(self.container, upl_file, upl_path)
                entry = obj.__dict__
                entry["cm"] = {}
                entry["cm"]["kind"] = "storage"
                entry["cm"]["cloud"] = "azure"
                entry["cm"]["name"] = upl_file
                entry["cm"]["created"] = obj.last_modified.isoformat()
                entry["cm"]["updated"] = obj.last_modified.isoformat()
                entry["cm"]["size"] = os.stat(upl_path).st_size
                del obj.last_modified
                dict_obj.append(entry)
                # build dict obj
            else:
                #Folder only specified - Upload all files from folder
                if recursive == True:
                    for file in os.listdir(src_path):
                        if os.path.isfile(os.path.join(src_path, file)):
                            upl_path = os.path.join(src_path, file)
                            upl_file = blob_folder + '/' + file
                            obj = self.block_blob_service.create_blob_from_path(self.container, upl_file, upl_path)
                            entry = obj.__dict__
                            entry["cm"] = {}
                            entry["cm"]["kind"] = "storage"
                            entry["cm"]["cloud"] = "azure"
                            entry["cm"]["name"] = upl_file
                            entry["cm"]["created"] = obj.last_modified.isoformat()
                            entry["cm"]["updated"] = obj.last_modified.isoformat()
                            entry["cm"]["size"] = os.stat(upl_path).st_size
                            del obj.last_modified
                            dict_obj.append(entry)
                            #build dict obj
                else:
                    print('Source is a folder, recursive expected in arguments')
        else:
            print('Not a valid local file or directory')

        pprint(dict_obj)
        return dict_obj

    def delete(self, source):
        HEADING()
        if re.search("\.", os.path.basename(source)) is None:
            print('test')
            blob_folder = source[1:]
            blob_file = None
        else:
            blob_file = os.path.basename(source)
            if re.search('/', source) is None:
                blob_folder = None
            else:
                blob_folder = os.path.dirname(source)[1:]

        if blob_folder is None:
            # SOURCE specified is File only
            if self.block_blob_service.exists(self.container, blob_file):
                self.block_blob_service.delete_blob(self.container, blob_file)
                pprint(blob_file.__dict__)
                # Build dict object
            else:
                print("file does not exist")
        else:
            if blob_file is None:
                #SOURCE specified is Folder only
                del_gen = self.block_blob_service.list_blobs(self.container)
                for blob in del_gen:
                    if os.path.commonpath([blob.name, blob_folder]) == blob_folder:
                        self.block_blob_service.delete_blob(self.container, blob.name)
                        pprint(blob.__dict__)
                        #Build dict object
            else:
                #Source specified is both file and directory
                if self.block_blob_service.exists(self.container, blob_file):
                    self.block_blob_service.delete_blob(self.container, blob_file)
                    pprint(blob_file.__dict__)
                    # Build dict object
                else:
                    print("file does not exist")

    def create_dir(self, directory):
        HEADING()
        if self.block_blob_service.exists(self.container):
            blob_cre =[]
            data = b' '
            blob_name = directory[1:] + '/dummy.txt'
            self.block_blob_service.create_blob_from_bytes(self.container, blob_name, data)
            blob_cre.append(self.block_blob_service.get_blob_to_bytes(self.container, blob_name))
            dict_obj = self.dict(blob_cre)
            pprint(dict_obj)
        return dict_obj

    def search(self, directory, filename, recursive):
        HEADING()
        srch_gen = self.block_blob_service.list_blobs(self.container)
        print("searching...")
        obj_list = []
        if recursive == False:
            srch_file = os.path.join(directory[1:], filename)
            print(srch_file)
            for blob in srch_gen:
                if blob.name == srch_file:
                    obj_list.append(blob)
                    print('File found:' + blob.name)
                    # Build dict object
        else:
            file_found = 'N'
            for blob in srch_gen:
                if re.search('/', blob.name) is not None:
                    if os.path.basename(blob.name) == filename:
                        if os.path.commonpath([blob.name, directory[1:]]) == directory[1:]:
                            obj_list.append(blob)
                            file_found = 'Y'
                            print('File Found:' + blob.name)
                            #Build dict object
                            #break
            if file_found == 'N':
                print('File not found ')
        dict_obj = self.dict(obj_list)
        pprint(dict_obj)
        return dict_obj

    def list(self, source, recursive):
        HEADING()
        #self.blob_file, self.blob_folder = self.service_path(source)

        if re.search("\.", os.path.basename(source)) is None:
            print('test')
            blob_folder = source[1:]
            blob_file = None
        else:
            blob_file = os.path.basename(source)
            if re.search('/', source) is None:
                blob_folder = None
            else:
                blob_folder = os.path.dirname(source)[1:]

        obj_list =[]
        if blob_folder is None:
            # SOURCE specified is File only
            if recursive == False:
                if self.block_blob_service.exists(self.container, blob_file):
                    blob_prop = self.block_blob_service.get_blob_properties(self.container, blob_file)
                    blob_size = self.block_blob_service.get_blob_properties(self.container,
                                                                           blob_file).properties.content_length
                    obj_list.append(blob_prop)
                    # Build dict Object
                else:
                    print('File does not exist')
            else:
                file_found = 'N'
                srch_gen = self.block_blob_service.list_blobs(self.container)
                for blob in srch_gen:
                    if os.path.basename(blob.name) == blob_file:
                        obj_list.append(blob)
                        pprint(blob.__dict__)
                        file_found = 'Y'
                        # Build dict Object
                if file_found == 'N':
                    print('File does not exist')
        else:
            if blob_file is None:
                #SOURCE specified is Directory only
                if recursive == False:
                #if recursive == 'N':
                    file_found = 'N'
                    srch_gen = self.block_blob_service.list_blobs(self.container)
                    for blob in srch_gen:
                        if os.path.dirname(blob.name) == blob_folder:
                            obj_list.append(blob)
                            pprint(blob.__dict__)
                            file_found = 'Y'
                            # Build dict Object
                    if file_found == 'N':
                        print('Directory does not exist on Azure storage')
                else:
                    file_found = 'N'
                    srch_gen = self.block_blob_service.list_blobs(self.container)
                    for blob in srch_gen:
                        if (os.path.dirname(blob.name) == blob_folder) or \
                        (os.path.commonpath([blob.name, blob_folder]) == blob_folder):
                            obj_list.append(blob)
                            pprint(blob.__dict__)
                            file_found = 'Y'
                            # Build dict Object
                    if file_found == 'N':
                        print('Directory does not exist on Azure storage')
            else:
                #SOURCE is specified with Directory and file
                if recursive == False:
                #if recursive == 'N':
                    if self.block_blob_service.exists(self.container, source[1:]):
                        blob_prop = self.block_blob_service.get_blob_properties(self.container, source[1:])
                        blob_size = self.block_blob_service.get_blob_properties(self.container,
                                                                                source[1:]).properties.content_length
                        obj_list.append(blob_prop)
                        # Build dict Object
                    else:
                        print('File does not exist')
                else:
                    print('Invalid arguments, recursive not applicable')
        dict_obj = self.dict(obj_list)
        pprint(dict_obj)
        return dict_obj
