"""
MicroDB Middlewares
===================
MicroDB middlewares are classes that can be used to extend the functionality of MicroDB. They can be used to add additional features to the database, such as caching, logging, or authentication.

IMPORTANT: This feature is not yet implemented working in the current version of MicroDB. It is planned for a future release.
"""

import abc
import typing as t
from microdb.utils import AutoSavingDict
import logging

class Middleware(abc.ABC, dict):

    def __init__(self, db: t.Any) -> None:
        if isinstance(db, dict): 
            self.db = db
        elif isinstance(db, str): 
            self.db = AutoSavingDict(filename=db)
    
    def append(self, record: t.Any) -> None:
        self.before_insert(record)
        self.db.append(record)

    def __setitem__(self, key: t.Any, value: t.Any) -> None:
        self.before_insert(key)
        self.db.__setitem__(key, value)

    def __getitem__(self, key: t.Any) -> t.Any:
        self.before_query(key)
        return self.db.__getitem__(key)
    
    def __delitem__(self, key: t.Any) -> None:
        self.before_remove(key)
        return self.db.__delitem__(key)

    @abc.abstractmethod
    def before_insert(self, record) -> t.Any:
        pass

    @abc.abstractmethod
    def before_query(self, record) -> t.Any:
        pass

    @abc.abstractmethod
    def before_remove(self, record) -> t.Any:
        pass


class LoggingMiddleware(Middleware):
    def __init__(self, db: t.Any) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__(db)
        
    def __setitem__(self, key: t.Any, value: t.Any) -> None:
        self.before_insert(key)
        self.db.__setitem__(key, value)

    def __getitem__(self, key: t.Any) -> t.Any:
        self.before_query(key)
        return self.db.__getitem__(key)
    
    def __delitem__(self, key: t.Any) -> None:
        self.before_remove(key)
        return self.db.__delitem__(key)
    
    def before_insert(self, record) -> t.Any:
        self.logger.info(f"Insert Record {record}")

    def before_query(self, record) -> t.Any:
        self.logger.info(f"Query Record {record}")
    
    def before_remove(self, record) -> t.Any:
        self.logger.info(f"Remove Record {record}")