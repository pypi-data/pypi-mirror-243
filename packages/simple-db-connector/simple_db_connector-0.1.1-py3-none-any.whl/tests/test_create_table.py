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

# Example Table Name
table_name = "cars_table"

# Example Table Content
table_content = {
	"manufacture" : "toyota",
	"model" : "Aygo X play",
	"ps" : 72, 
} 

# Example Table creation
db.create_table(table_name, table_content)