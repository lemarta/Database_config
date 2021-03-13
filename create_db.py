from psycopg2 import connect, OperationalError, errors

sql_create_database = "CREATE DATABASE db_workshop"

sql_users = """CREATE TABLE users (
id serial NOT NULL,
username varchar(255) NOT NULL,
hashed_password varchar(80) NOT NULL,
PRIMARY KEY(id)
);"""

sql_messages = """CREATE TABLE messages (
id serial NOT NULL,
PRIMARY KEY(id),
from_id int NOT NULL,
FOREIGN KEY(from_id) REFERENCES users(id),
to_id int NOT NULL,
FOREIGN KEY(to_id) REFERENCES users(id),
creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

try:
    cnx = connect(host='localhost', user='postgres', password='coderslab')
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(sql_create_database)
    print('Database created successfully')
except (OperationalError, errors.DuplicateDatabase):
    print('Error - database not created')
else:
    cursor.close()
    cnx.close()

for table in (sql_users, sql_messages):
    try:
        cnx = connect(host='localhost', user='postgres', password='coderslab', database='db_workshop')
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(table)
        print('Users table created successfully')
    except (OperationalError, errors.DuplicateTable):
        print('Error - table not created')
    else:
        cursor.close()
        cnx.close()



