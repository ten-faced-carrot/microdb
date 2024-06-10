from typing import overload

class QueryDriver:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _record_exists(name):
        def wrapper(record):
            return name in record
        return wrapper
    
    @staticmethod
    def _record_equality(name, value):
        def wrapper(record):
            return record.get(name) == value
        
        return wrapper
    
class QueryResult:
    
    def __init__(self, results: list):
        self._rows = results

    @classmethod
    def from_list(cls, results: list):
        return cls(results)

    @classmethod
    def none(cls):
        return cls([])

    def all(self):
        return self._rows
    
    def first(self):
        return self._rows[0]
    
    def final(self):
        return self._rows[-1]

    def count(self):
        return len(self._rows)
    


class Query:
    def __init__(self) -> None:
        self._actionchain = []

    def exists(self, name):
        self._actionchain.append(QueryDriver._record_exists(name))
        return self
    
    @overload
    def value(self, name,value):
        pass

    @overload
    def value(self, subquery):
        pass

    def value(self, subquery_or_name, value=None):
        if value:
            self._actionchain.append(QueryDriver._record_equality(subquery_or_name,value))
        else:
            self._actionchain.append(subquery_or_name)
        return self
    
    @staticmethod
    def lt(name, value):
        def fw(r):
            return r[name] < value
        return fw
    
    @staticmethod
    def gt(name, value):
        def fw(r):
            return r[name] > value
        return fw
    
    @staticmethod
    def neq(name, value):
        def fw(r):
            return r[name] != value
        return fw
    
    @staticmethod
    def lte(name, value):
        def fw(r):
            return r[name] <= value
        return fw
    
    @staticmethod
    def gte(name, value):
        def fw(r):
            return r[name] >= value
        return fw
    

    def _find_all_records(self, records:list):

        possibleResults = records[:]
        for i,record in enumerate(possibleResults):
            for cond in self._actionchain:
                if not cond(record):
                    possibleResults.remove(record)
                    continue
            


        return QueryResult(possibleResults)


class where:
    def __init__(self, name) -> None:
        self._actionchain = []
        self.name = name

    def __eq__(self, value: object):
        self._actionchain.append(QueryDriver._record_equality(self.name,value))
        return self

    def __lt__(self, value: object):
        def fw(r):
            return r[self.name] < value
        self._actionchain.append(fw)
        return self

    def __gt__(self, value: object):
        def fw(r):
            return r[self.name] > value
        self._actionchain.append(fw)
        return self

    def __ne__(self, value: object) -> bool:
        def neq(record):
            return record.get(self.name) != value
        self._actionchain.append(neq)
        return self
 

    def _find_all_records(self, records:list):
        possibleResults = records[:]
        for i,record in enumerate(possibleResults):
            for cond in self._actionchain:
                if not cond(record):
                    possibleResults.remove(record)
                    continue

        return QueryResult(possibleResults)