import json
from typing import Any

class AutoSavingDict(dict):
    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, value)
        self.save()
    
    def __delitem__(self, key: Any) -> None:
        super().__delitem__(key)
        self.save()

    def __init__(self,*,filename="_autosd.json", **kwa) -> None:
        
        data = kwa
        for k,v in self.load().items():
            data[k]=v
        if not filename:
            filename = "_autosd.json"
        self.__file__ = filename
        super().__init__(data)
    
    def load(self):
        try:
            with open(self.__file__, "r+") as f:
                a = json.load(f)
        except:
            a = {}
        return a

    def save(self):
        with open(self.__file__, "w+") as f:
            json.dump(self, f)