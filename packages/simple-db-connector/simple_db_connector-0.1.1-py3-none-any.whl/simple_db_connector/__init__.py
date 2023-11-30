import mysql.connector
import os
import json
import logging
import uuid

def get_keys_out_of_dict(dict):
    keys = []
    for key in dict.keys():
        keys.append(key)
    return keys

def get_values_out_of_dict(dict):
    values = []
    for value in dict.values():
        values.append(value)
    return values


class database:
    def __init__(self, db_url, db_user, db_password, db_port, db_name):
        try:
            # Set DB Variables
            self.db_url = db_url
            self.db_user = db_user
            self.db_password = db_password
            self.db_port = db_port
            self.db_name = db_name

        except Exception as e:
            raise Exception("An error occurred while initiating the class object. Error: " + e)

    def data_typ_converter(self, python_type):
        switcher = {
            "str": "VARCHAR(255)",
            "int": "INT",
            "float": "FLOAT",
            "bool": "BOOLEAN",
            "bytes": "BLOB",
            "bytearray": "BLOB",
            "memoryview": "BLOB",
            "NoneType": "NULL",
            "list": "VARCHAR(255)",
            "dict": "VARCHAR(255)",
            "tuple": "VARCHAR(255)",
            "set": "VARCHAR(255)",
            "frozenset": "VARCHAR(255)",
            "range": "VARCHAR(255)",
            "complex": "VARCHAR(255)",
            "Decimal": "DECIMAL",
            "date": "DATE",
        }

        return switcher[type(python_type).__name__]

    def connect_db(self):
        self.mydb = mysql.connector.connect(
            host=self.db_url,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port,
            database=self.db_name,
        )
        self.mycursor = self.mydb.cursor(dictionary=True)

    def generate_guid(self):
        return str(uuid.uuid4())

    def check_table(self, table):
        try:
            self.connect_db()
            query = f"SHOW TABLES LIKE '{table}'"
            self.mycursor.execute(query)
            for row in self.mycursor:
                return True
            return False
        except Exception as e:
            raise Exception("An error occurred while checking the table. Error: " + e)

    def create_table(self, table, dict):
        try:
            if not self.check_table(table):
                keys = get_keys_out_of_dict(dict)
                self.connect_db()

                query = f"CREATE TABLE {table} (id VARCHAR(36) NOT NULL PRIMARY KEY"

                for key in keys:
                    query += f", {key} {self.data_typ_converter(dict[key])}"

                query += ")"
                self.mycursor.execute(query)
            else:
                raise Exception(f"Table with the name {table} already exists.")
        except Exception as e:
            raise Exception("An error occurred while creating the table. Error: " + e)

    def check_db_entry(self, table, search_parameter, operators = None):
        try:
            if self.check_table(table):
                self.connect_db()

                query = f"SELECT * FROM {table} WHERE " + self.create_sql_condition(
                    search_parameter, operators
                )

                self.mycursor.execute(query)
                if len(self.mycursor.fetchall()) == 0:
                    return False
                else:
                    return True
            else:
                raise Exception(f"An error occurred while checking the table entry. Error: The table {table} does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while checking the table entry. Error: " + e)

    def create_db_entry(self, table, data, search_column_prime_key="id"):
        try:
            if hasattr(data, search_column_prime_key):
                current_id = data[search_column_prime_key]
            else:
                current_id = self.generate_guid()  # self.check_id_exists(table)
                data[search_column_prime_key] = current_id

            if self.check_table(table):
                if not self.check_db_entry(table, {search_column_prime_key: data[search_column_prime_key]}):
                    self.connect_db()
                    keys = get_keys_out_of_dict(data)
                    values = get_values_out_of_dict(data)
                    query = f"INSERT INTO {table} (id, "
                    query += ", ".join(keys)
                    query += f') VALUES ("{current_id}", '
                    count = 0
                    for value in values:
                        counter = 0
                        count += 1
                        if type(value) == str:
                            query += f'"{value}", '
                        elif type(value) == list:
                            query_temp = ""
                            for item in value:
                                counter += 1
                                if not len(value) == 1:
                                    if query_temp == "":
                                        query_temp += f'"{item}, '
                                    elif counter == len(value):
                                        query_temp += f'{item}"'
                                    else:
                                        query_temp += f"{item}, "
                                else:
                                    query_temp += f'"{item}'
                            query += query_temp

                        else:
                            query += f"{value}, "

                        if count == len(values) and counter == 0:
                            query = query[:-2]
                    if 'query_temp' in locals():
                        if "," in query_temp:
                            query += ")"
                        else:
                            query += '")'
                    else:
                        query += ")"
                    self.mycursor.execute(query)
                    self.mydb.commit()
                else:
                    raise Exception(f"An error occurred while creating the table entry. Error: The entry with the same search parameter doss already exist.")
            else:
                raise Exception(f"An error occurred while creating the table entry. Error: The table {table} does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while creating the table entry. Error: " + e)

    def get_db_entrys(self, table, search_parameter, search_operator=None):
        try:
            if self.check_table(table):
                self.connect_db()

                query = f"SELECT * FROM {table} WHERE " + self.create_sql_condition(
                    search_parameter, search_operator
                )
                self.mycursor.execute(query)
                self.output = {"status": True}
                return self.mycursor.fetchall()
            else:
                raise Exception(f"An error occurred while getting the table entrys. Error: The table {table} does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while getting the table entrys. Error: " + e)

    def update_entry(self, table, search_parameter, update_parameter, operators = None):
        try:
            if self.check_table(table):
                if self.check_db_entry(table, search_parameter):
                    keys = get_keys_out_of_dict(update_parameter)
                    set_query = ""
                    for key in keys:
                        if set_query == "":
                            set_query += f'{key}="{update_parameter[key]}"'
                        else:
                            set_query += f', {key}="{update_parameter[key]}"'

                    self.connect_db()

                    query = (
                        f"UPDATE {table} SET "
                        + set_query
                        + " WHERE "
                        + self.create_sql_condition(search_parameter, operators)
                    )

                    self.mycursor.execute(query)
                    self.mydb.commit()
                    self.output = {"status": True}
                else:
                    raise Exception(f"An error occurred while updating the table entrys. Error: The table entry does not exist.")
            else:
                raise Exception(f"An error occurred while updating the table entrys. Error: The table {table} does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred while updating the table entrys. Error: " + e)

    def create_sql_condition(self, search_parameter, operators = None):
        try:
            keys = get_keys_out_of_dict(search_parameter)
            query = ""
            count = 0
            for key in keys:
                if operators ==     None:
                    operator = "and"
                try:
                    operator = operators[count]
                except:
                    operator = "and"

                if query == "":
                    query += f'{key}="{search_parameter[key]}"'
                else:
                    query += f' {operator} {key}="{search_parameter[key]}"'
                
                count += 1
            return query
        except:
            raise Exception(f"An error occurred while creating the sql condition. Error: " + e)