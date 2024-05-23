import sqlite3
import inventory
from datetime import date
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
        name = request.form.get("fname")
        data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
 
        return render_template("edit.html", data=data)
        
    data = cursor.execute('SELECT * FROM item').fetchall()
    conn.close()
        
    return render_template("index.html", data=data)

@app.route('/delete', methods=["GET", "POST"])
def delete():
    print('in delete')
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form["name"]
    
    #delete
    command = 'DELETE FROM item WHERE name = ?'
    cursor.execute(command, (name,))
    conn.commit()
    
    data = cursor.execute('SELECT * FROM item').fetchall()
    conn.close()
    
    return render_template("index.html", data=data)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        print('in add')
        conn = get_db_connection()
        cursor = conn.cursor()
        new_name = request.form.get("new_name")
        new_quant = request.form.get("new_quant")
        new_desc = request.form.get("new_desc")
        
        if new_name and new_quant and new_desc:
            command = 'INSERT INTO item VALUES (?, ?, ?, ?)'
            cursor.execute(command, (new_name, new_quant, new_desc, str(date.today())))
            conn.commit()
            data = cursor.execute('SELECT * FROM item').fetchall()
            conn.close()
            
            return render_template("index.html", data=data)

    
    
    return render_template("add.html")

@app.route('/edit', methods=["GET", "POST"])
def edit():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form["name"]

    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
    conn.close()
        
    return render_template("edit.html", data=data)

@app.route("/field_edit", methods=["POST"])
def field_edit():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    new_name = request.form.get("new_name")
    new_quant = request.form.get("new_quant")
    new_desc = request.form.get("new_desc")
    
    if new_name != "":
        command = 'UPDATE item SET name = ? WHERE name = ?;'
        cursor.execute(command, (new_name, name))
        conn.commit()
        name = new_name
    
    if new_quant != "":
        command = 'UPDATE item SET quantity = ? WHERE name = ?;'
        cursor.execute(command, (new_quant, name))
        conn.commit()
    
    if new_desc != "":
        command = 'UPDATE item SET description = ? WHERE name = ?;'
        cursor.execute(command, (new_desc, name))
        conn.commit()
    
    if new_name or new_quant or new_desc:
        command = 'UPDATE item SET date = ? WHERE name = ?;'
        cursor.execute(command, (str(date.today()), name))
        conn.commit()
    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
    conn.close()
    return render_template("edit.html", data=data)

@app.route("/sort", methods=["GET", "POST"])
def sort():
    conn = get_db_connection()
    cursor = conn.cursor()
    row = request.form.get("name")
    print(row)
    
    if row == '1':
        data = cursor.execute('SELECT * FROM item ORDER BY name').fetchall()
        conn.close()
        
    if row == '2':
        data = cursor.execute('SELECT * FROM item ORDER BY quantity DESC').fetchall()
        conn.close()
        
    if row == '3':
        data = cursor.execute('SELECT * FROM item ORDER BY description').fetchall()
        conn.close()
        
    if row == '4':
        data = cursor.execute('SELECT * FROM item ORDER BY date DESC').fetchall()
        conn.close()
        
    return render_template("index.html", data=data) 

@app.route("/sort_asc", methods=["GET", "POST"])
def sort_asc():
    conn = get_db_connection()
    cursor = conn.cursor()
    row = request.form.get("name")
    print(row)
    
    if row == '1':
        data = cursor.execute('SELECT * FROM item ORDER BY name ASC').fetchall()
        conn.close()
        
    if row == '2':
        data = cursor.execute('SELECT * FROM item ORDER BY quantity ASC').fetchall()
        conn.close()
        
    if row == '3':
        data = cursor.execute('SELECT * FROM item ORDER BY description ASC').fetchall()
        conn.close()
        
    if row == '4':
        data = cursor.execute('SELECT * FROM item ORDER BY date ASC').fetchall()
        conn.close()
        
    return render_template("index.html", data=data) 

@app.route("/sort_desc", methods=["GET", "POST"])
def sort_desc():
    conn = get_db_connection()
    cursor = conn.cursor()
    row = request.form.get("name")
    print(row)
    
    if row == '1':
        data = cursor.execute('SELECT * FROM item ORDER BY name DESC').fetchall()
        conn.close()
        
    if row == '2':
        data = cursor.execute('SELECT * FROM item ORDER BY quantity DESC').fetchall()
        conn.close()
        
    if row == '3':
        data = cursor.execute('SELECT * FROM item ORDER BY description DESC').fetchall()
        conn.close()
        
    if row == '4':
        data = cursor.execute('SELECT * FROM item ORDER BY date DESC').fetchall()
        conn.close()
        
    return render_template("index.html", data=data) 

if __name__ == "__main__":
    app.run(port = 5000)