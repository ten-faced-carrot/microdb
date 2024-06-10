# MicroDB
MicroDB is a lightweight, NoSQL database that is designed to be easy to use and easy to understand. It is built on top of the `AutoSavingDict` class, 
which is a dictionary that automatically saves itself to a file whenever it is modified. This makes it easy to persist data between runs of your program.

MicroDB provides a simple API for interacting with the database. You can create tables, insert records, query records, and remove records.

## Installation
You can install MicroDB using pip:
```bash
pip install git+https://github.com/ten-faced-carrot/microdb.git
```


## Getting Started
Here's an example of how you might use MicroDB to store some data:
    
```python   
from microdb import MicroDB
db = MicroDB('mydb.json')

# Create a table
users = db.table('users')
# Insert some records
users.insert({'name': 'Alice', 'age': 30})
users.insert({'name': 'Bob', 'age': 25})
users.insert({'name': 'Charlie', 'age': 35})

# Query the records
from microdb import where # Where is a class that allows you to create simple queries. For more complex queries, you can use the Query class.

# Find all users with age less than 30
results = users.query(where('age') < 30)
for user in results.all():
    print(user)

# Remove the records
users.remove(where('age') < 30)
```

Or, you can use the `Query` class to create more complex queries:
```python
from microdb import Query
# Find all users with age less than or equal to 30 and name 'Alice'

results = users.query(Query().exists('age').value(Query.lte('age', 30)).exists('name').value('name', 'Alice'))
```

## Storage
You can also create in-memory databases by using this code:
```python
from microdb import MicroDB
from microdb.storage import InMemoryStorage

db = MicroDB(InMemoryStorage())
```

If you want to use a different storage backend, you can create your own storage class by creating a class implementing the `__getitem__`, `__setitem__`, `__delitem__`, and `__iter__` methods. You can then pass an instance of your storage class to the `MicroDB` constructor.


This is just a simple example to get you started. MicroDB is designed to be flexible and easy to use, so you can customize it to fit your needs.
