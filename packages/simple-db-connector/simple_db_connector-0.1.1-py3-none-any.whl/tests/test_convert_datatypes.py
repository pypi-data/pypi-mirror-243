import os
from simple_db_connector import database
import decimal
import datetime


# Call the database class
db = database(
    os.environ["db_url"],
    os.environ["db_user"],
    os.environ["db_password"],
    os.environ["db_port"],
    os.environ["db_name"],
)

# Create a list of the most python data types
data_types = [
    "string", # String
    1, # Int
    1.1, # Float
    True, # Boolean
    b"Hello", # Bytes
    bytearray(5), # Bytearray
    memoryview(bytes(5)), # Memoryview
    None, # NoneType
    ["Hello", "World"], # List
    {"Hello": "World"}, # Dict
    ("Hello", "World"), # Tuple
    {"Hello", "World"}, # Set
    frozenset({"Hello", "World"}), # Frozenset
    range(5), # Range
    complex(1, 2), # Complex
    decimal.Decimal(1), # Decimal
    datetime.date(2020, 5, 17), # Date
]

# Convert every python data type
for data_type in data_types:
    print(db.data_typ_converter(data_type))