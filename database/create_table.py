import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_tabel = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_tabel)

create_tabel = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price text)"
cursor.execute(create_tabel)

connection.commit()

cursor.close()