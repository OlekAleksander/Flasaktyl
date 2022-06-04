from flask import Flask, render_template, request, redirect, url_for, flash, session
import json

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/")
def index():
    logged = True
    if session == None:
        logged = False

    return render_template('index.html', logged = logged)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username in users:
            if check_password(password, users[username]['password']):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password","error")
        else:
            flash("User does not exist", "error")
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mail = request.form['mail']
        firstname = request.form['firstname']
        lastname = request.form['secondname']
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username in users:
            flash("User already exists")
            return redirect(url_for("register"))

        create_user(username, password,mail,firstname,lastname)
        flash("You were successfully registered", "success")
        return redirect(url_for("login"))
    return render_template('register.html')
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out","success")
    return redirect(url_for('login'))

def get_users():
    with open('users.json') as f:
        users = json.load(f)
    return users

def create_user(username, password,mail,firstname,lastname):
    users = get_users()
    password = hash_password(password)
    users[username] = {'password': password, 'mail': mail, 'firstname': firstname, 'lastname': lastname}
    with open('users.json', 'w') as f:
        json.dump(users, f)

def check_password(password, hashed_password):
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password

def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route("/dashboard")
def dashboard():
    x = session.get("username")
    if x == None:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user = session['username'])

if __name__ == "__main__":
    app.run(debug=True)