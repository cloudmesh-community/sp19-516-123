import cloudmesh.storage.provider.gdrive.Provider
import cloudmesh.storage.provider.box.Provider
import cloudmesh.storage.provider.azureblob.Provider


class Manager(object):

    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))

    def _provider(self, service):
        provider = None
        if service == "gdrive":
            provider = cloudmesh.storage.provider.gdrive.Provider.Provider()
        elif service == "box":
            provider = cloudmesh.storage.provider.box.Provider.Provider()
        elif service == "azureblob":
            provider = cloudmesh.storage.provider.azureblob.Provider.Provider()
        return provider

    def get(self, service, source, destination, recursive):
        print("get", service, source)
        provider = self._provider(service)
        d = provider.get(source, destination, recursive)
        return d

    def put(self, service, source, destination, recursive):
        print("put", service, source)
        provider = self._provider(service)
        d = provider.put(source, destination, recursive)
        return d

    def createdir(self, service, directory):
        print("createdir", directory)
        provider = self._provider(service)
        d = provider.create_dir(directory)
        return d

    def delete(self, service, source):
        print("delete filename", source)
        provider = self._provider(service)
        provider.delete(source)

    def search(self, service, directory, filename, recursive):
        print("search", directory)
        provider = self._provider(service)
        d = provider.search(directory, filename, recursive)
        return d

    def list(self, service, source, recursive):
        print("list", source)
        provider = self._provider(service)
        d = provider.list(source, recursive)
        return d
