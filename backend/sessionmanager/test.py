import sqlite3

dbname = 'db/test.db'
conn = sqlite3.connect(dbname)


cur = conn.cursor()
cur.execute(
    'CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT,token STRING)')

# データベースへコミット。これで変更が反映される。
conn.commit()

print(cur.fetchall())

conn.close()
