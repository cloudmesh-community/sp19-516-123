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

    def get(self, service, filename, destdir):
        print("get", service, filename)
        provider = self._provider(service)
        provider.get(filename, destdir)

    def put(self, service, filename, sourcedir):
        print("put", service, filename)
        provider = self._provider(service)
        provider.put(filename, sourcedir)

    def delete(self, service, filename):
        print("delete filename", filename)
        provider = self._provider(service)
        provider.delete(filename)

    def listfiles(self, service, dirname):
        print("list", dirname)
        provider = self._provider(service)
        provider.listfiles(dirname)

    def info(self, service, filename):
        print("info", filename)
        provider = self._provider(service)
        provider.info(filename)

    def createdir(self, service, dirname):
        print("createdir", dirname)
        provider = self._provider(service)
        provider.createdir(dirname)

    def listdir(self, service):
        print("listdir")
        provider = self._provider(service)
        provider.listdir()

    def deletedir(self, service, dirname):
        print("deletedir", dirname)
        provider = self._provider(service)
        provider.deletedir(dirname)

    def search(self, service, directory, filename, recursive):
        print("search", directory)
        provider = self._provider(service)
        provider.search(directory, filename, recursive)