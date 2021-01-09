import os
import re
from datetime import datetime
from os import listdir

import mysql.connector
from mysql.connector import Error

import Globals

SQL_PATH = r'C:\Projects\Workspace\Web\JT database - local'


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print(f"{Globals.Font.LIGHT_GREEN}MySQL Database connection successful{Globals.Font.END}")
    except Error as err:
        print(f"{Globals.Font.RED}Error: '{err}'{Globals.Font.END}")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print(f"{Globals.Font.LIGHT_GREEN}Database created successfully{Globals.Font.END}")
    except Error as err:
        print(f"{Globals.Font.RED}Error: '{err}'{Globals.Font.END}")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            connection_timeout=30
        )
        print(f"{Globals.Font.LIGHT_GREEN}MySQL Database connection successful{Globals.Font.END}")
    except Error as err:
        print(f"{Globals.Font.RED}Error: '{err}'{Globals.Font.END}")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    print("Query: " + (query[:100] if len(query) > 100 else query + ' '*(100-len(query))), end='')
    try:
        start_time = datetime.now()
        for result in cursor.execute(query, multi=True):
            #print(f"Cursor result: {result}")
            pass
        # result = cursor.execute(query, multi=True)
        # result.send(None)
        connection.commit()
        elapsed_time = datetime.now() - start_time
        print(f" - {Globals.Font.LIGHT_GREEN}Query successful, time: {elapsed_time}{Globals.Font.END}")
    except Error as err:
        print(f" - {Globals.Font.RED}Error: '{err}'{Globals.Font.END}")


pw = "ba21181476"
db = "japagram_wp27a"
connection = create_server_connection("localhost", "root", pw)
create_database(connection, f"CREATE DATABASE {db}")
connection = create_db_connection("localhost", "root", pw, db)

max_packet_size = 50*1024*1024  # 5MB
execute_query(connection, f"SET GLOBAL max_allowed_packet={max_packet_size}")

# content = Globals.get_file_contents(f'{SQL_PATH}\\jt_ExtendedDbFrenchIndex.txt').replace('\n', '')
# execute_query(connection, content)

sqlFiles = [f for f in listdir(SQL_PATH) if os.path.isfile(os.path.join(SQL_PATH, f)) and 'jt_' in f]
for sqlFile in sqlFiles:
    content = Globals.get_file_contents(f'{SQL_PATH}\\{sqlFile}').replace('\n', '')
    execute_query(connection, content)
    if '-PART0.txt' in sqlFile or not re.search(r'-PART\d+\.txt', sqlFile):
        table = re.sub(r'(|-PART\d+)\.txt', '', sqlFile)
        execute_query(connection, f"ALTER TABLE `{table}` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci")

execute_query(connection, "SHOW TABLES")
