import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute('''DELETE FROM IMAGES;''')
conn.execute('''DELETE FROM GROUPS;''')
conn.commit()
conn.execute('''VACUUM;''')
print("Table cleared successfully")

conn.close()