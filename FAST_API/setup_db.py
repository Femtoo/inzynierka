import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE IMAGES (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
TITLE VARCHAR(255),
[TYPE] VARCHAR(255),
[DESCRIPTION] VARCHAR(255),
[METADATA] VARCHAR(255),
[GROUPID] VARCHAR(255),
[GROUPNAME] VARCHAR(255),
[URL] VARCHAR(255)
)''')
conn.execute('''CREATE TABLE GROUPS (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
[GROUPID] VARCHAR(255),
[GROUPNAME] VARCHAR(255)
)''')
print("Table created successfully")

conn.close()