import sqlite3
import inventory
from flask import Flask, render_template, request, jsonify, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'roll_tide'

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
    name = request.form["name"]

    print(name)
    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
        
    conn.close()
        
    return render_template("edit.html", data=data)

@app.route("/ajax_edit_n", methods=["POST"])
def ajax_edit_n():
    data = {}
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    new_name = request.form.get("new_name")
    new_quant = request.form.get("new_quant")
    new_desc = request.form.get("new_desc")
    
    if new_name != "":
        print('doing new name:')
        command = 'UPDATE item SET name = ? WHERE name = ?;'
        cursor.execute(command, (new_name, name))
        conn.commit()
        name = new_name
    
    if new_quant != "":
        print('doing new quant:')
        command = 'UPDATE item SET quantity = ? WHERE name = ?;'
        cursor.execute(command, (new_quant, name))
        conn.commit()
    
    if new_desc != "":
        print('doing new desc:')
        command = 'UPDATE item SET description = ? WHERE name = ?;'
        cursor.execute(command, (new_desc, name))
        conn.commit()
    
    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
    conn.close()
    return render_template("edit.html", data=data)

if __name__ == "__main__":
    app.run(port = 5000)