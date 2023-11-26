import json
import pymysql
import pymysql.cursors


class Db:
    # This is the connection class for MySQL.  If you are using a different database
    # change this function to connect properly.

    def __init__(self):
        pass

    @classmethod
    def connect(cls, connection_vault_path):
        try:
            with open(connection_vault_path, 'r') as connection_file:
                connection_dict = json.load(connection_file)

            return pymysql.connect(
                host=connection_dict['host'],
                user=connection_dict['user'],
                password=connection_dict['password'],
                database=connection_dict['database'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except FileNotFoundError:
            return {"error_code": "5501", "error_msg": "Connection Vault " + str(connection_vault_path) + " not found.", "data": {}}
        except json.JSONDecodeError as e:
            return {"error_code": "5502", "error_msg": "Error decoding JSON" + str(e), "data": {}}
