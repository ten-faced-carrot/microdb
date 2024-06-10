from microdb.utils import AutoSavingDict
import abc
import typing as t
import operator
from microdb.query import QueryResult, Query, where

class Model(abc.ABC):

    @abc.abstractmethod
    def query(self, _query):
        pass

    @abc.abstractmethod
    def remove(self, _query):
        pass


    @abc.abstractmethod
    def insert(self, record):
        pass

    
class MDB_Table(Model):
    def __init__(self,name, raw) -> None:
        self.raw = raw
        self.name = name
        if not self.name in self.raw:
            self.raw[self.name] = []
        super().__init__()

    def insert(self, record):
        if isinstance(record, dict):
            self.raw[self.name].append(record)
        else:
            self.raw[self.name].append(record, self.name)
        self.raw.save()

    def query(self, _query=Query()) -> QueryResult:
        return _query._find_all_records(self.raw[self.name])
    
    def remove(self, _query):
        for i in _query._find_all_records(self.raw[self.name]).all():
            self.raw[self.name].remove(i)

    def table(self, name):
        return MDB_Table(name, self._raw)

class MicroDB(MDB_Table):
    def __init__(self, db=None, *, storage=AutoSavingDict) -> None:
        
        self._raw = storage(filename=db)
        super().__init__('_default',self._raw)

    def commit(self):
        """
        Persist the data to the storage
        """
        self._raw.save()
    
    def table(self, name):
        return MDB_Table(name, self._raw)
