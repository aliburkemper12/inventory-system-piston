import sqlite3
import inventory
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    inventory.create_db()
    
    return conn

@app.route('/', methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form.get("fname")
        data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
 
        return render_template("index.html", data=data)
        

    data = cursor.execute('SELECT * FROM item').fetchall()
    conn.close()
    
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(port = 5000)