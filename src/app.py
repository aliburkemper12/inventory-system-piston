import sqlite3
import db_func
from datetime import date
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xf9\xf6\xdc\x82P\x7f\xc4X\x07\xb8\xc0\x01'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
        
# db.init_app(app)
with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def load_user(user_id):  
    return User.query.get(int(user_id))

def authenticate_user(username, password):
    # see if username and password are correct
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    elif check_password_hash(user.password, password):
        return user
    else:
        return None
    
def admin_required(func):
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or 'admin' not in [role.name for role in current_user.roles]:
            return "You don't have permission to access this page."
        return func(*args, **kwargs)
    return decorated_view

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    db_func.create_db()
    
    return conn

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user_id = authenticate_user(username, password)
        if user_id:
            login_user(user_id)
            return redirect(url_for("home"))
        else:
            flash('Invalid username or password')
                
    return render_template("login.html", error="")

@app.route('/new_user', methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        username = request.form.get("new_name")
        password = request.form.get("new_pass")
        password1 = request.form.get("new_pass_two")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
        elif password1 != password:
            flash("Passwords don't match.")
        else:
            hashed_pass = generate_password_hash(password)
            print(hashed_pass)
            new_user = User(username=username, password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.')
            return redirect(url_for('login'))
        
    return render_template("new.html")

@app.route('/admin')
@login_required
@admin_required
def admin():
    data = User.query.all()
    
    return render_template("admin.html", data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(''))

@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        name = request.form.get("fname")
        data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
        print(data)
 
        if len(data) != 0:
            return render_template("edit.html", data=data)
        else:
            data = cursor.execute('SELECT * FROM item WHERE name LIKE ?', ('%' + name + '%',)).fetchall()
    
            return render_template("index.html", data=data)      
        
    data = cursor.execute('SELECT * FROM item').fetchall()
    conn.close()
        
    return render_template("index.html", data=data)

@app.route('/full', methods=["GET", "POST"])
@login_required
def full():
    return redirect("/home")

@app.route('/partial', methods=["GET", "POST"])
@login_required
def partial():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    data = cursor.execute('SELECT name, quantity, alert FROM item').fetchall()
    
    return render_template("small.html", data=data)

@app.route('/checkout', methods=["GET", "POST"])
@login_required
def checkout():
    
    return render_template("index.html")
        
@app.route('/location', methods=["GET", "POST"])
@login_required
def location():
    conn = get_db_connection()
    cursor = conn.cursor()
    location = request.form.get("flocation")
    print(location)
        
    data = cursor.execute('SELECT * FROM item WHERE location = ?', (location,)).fetchall()
    conn.close()

        
    return render_template("sub.html", data=data)
    
@app.route('/user', methods=["GET", "POST"])
@login_required
def user():
    if request.method == "POST":
        username = request.form.get("new_name")
        print(username)
        password = request.form.get("new_pass")
        user = User.query.filter_by(username=current_user.username).first()
        
        #UPDATE USERNAME
        if username:
            user.username = username
            db.session.commit()
            flash('Username updated')
            
        #UPDATE PASSWORD
        if password:
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Password updated')
            
        
    return render_template("user.html")

@app.route('/delete', methods=["GET", "POST"])
@login_required
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

@app.route('/delete_user', methods=["GET", "POST"])
@login_required
def delete_user():
    name = request.form["name"]
    
    #delete
    User.query.filter_by(username=name).delete()
    db.session.commit()
    

    data = User.query.all()
    return render_template("admin.html", data=data)

@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()
        new_name = request.form.get("new_name")
        new_quant = request.form.get("new_quant")
        new_desc = request.form.get("new_desc")
        new_location = request.form.get("new_location")
        new_alert = request.form.get("new_alert")
        print(new_alert)
        
        if new_name and new_quant and new_desc and new_location:
            if new_alert:
                print('new alert')
                command = 'INSERT INTO item VALUES (?, ?, ?, ?, ?, ?)'
                cursor.execute(command, (new_name, new_quant, new_desc, str(date.today()), new_location, new_alert))
                conn.commit()
            else:
                command = 'INSERT INTO item VALUES (?, ?, ?, ?, ?, ?)'
                cursor.execute(command, (new_name, new_quant, new_desc, str(date.today()), new_location, 'None'))
                conn.commit()
                
            data = cursor.execute('SELECT * FROM item').fetchall()
            conn.close()
            
            flash('Database updated')
            return render_template("add.html", error="")
        
        else:
            return render_template("add.html", error="Invalid. Please try again.")
    
    
    return render_template("add.html", error="")

@app.route('/edit', methods=["GET", "POST"])
@login_required
def edit():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form["name"]

    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
    conn.close()
        
    return render_template("edit.html", data=data)

@app.route('/update_q', methods=["POST", "GET"])
@login_required
def update_q():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    q = request.form.get("d_q")
    
    if q != "":
        command = 'UPDATE item SET quantity = ? WHERE name = ?;'
        cursor.execute(command, (q, name))
        
        command = 'UPDATE item SET date = ? WHERE name = ?;'
        cursor.execute(command, (str(date.today()), name))
        conn.commit()
        
    data = cursor.execute('SELECT * FROM item').fetchall()
    conn.close()
    
    return render_template("index.html", data=data)

@app.route('/update_q_p', methods=["POST", "GET"])
@login_required
def update_q_p():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    q = request.form.get("d_q")
    
    if q != "":
        command = 'UPDATE item SET quantity = ? WHERE name = ?;'
        cursor.execute(command, (q, name))
        
        command = 'UPDATE item SET date = ? WHERE name = ?;'
        cursor.execute(command, (str(date.today()), name))
        conn.commit()
        
    data = cursor.execute('SELECT name, quantity FROM item').fetchall()
    conn.close()
    
    return render_template("small.html", data=data)

@app.route('/update_q_sub', methods=["POST", "GET"])
@login_required
def update_q_sub():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    q = request.form.get("d_q")
    location = request.form.get("flocation")
    
    if q != "":
        command = 'UPDATE item SET quantity = ? WHERE name = ?;'
        cursor.execute(command, (q, name))
        
        command = 'UPDATE item SET date = ? WHERE name = ?;'
        cursor.execute(command, (str(date.today()), name))
        conn.commit()

    data = cursor.execute('SELECT * FROM item WHERE location = ?', (location,)).fetchall()
    conn.close()
    
    return render_template("sub.html", data=data)

@app.route("/field_edit", methods=["POST"])
@login_required
def field_edit():
    conn = get_db_connection()
    cursor = conn.cursor()
    name = request.form.get("name")
    new_name = request.form.get("new_name")
    new_quant = request.form.get("new_quant")
    new_desc = request.form.get("new_desc")
    new_location = request.form.get("new_location")
    new_alert = request.form.get("new_alert")
    
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
        
    if new_location != "":
        command = 'UPDATE item SET location = ? WHERE name = ?;'
        cursor.execute(command, (new_location, name))
        conn.commit()
        
    if new_alert != "":
        command = 'UPDATE item SET alert = ? WHERE name = ?;'
        cursor.execute(command, (new_alert, name))
        conn.commit()
    
    if new_name or new_quant or new_desc or new_location or new_alert:
        command = 'UPDATE item SET date = ? WHERE name = ?;'
        cursor.execute(command, (str(date.today()), name))
        conn.commit()
    data = cursor.execute('SELECT * FROM item WHERE name = ?', (name,)).fetchall()
    conn.close()
    return render_template("edit.html", data=data)    

@app.route("/sort_asc", methods=["GET", "POST"])
@login_required
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
        
    if row == '5':
        data = cursor.execute('SELECT * FROM item ORDER BY location ASC').fetchall()
        conn.close()
        
    return render_template("index.html", data=data) 

@app.route("/sort_desc", methods=["GET", "POST"])
@login_required
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
        
    if row == '5':
        data = cursor.execute('SELECT * FROM item ORDER BY location DESC').fetchall()
        conn.close()
        
    return render_template("index.html", data=data)

@app.route("/sort_asc_sub", methods=["GET", "POST"])
@login_required
def sort_asc_sub():
    conn = get_db_connection()
    cursor = conn.cursor()
    row = request.form.get("name")
    location = request.form.get("flocation")
    print(location)
    print(row)
    
    if row == '1':
        data = cursor.execute('SELECT * FROM item ORDER BY name ASC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    if row == '2':
        data = cursor.execute('SELECT * FROM item ORDER BY quantity ASC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    if row == '3':
        data = cursor.execute('SELECT * FROM item ORDER BY description ASC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    if row == '4':
        data = cursor.execute('SELECT * FROM item ORDER BY date ASC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    # return render_template("sub.html", data=data) 
    return jsonify(data=data)

@app.route("/sort_desc_sub", methods=["GET", "POST"])
@login_required
def sort_desc_sub():
    conn = get_db_connection()
    cursor = conn.cursor()
    row = request.form.get("name")
    location = request.form.get("location")
    print(row)
    
    if row == '1':
        data = cursor.execute('SELECT * FROM item ORDER BY name DESC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    if row == '2':
        data = cursor.execute('SELECT * FROM item ORDER BY quantity DESC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    if row == '3':
        data = cursor.execute('SELECT * FROM item ORDER BY description DESC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    if row == '4':
        data = cursor.execute('SELECT * FROM item ORDER BY date DESC WHERE location = ?', (location,)).fetchall()
        conn.close()
        
    return render_template("sub.html", data=data) 

if __name__ == "__main__":
    app.run(port = 5000)