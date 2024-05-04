import sqlite3

dbname = 'db/test.db'
conn = sqlite3.connect(dbname)

conn.close()
