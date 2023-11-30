# Simple_Python_DB_Connector

Python module for simple connection and editing of databases.

## Installation

To install the python module, enter the following code in the terminal. Remember, "python" must be swapped with the Python interpreter installed on your system:

```sh
python -m pip install simple-db-connector
```

## Usage Example

### Call Database Class

First of all, we call the "database" class. Im using the os modul to call my database parameter from my environment variables. I advise you to do this straight away, as it is very bad to have sensitive data such as passwords and IP addresses in plain text:

```python 
import  os
from  simple_db_connector  import  database

# Call the database class
db  =  database(
	os.environ["db_url"],
	os.environ["db_user"],
	os.environ["db_password"],
	os.environ["db_port"],
	os.environ["db_name"],
)
```

After we have called the class, we can also use the functions of the class. All functions are self-explanatory. Nevertheless, I will briefly explain the use of each function:

### *class* database.check_table 

##### Parameter
>table name: *string*

```python 
# Example Table Name
table_name = "test_table"

# if "test_table" exists return true, otherwise return false
print(db.check_table(table_name))
```

> It is also executed within the create_table function, so it is not necessary to execute this before you create a table.

### *class* database.create_table 

##### Parameter
	
>table name: *string*, table content: *dict*

```python 
# Example Table Name
table_name = "cars_table"

# Example Table Content
table_content = {
	"manufacture" : "toyoat",
	"model" : "Aygo X yalp",
	"ps" : 72, 
} 

# Example Table creation
db.create_table(table_name, table_content)
```

>This will create the table "cars_table" with the information contained in "test_content". In addition, a primary key field with the name "id" will be created too.  Currently this field is hard coded with a GUID field. In the near future, however, it will be possible to declare your own primary key field.

### *class* database.check_db_entry

##### Parameter

>table: *string*, search_parameter: *dict*
```python
# Example Table Name 
table_name =  "cars_table"  

# Example Search Parameter
search_parameter =  {
	"manufacture" : "toyoat"
}  

# Example Table creation 
db.check_db_entry(table_name, search_parameter)
```
>This will create the table "cars_table" with the information contained in "test_content". In addition, a primary key field with the name "ID" will be created too.  Currently this field is hard coded with a GUID field. In the near future, however, it will be possible to declare your own primary key field.

```python
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
db.check_db_entry(table_name, search_parameter, search_operator)
```
>It's also possible to have multiple search parameter

### *class* database.create_db_entry

##### Parameter
>table: *string*, data: *dict*, prime_key: *string*; default value = "id"

```python
# Example Table Name 
table_name =  "cars_table"  

# Example Table Content
table_content = {
	"manufacture" : "toyoat",
	"model" : "Aygo X yalp",
	"ps" : 72, 
} 

# Example Table prime key
prime_key = "id"
# To illustrate this, I have entered "id". However, if "prime_key" is empty, "id" is selected.

# Example 
db.create_db_entry(table_name, table_content, prime_key)
```

### *class* database.get_db_entrys

##### Parameter
>table: *string*, search_parameter: *dict*

```python
# Example Table Name 
table_name =  "cars_table"  

# Example Search Parameter
search_parameter =  {
	"manufacture" : "toyoat"
} 

# Example Table creation 
db.get_db_entrys(table_name, search_parameter)
```
```python
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
db.get_db_entrys(table_name, search_parameter, search_operator)
```
> As with check_db_entry, it is also possible to use several search parameters here

### *class* database.update_entry

##### Parameter
>table: *string*, search_parameter: *dict*, update_parameter *dict*

```python
# Example Table Name 
table_name =  "cars_table"  

# Example Search Parameter
search_parameter =  {
	"manufacture"  :  "toyoat"
}  
# Example Update Parameter
search_parameter =  {
	"manufacture"  :  "toyota"
} 

# Example Table creation 
db.update_entry(table_name, search_parameter)
```
```python
# Example Table Name 
table_name =  "cars_table"  

# Example Search Parameter
search_parameter =  {
	"manufacture" : "toyoat",
	"model" : "Aygo X yalp",
}
# Example Update Parameter
search_parameter =  {
	"manufacture"  :  "toyota"
	"model" : "Aygo X play",
} 
# Example Search Operator
search_operator = ["AND"]

# Example Table creation 
db.update_entry(table_name, search_parameter, search_operator)
```
> It's also possible to use multiple search and update parameter here