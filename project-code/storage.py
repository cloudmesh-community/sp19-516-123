        """
        ::

          Usage:
                storage [--storage=SERVICE] put CONTAINER FILENAME SOURCEDIR
                storage [--storage=SERVICE] get CONTAINER FILENAME DESTDIR
                storage [--storage=SERVICE] delete file CONTAINER FILENAME
                storage [--storage=SERVICE] list file CONTAINER
                storage [--storage=SERVICE] info CONTAINER FILENAME
                storage [--storage=SERVICE] create file CONTAINER FILENAME
                storage [--storage=SERVICE] create dir CONTAINER
                storage [--storage=SERVICE] list dir
                storage [--storage=SERVICE] delete dir CONTAINER


          This command does some useful things.

          Arguments:
              CONTAINER  a CONTAINER name
              FILENAME   a BLOB name
              SOURCEDIR  local download path for FILENAME 
              DESTDIR    local upload path for the FILENAME

          Options:
              --storage=SERVICE  specify the cloud service name like aws or azure or box or google

          Description:
                commands used to upload, download, list files on different cloud storage services.

                storage put [options..]
                    Uploads the file specified in the filename to the container name specified
                    on the specified cloud  from the SOURCEDIR.

                storage get [options..]
                    Downloads the file specified in the filename from the container name specified
                    on the specified cloud to the DESTDIR.

                storage delete file [options..]
                    Deletes the file specified in the filename from the container name specified
                    on the specified cloud.

                storage list file [options..]
                    lists all the files from the container name specified on the specified cloud.

                storage info [options..]
                    returns the properties of the filename specified from the container name specified
                    on the specified cloud.

                storage create dir [options..]
                    creates the container with the container name specified on the specified cloud.

                storage list dir [options..]
                    lists all the containers on the specified cloud.

                storage delete dir [options..]
                    deletes the container with the container name specified on the specified cloud.


          Example:
            set storage=azure
            storage put CONTAINER FILENAME

            is the same as 

            storage --storage=azure put CONTAINER FILENAME


        """
