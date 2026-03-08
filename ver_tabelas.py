import sqlite3

conn = sqlite3.connect("churn.db")

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tabelas = cursor.fetchall()