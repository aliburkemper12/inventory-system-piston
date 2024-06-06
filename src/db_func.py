# different page for each item
# home screen where you can add or delete item categories
import sqlite3
from datetime import date

def create_db():
    global conn, cursor
    dbName = 'inventory.db'

    try:
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()

    except Exception as e:
        print("Something bad happened: ", e)
        if conn:
            conn.close()

    create_query = '''CREATE TABLE IF NOT EXISTS item(
    name TEXT NOT NULL PRIMARY KEY,
    quantity INTEGER,
    description TEXT,
    date TEXT NOT NULL
    );
    '''
    
    cursor.execute(create_query)
    
def insert_command(conn, name, quantity, description):
  command = 'INSERT INTO item VALUES (?, ?, ?, ?)'
  cur = conn.cursor()
  cur.execute(command, (name, quantity, description, str(date.today())))
  conn.commit()
  
def update_time(conn, name):
    command = 'UPDATE item SET date = ? WHERE name = ?;'
    cursor.execute(command, (str(date.today()), name))
    conn.commit()

def find(conn, name):
    records = cursor.execute('SELECT * FROM item WHERE name = ?', (name,))
    for row in records:
        print(row)

def update_quantity(conn, quantity, name):
    command = 'UPDATE item SET quantity = ? WHERE name = ?;'
    cursor.execute(command, (quantity, name))
    conn.commit()
    print_items()

def update_name(conn, name, new_name):
    command = 'UPDATE item SET name = ? WHERE name = ?;'
    cursor.execute(command, (new_name, name))
    conn.commit()
    print_items()
    
def update_description(conn, name, description):
    command = 'UPDATE item SET description = ? WHERE name = ?;'
    cursor.execute(command, (description, name))
    conn.commit()
    print_items()

def delete_item(conn, name):
    command = 'DELETE FROM item WHERE name = ?'
    cursor.execute(command, (name,))
    conn.commit()
    print_items()

def print_items():
    records = cursor.execute("SELECT * FROM item")
    for row in records:
        print(row)