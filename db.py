from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///students.db")

def fetch_data(query):
    return pd.read_sql(query, engine)

import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class INTEGER,
    marks INTEGER
)
""")

cursor.executemany("""
INSERT INTO students (name, class, marks)
VALUES (?, ?, ?)
""", [
    ("Rahul", 10, 85),
    ("Anita", 10, 92),
    ("Aman", 9, 70),
    ("Priya", 10, 78)
])

conn.commit()
conn.close()



