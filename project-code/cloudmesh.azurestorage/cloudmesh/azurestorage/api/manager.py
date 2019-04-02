form
cloudmesh.storage.provider.gdrive.Provider
import Provider as GoogleProvider
from cloudmesh.storage.provider.box.Provider import Provider as BoxProvider
from cloudmesh.storage.provider.azureblob.Provider import \
    Provider as AzureProvider
from cloudmesh.common.console import Console

class Manager(object):

    def __init__(self, name=None):
        if name is None:
            raise ValueError(f"the provider {name} is not defined")
        self._provider(self, service)

    # bug, must be called in init and init must have name as parameter, rename service here to name
    def _provider(self, service):
        provider = None
        if service == "gdrive":
            provider = GoogleProvider()
        elif service == "box":
            provider = BoxProvider()
        elif service == "azureblob":
            provider = AzureProvider(service)
        else:
            raise ValueError(f"the provider {service} is not defined")
        return provider

    def get(self, service, source, destination, recursive):
        Console.ok(f"get {service} {source}")
        provider = self._provider(service)
        d = provider.get(source, destination, recursive)
        return d

    def put(self, service, source, destination, recursive):
        Console.ok(f"put {service} {source}")
        provider = self._provider(service)
        d = provider.put(source, destination, recursive)
        return d

    def createdir(self, service, directory):
        Console.ok(f"createdir {directory}")
        provider = self._provider(service)
        d = provider.create_dir(directory)
        return d

    def delete(self, service, source):
        Console.ok(f"delete filename {service} {source}")
        provider = self._provider(service)
        provider.delete(source)

    def search(self, service, directory, filename, recursive):
        Console.ok(f"search {directory}")
        provider = self._provider(service)
        d = provider.search(directory, filename, recursive)
        return d

    def list(self, service, source, recursive):
        Console.ok(f"list {source}")
        provider = self._provider(service)
        d = provider.list(source, recursive)
        return d
