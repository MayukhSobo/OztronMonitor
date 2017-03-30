from abc import ABC, abstractmethod
import pymongo
from pymongo.errors import ServerSelectionTimeoutError


class Database(ABC):
    """
    Generic Database helper class. Abstract class
    to perform connection and authentication with
    the data base. Must be inherited by other database
    classes for extended support.
    """
    def __init__(self, configParams, dataBaseName='device', dataBaseType='mongo',
                 uri='localhost:27017', timeOut=2):
        if dataBaseType not in ['mongo', 'influx']:
            raise NotImplementedError('OOPs!! {} is not supported yet'.format(dataBaseType))
        if timeOut < 1:
            raise ValueError('Database time out can not be {}'.format(timeOut))
        self._client = None
        # ------- Validation of the db parameters -------- #
        self.connect(uri, timeOut)

    def connect(self, uri, timeOut):
        # // TODO Find out a better way to authenticate
        try:
            self._client = pymongo.MongoClient(uri, connect=False,
                                               serverSelectionTimeoutMS=timeOut)
            self._client.server_info()
        except ServerSelectionTimeoutError:
            raise ConnectionError('Error connecting database server with {}'.format(uri))

    @property
    def client(self): return self._client

    @abstractmethod
    def work(self): pass

    @abstractmethod
    def clean(self): pass

db = Database(None)