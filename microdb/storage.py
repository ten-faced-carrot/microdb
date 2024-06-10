"""
Custom storage classes for MicroDB

This module provides custom storage classes for MicroDB. These classes can be used to create in-memory databases or to customize the way that data is stored.

InMemoryStorage: A storage class that stores data in memory. This class is useful for creating in-memory databases that do not persist data between runs of your program.

Implementing a custom storage class is as simple as subclassing the `dict` class and implementing the `save` and `__call__` method. For example:
    
    ```python
    class MyStorage(dict):
        def __call__(self, filename) -> None:
            super().__init__()
            
        def save(self):
            # Implement the save method here
            pass
    ```
"""
from typing import Any

class InMemoryStorage(dict):
    
    def __call__(self, *args, **kwargs) -> None:
        # Here could be some logic, but since we are creating an in-memory storage, we don't need to do anything here
        return self
    
    def save(self):
        pass