# 接口文件 (基于 file_service.py 生成)



class IFileStorageClient(ABC):
    @abstractmethod
    async def upload(self, file, config_obj):
        pass

    @abstractmethod
    async def download(self, config_obj, file_path):
        pass


class IS3FileStorageClient(ABC):
    @abstractmethod
    async def upload(self, file, config_obj):
        pass

    @abstractmethod
    async def download(self, config_obj, file_path):
        pass


class ISftpFileStorageClient(ABC):
    @abstractmethod
    async def upload(self, file, config_obj):
        pass

    @abstractmethod
    async def download(self, config_obj, file_path):
        pass


class IFtpFileStorageClient(ABC):
    @abstractmethod
    async def upload(self, file, config_obj):
        pass

    @abstractmethod
    async def download(self, config_obj, file_path):
        pass


class ILocalFileStorageClient(ABC):
    @abstractmethod
    async def upload(self, file, config_obj):
        pass

    @abstractmethod
    async def download(self, config_obj, file_path):
        pass


class IFileService(ABC):
    @abstractmethod
    async def upload(self, file):
        pass

    @abstractmethod
    async def get(self, configType, filePath):
        pass

    @abstractmethod
    async def UpdateDeafultUploadConfig(self, configId):
        pass

