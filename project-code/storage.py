from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.storage.api.manager import Manager
from cloudmesh.shell.variables import Variables
from pprint import pprint
from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter


# noinspection PyBroadException
class StorageCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_storage(self, args, arguments):
        """
        ::

          Usage:
                storage [--storage=SERVICE] put FILENAME SOURCEDIR
                storage [--storage=SERVICE] get FILENAME DESTDIR
                storage [--storage=SERVICE] delete file FILENAME
                storage [--storage=SERVICE] list file DIRNAME
                storage [--storage=SERVICE] info FILENAME
                storage [--storage=SERVICE] create dir DIRNAME
                storage [--storage=SERVICE] list dir
                storage [--storage=SERVICE] delete dir DIRNAME


          This command does some useful things.

          Arguments:
              FILENAME   a BLOB name
              SOURCEDIR  local path for the FILENAME to be uploaded
              DESTDIR    local path for the FILENAME to be downloaded

          Options:
              --storage=SERVICE  specify the cloud service name like aws or azure or box or google

          Description:
                commands used to upload, download, list files on different cloud storage services.

                storage put [options..]
                    Uploads the file specified in the filename to specified cloud from the SOURCEDIR.

                storage get [options..]
                    Downloads the file specified in the filename from the specified cloud to the DESTDIR.

                storage delete file [options..]
                    Deletes the file specified in the filename from the specified cloud.

                storage list file [options..]
                    lists all the files from the container name specified on the specified cloud.

                storage info [options..]
                    returns the properties of the filename specified on the specified cloud.

                storage create dir [options..]
                    creates a folder with the directory name specified on the specified cloud.

                storage list dir [options..]
                    lists all the folders on the specified cloud.

                storage delete dir [options..]
                    deletes all the files in the directory specified on the specified cloud.


          Example:
            set storage=azureblob
            storage put FILENAME SOURCEDIR

            is the same as 

            storage --storage=azureblob put FILENAME SOURCEDIR


        """
        # arguments.CONTAINER = arguments["--container"]
        arguments.SERVICE = arguments["--storage"]
        pprint(arguments)

        m = Manager()

        service = None

        try:
            service = arguments["--storage"][0]
        except Exception as e:
            try:
                v = Variables()
                service = v['storage']
            except Exception as e:
                service = None

        if service is None:
            Console.error("storage service not defined")

        if arguments['get']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.get(arguments.SERVICE, arguments.FILENAME, arguments.DESTDIR)

        elif arguments['put']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.put(arguments.SERVICE, arguments.FILENAME, arguments.SOURCEDIR)

        elif arguments['delete'] and  arguments['file']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.delete(arguments.SERVICE, arguments.FILENAME)

        elif arguments['list'] and arguments['file']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.listfiles(arguments.SERVICE, arguments.DIRNAME)

        elif arguments['info']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.info(arguments.SERVICE, arguments.FILENAME)

        elif arguments['create'] and arguments['dir']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.createdir(arguments.SERVICE, arguments.DIRNAME)

        elif arguments['list'] and arguments['dir']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.listdir(arguments.SERVICE)

        elif arguments['delete'] and arguments['dir']:
            if arguments.SERVICE is None:
                variables = Variables()
                arguments.SERVICE = variables['storage']
            m.deletedir(arguments.SERVICE, arguments.DIRNAME)

