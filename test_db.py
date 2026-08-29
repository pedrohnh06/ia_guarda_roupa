import sqlite3
try:
    conn = sqlite3.connect('backend/sql_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
except Exception as e:
    print('ERROR:', e)