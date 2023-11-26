###########################################################################################################
# KineticForms API Engine
#
# Copyright (c) 2023 - Kinetic Seas Inc.
# by Edward Honour and Joseph Lehman.
#
# KineticForms is a database access library originally designed to support KineticPdf and KineticEmail
#         designed for rapid application development.
#
#         It supports a simplified database interface that makes it possible to perform CRUD operations on your
#         database without deep knowledge of SQL.
#
###########################################################################################################
import json
import pymysql
import pymysql.cursors
from .db import Db
import hashlib

class KineticForms():

    # When an object of KineticForms is created, the path to connection information must
    # be specified.
    def __init__(self, connection):
        print(connection)
        if isinstance(connection, dict):
            self.connection_dict = connection
        else:
            with open(connection, 'r') as connection_file:
                self.connection_dict = json.load(connection_file)

    def connect(self):
        return pymysql.connect(
            host=self.connection_dict['host'],
            user=self.connection_dict['user'],
            password=self.connection_dict['password'],
            database=self.connection_dict['database'],
            cursorclass=pymysql.cursors.DictCursor
        )


    # execute any query and return multiple records as a list object.
    def sql(self, s, errors=True):
        try:
            conn = self.connect()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Connecting: " + str(err), "data": []}
            else:
                return []

        try:
            cursor = conn.cursor()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9998", "error_msg": "Error Creating Cursor: " + str(err), "data": []}
            else:
                return []

        try:
            cursor.execute(s)
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Executing: " + str(err), "data": []}
            else:
                return []

        try:
            records = cursor.fetchall()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Fetching: " + str(err), "data": []}
            else:
                return []

        if errors:
            return {"error_code": "0", "error_msg": "", "data": records}
        else:
            return records

    # Execute a query that you know will only return a single record.
    def sql0(self, s, errors=True):
        try:
            conn = self.connect()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Connecting: " + str(err), "data": {}}
            else:
                return {}

        try:
            cursor = conn.cursor()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Creating Cursor: " + str(err), "data": {}}
            else:
                return {}

        try:
            cursor.execute(s)
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Executing: " + str(err), "data": {}}
            else:
                return []
        try:
            records = cursor.fetchone()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Fetching: " + str(err), "data": {}}
            else:
                return []

        if errors:
            return {"error_code": "0", "error_msg": "", "data": records}
        else:
            return records

    # Execute an update statement.  Results will be automatically committed to the
    # database.
    def execute(self, s, errors=True):
        try:
            conn = self.connect()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Connecting: " + str(err), "data": {}}
            else:
                return {}

        try:
            cursor = conn.cursor()
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Creating Cursor: " + str(err), "data": {}}
            else:
                return {}

        try:
            cursor.execute(s)
        except pymysql.err.MySQLError as err:
            if errors:
                return {"error_code": "9999", "error_msg": "Error Executing: " + str(err), "data": []}
            else:
                return []

        try:
            conn.commit()
            return {"error_code": "0", "error_msg": "" + str(e), "data": {}}
        except Exception as e:
            return {"error_code": "9999", "error_msg": "Database Error: " + str(e), "data": {}}


    # returns an dict object that returns all the columns in a table with blank default values.
    def get_form(self, table_Name):

        try:
            conn = self.connect()
        except pymysql.err.MySQLError as err:
            return {"error_code": "9999", "error_msg": "Error Connecting: " + str(err), "data": {}}

        try:
            cursor = conn.cursor()
        except pymysql.err.MySQLError as err:
            return {"error_code": "9999", "error_msg": "Error Creating Cursor: " + str(err), "data": {}}

        columns = []
        sql = "SHOW COLUMNS FROM " + table_name
        try:
            cursor.execute(sql)
            columns = cursor.fetchall()
        except Exception as e:
            return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {}}

        output = {}
        for i in columns:
            output[i['Field']] = ""

        return {"error_code": "0", "error_msg": "", "data": output}

    # returns an dict object that returns all the columns of a record so it can be edited.
    def get_edit_form(self, sql):
        record = self.sql0(sql)
        if record.error_code == "0":
            x = removed_value = record.pop('create_timestamp', None)
            return {"error_code": "0", "error_msg": "", "data": output}
        else:
            return record

    def create_kinetic_infrastucture(self):
        sql = "create table if not exists pdf_touch (id varchar(64) not null) ENGINE = InnoDB"
        self.execute(sql)
        sql = "alter table pdf_touch add primary key('id')"
        self.execute(sql)


    # returns an dict object that returns all the columns of a record so it can be edited.
    def row_import(self, my_records, table_name):

        process_list = []
        if isinstance(my_records, dict):
            my_records['table_name'] = table_name
            my_records['action'] = "insert"
            process_list.append(my_records)
        elif isinstance(my_records, list):
            for i in my_records:
                if isinstance(i, dict):
                    i['table_name'] = table_name
                    i['action'] = "insert"
                    process_list.append(i)
                else:
                    return {"error_code": "6500", "error_msg": "Parameter 1 must be a dict or a list or dicts", "data": {}}
        else:
            return {"error_code": "6500", "error_msg": "Parameter 1 must be a dict or a list or dicts", "data": {}}

        results = []
        for i in process_list:
            results.append(self.post(i))

        return {"error_code": "0", "error_msg": "", "data": results}

    def clean_pdf_input(self, record):
        for i in record:
            if record[i] == '/Yes':
                record[i] = "on"
            if record[i] == '/Off':
                record[i] = "off"
        return record

    def clean_pdf_output(self, record, hint=None):

        if hint is None:
            hint = {}
        else:
            if isinstance(hint, dict):
                pass
            else:
                return {"error_code": "8000", "error_msg": "Hint Must be a dict containing key and field type.", "data": {}}

        if record['error_code'] == "0":
            data = record['data']
            for i in data:
                for k in hint:
                    if i == k:
                        if "checkbox" in hint[k]:
                            if data[i] == 'on':
                                data[i] = "/Yes"
                            elif data[i] == 'off':
                                data[i] = "/Off"
                            else:
                                data[i] = "/Off"
                        if "radio" in hint[k]:
                            data[i] = '/' + str(data[i])
            record['data'] = data
        else:
            return record


    def touched(self, input_dict):
        if 'data' in input_dict:
            s = json.dumps(input_dict['data'])
        else:
            s = json.dumps(input_dict)

        sha256_hash = hashlib.sha256()
        sha256_hash.update(s.encode())
        sha256 = sha256_hash.hexdigest()
        sql = "select count(*) as c from pdf_touch where id = '" + str(sha256) + "'"
        c = self.sql0(sql)
        count = c['data']['c']
        if c['data']['c'] > 0:
            return True
        else:
            return False


    def touch(self, input_dict):
        if 'data' in input_dict:
            s = json.dumps(input_dict['data'])
        else:
            s = json.dumps(input_dict)

        sha256_hash = hashlib.sha256()
        sha256_hash.update(s.encode())
        sha256 = sha256_hash.hexdigest()
        sql = "select count(*) as c from pdf_touch where id = '" + str(sha256) + "'"
        c = self.sql0(sql)
        count = c['data']['c']

        if c['data']['c'] > 0:
            return {"error_code": "1", "error_message": "Message was already processed", "data": { "id": sha256, "count": count }}
        else:
            sql = "insert into pdf_touch values ('" + str(sha256) + "')"
            self.execute(sql)
            return {"error_code": "0", "error_message": "", "data": {"id": sha256, "count": 0}}


    def clear_touch(self):
        sql = "delete from pdf_touch"
        self.execute(sql)
        return {"error_code": "0", "error_message": "", "data": {}}

    # Save a record to the database.
    # Simplified wrapper around .post()
    def save(self, my_dict, table_name):
        if isinstance(my_dict, dict):
            my_dict['table_name'] = table_name
            my_dict['action'] = "insert"
            return self.post(my_dict)
        else:
            return {"error_code": "9999", "error_msg": "Parameter must be a dict", "data": {}}

    # Save a record to the database after checking to see if it exists based on the keys
    # provided.
    def merge(self, my_dict, table_name, keys):

        if isinstance(my_dict, dict):
            pass
        else:
            return {"error_code": "9999", "error_msg": "Parameter must be a dict", "data": {}}

        if isinstance(keys, list):
            pass
        else:
            return {"error_code": "9999", "error_msg": "Keys must be a list of columns", "data": {}}

        try:
            conn = self.connect()
        except pymysql.err.MySQLError as err:
            return {"error_code": "9999", "error_msg": "Error Connecting: " + str(err), "data": {}}

        try:
            cursor = conn.cursor()
        except pymysql.err.MySQLError as err:
            return {"error_code": "9999", "error_msg": "Error Creating Cursor: " + str(err), "data": {}}

        columns = []
        sql = "SHOW COLUMNS FROM " + table_name
        try:
            cursor.execute(sql)
            columns = cursor.fetchall()
        except Exception as e:
            return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {}}

        sql = "select id from " + str(table_name) + " where 1 = 1 "
        # Make the rest of the where clause.
        for i in keys:
            for k in columns:
                if k['Field'] == i:
                    if 'int' in k['Type']:
                        sql += " and " + str(i) + " = " + my_dict[i] + " "
                    if 'varchar' in k['Type']:
                        sql += " and " + str(i) + " = '" + my_dict[i] + "' "
                    if 'date' in k['Type']:
                        sql += " and " + str(i) + " = '" + my_dict[i] + "' "

        # look for existing data
        cursor.execute(sql)
        existing = cursor.fetchall()

        id_list = []
        if len(existing) == 0:
            my_dict['id'] = ""
            id_list.append(self.post(my_dict))
        else:
            for l in existing:
                my_dict['id'] = l['id']
                my_dict['table_name'] = table_name
                my_dict['action'] = "insert"
                id_list.append(self.post(my_dict))

        return {"error_code": "0", "error_msg": "", "data": id_list}

    # Legacy post function.
    def post(self, my_dict):
        # id is required to be an autonumber primary key.
        # if it does not exist, is 0, or is "", this is a new record.
        try:
            if 'id' not in my_dict:
                my_id = 0
            else:
                my_id = my_dict['id']
        except Exception as e:
            return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {"id": "0"}}

        # action is a reserved word.  insert/delete
        try:
            if 'action' not in my_dict:
                my_action = "insert"
            else:
                my_action = my_dict['action']
        except Exception as e:
            return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {}}

        # table name is a reserved word.
        try:
            if 'table_name' not in my_dict:
                return {"error_code": "9000", "error_msg": "Table Name not in post dictionary", "data": {}}
            else:
                table_name = my_dict['table_name']
        except Exception as e:
            return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {}}

        try:
            conn = self.connect()
        except pymysql.err.MySQLError as err:
            return {"error_code": "9999", "error_msg": "Error Connecting: " + str(err), "data": {}}

        try:
            cursor = conn.cursor()
        except pymysql.err.MySQLError as err:
            return {"error_code": "9999", "error_msg": "Error Creating Cursor: " + str(err), "data": {}}

        # process insert and update
        if my_action == 'insert' or my_action == 'update':
            if my_id == 0 or my_id == '':
                sql = "insert into " + table_name + "(create_timestamp) values (now())"
                cursor.execute(sql)
                conn.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                m = cursor.fetchone()
                my_id = m['LAST_INSERT_ID()']

            # Get columns in the table.
            columns = []
            sql = "SHOW COLUMNS FROM " + table_name
            try:
                cursor.execute(sql)
                columns = cursor.fetchall()
            except Exception as e:
                return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {}}

            for key in my_dict:
                if key != 'table_name' and key != 'id' and key != 'action':
                    column_exists = False
                    for column in columns:
                        if column['Field'] == key:
                            column_exists = True

                    if column_exists:
                        cursor = conn.cursor()
                        sql = "update " + table_name + " set " + key + " = %s where id = %s"
                        v = (my_dict[key], my_id)
                        cursor.execute(sql, v)
                        conn.commit()
        if my_action == 'delete':
            try:
                sql = "delete from " + table_name + " where id = " + my_id
                cursor.execute(sql)
            except Exception as e:
                return {"error_code": "9999", "error_msg": "General Error: " + str(e), "data": {}}

        return {"error_code": "0", "error_msg": "", "data": {"id": str(my_id)}}
