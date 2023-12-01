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
table_name =  "cars_table"  

# Example Search Parameter
search_parameter =  {
	"manufacture" : "toyoat"
} 

# Example Table creation 
db.get_db_entrys(table_name, search_parameter)

# Example Table Name 
table_name =  "cars_table"  

# Example Search Parameter
search_parameter =  {
	"manufacture" : "toyoat",
	"model" : "Aygo X yalp",
} 
# Example Search Operator
search_operator = ["AND"]

# Example Table creation 
print(db.get_db_entrys(table_name, search_parameter, search_operator))