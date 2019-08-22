from __future__ import print_function
from cloudmesh.shell.command import command


from cloudmesh.shell.command import PluginCommand, map_parameters
from cloudmesh.storage.Provider import Provider
from cloudmesh.common.variables import Variables
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
                storage [--storage=SERVICE] create dir DIRECTORY
                storage [--storage=SERVICE] get SOURCE DESTINATION [--recursive]
                storage [--storage=SERVICE] put SOURCE DESTINATION [--recursive]
                storage [--storage=SERVICE] list SOURCE [--recursive]
                storage [--storage=SERVICE] delete SOURCE
                storage [--storage=SERVICE] search  DIRECTORY FILENAME [--recursive]


          This command does some useful things.

          Arguments:
              SOURCE        SOURCE can be a directory or file
              DESTINATION   DESTINATION can be a directory or file
              DIRECTORY     DIRECTORY refers to a folder on the cloud service


          Options:
              --storage=SERVICE  specify the cloud service name like aws or azure or box or google
          Description:
                commands used to upload, download, list files on different cloud storage services.

                storage put [options..]
                    Uploads the file specified in the filename to specified cloud from the SOURCEDIR.

                storage get [options..]
                    Downloads the file specified in the filename from the specified cloud to the DESTDIR.

                storage delete [options..]
                    Deletes the file specified in the filename from the specified cloud.

                storage list [options..]
                    lists all the files from the container name specified on the specified cloud.

                storage create dir [options..]
                    creates a folder with the directory name specified on the specified cloud.

                storage search [options..]
                    searches for the source in all the folders on the specified cloud.

          Example:
            set storage=azureblob
            storage put SOURCE DESTINATION --recursive

            is the same as
            storage --storage=azureblob put SOURCE DESTINATION --recursive

        """
        # arguments.CONTAINER = arguments["--container"]

        map_parameters(arguments,
                       "recursive",
                       "storage")
        arguments.storage = arguments["--storage"]
        pprint(arguments)

        m = Provider()

        service = None

        #
        # BUG
        # services = Parameter.expand(arguments.storage)
        # service = services[0]
        # if services is None:
        #  ... do second try

        ##### BUG
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
            return

        # bug this is now done twice ....
        if arguments.storage is None:
            variables = Variables()
            arguments.storage = variables['storage']

        ##### Prvious code needs to be modified

        if arguments.get:
            m.get(arguments.storage, arguments.SOURCE, arguments.DESTINATION,
                  arguments.recursive)

        elif arguments.put:
            m.put(arguments.storage, arguments.SOURCE, arguments.DESTINATION,
                  arguments.recursive)

        elif arguments.list:
            print('in List')
            m.list(arguments.storage, arguments.SOURCE, arguments.recursive)

        elif arguments.create and arguments.dir.:
            m.createdir(arguments.storage, arguments.DIRECTORY)

        elif arguments.delete.:
            m.delete(arguments.storage, arguments.SOURCE)

        elif arguments['search']:
            m.search(arguments.storage, arguments.DIRECTORY, arguments.FILENAME,
                     arguments.recursive)
