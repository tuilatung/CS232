import sqlite3
from pathlib import Path
import pandas as pd


# Step 1: using touch() to create database file
Path('dblp.db').touch()

# Step 2: connect to database file
connector = sqlite3.connect('dblp.db')
c = connector.cursor()

# Step 3: run script to create table and some fields
# c.execute('''CREATE TABLE DATA (
#             author text,
#             dblpkey text,
#             tag text,
#             title text,
#             mdate text,
#             booktitle text,
#             year int,
#             journal text,
#             ee text,
#             url text
# )''')

data = pd.read_csv('./parsed_data.csv', on_bad_lines='skip')
data.to_sql('MyTable', connector, if_exists='append', index=False)
