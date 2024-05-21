import sqlite3
import inventory
from flask import Flask, render_template, request, jsonify

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
        print('post')
        name = request.form.get("fname")
        data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
 
        return render_template("edit.html", data=data)
        
    data = cursor.execute('SELECT * FROM item').fetchall()
    conn.close()
        
    return render_template("index.html", data=data)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")

    print(name)
    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
        
    conn.close()
        
    return render_template("edit.html", data=data)

@app.route("/ajax_edit", methods=["POST"])
def ajax_edit():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    new_name = request.form.get("new_name")
    
    print(name)
    inventory.update_name(conn, name, new_name)
    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
        
    conn.close()
        
    return render_template("edit.html", data=data)

if __name__ == "__main__":
    app.run(port = 5000)