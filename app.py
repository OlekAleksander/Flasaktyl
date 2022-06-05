# Imports
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import configmanager
from pydactyl import PterodactylClient
import requests
from colorama import init, Fore, Back, Style

# Pterodactyl API
panel_domain = configmanager.get_config()["api"]['panel_domain']
key = configmanager.get_config()["api"]['key']
api = PterodactylClient(panel_domain, key)

# Global variables
debug = configmanager.get_config()["app"]['debug']

# Flask config
app = Flask(__name__)
app.secret_key = 'secret'

# Disable flasks logs
flask_logs = configmanager.get_config()["app"]["flask_logs"]
if not flask_logs:    
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    from flask import cli
    cli.show_server_banner = lambda *_: None

# Index route
@app.route("/")
def index():
    logged = True
    if session == None:
        logged = False

    return render_template('index.html', logged = logged, gamepanel = panel_domain)

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        # Check if user entered every field
        if username == "" or password == "":
            flash("Please fill in all fields", "danger")
            return redirect(url_for('login'))
        # Check if user exists
        if username in users:
            if check_password(password, users[username]['password']):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password","danger")
        else:
            flash("User does not exist", "danger")
    return render_template('login.html')

# Register route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if configmanager.get_config()["auth"]['register'] == False:
            flash("Registration is disabled!", "danger")
            return redirect(url_for('register'))

        # get every value from the registration form
        mail = request.form['mail']
        firstname = request.form['firstname']
        lastname = request.form['secondname']
        username = request.form['username']
        password = request.form['password']
        # create account in pterodactyl


        users = get_users()
        # Check if user entered every field
        if username == "" or password == "":
            flash("Please fill in all fields", "danger")
            return redirect(url_for('register'))
        # check if the user already exists
        if username in users:
            flash("User already exists", "danger")
            return redirect(url_for("register"))
        
        # check if the mail is already in use
        if mail in users:
            flash("Mail already in use", "danger")
            return redirect(url_for("register"))

        # check if password is long enough
        if len(password) < 8:
            flash("Password is too short", "danger")
            return redirect(url_for("register"))

        # create user
        create_user(username, password,mail,firstname,lastname)
        try:
            api.user.create_user(username,mail, firstname, lastname,None, password)
        except:
            flash("Could not create user", "danger")
            print(Back.RED + "[ ERROR ] -> Could create pterodactyl user for " + username + Style.RESET_ALL)
            return redirect(url_for("register"))
        flash("You were successfully registered", "success")
        return redirect(url_for("login"))
    return render_template('register.html')

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out","success")
    return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    x = session.get("username")
    if x == None:
        return redirect(url_for('login'))
    ram = float(get_user_ram(x))
    cpu = float(get_user_cpu(x))
    disk = float(get_user_disk(x))
    coins = float(get_user_coins(x))
    usedram = 0.25
    usedcpu = 0.75
    useddisk = 3
    # calculate ram usage
    ram_usage = percentage(usedram,ram)
    cpu_usage = percentage(usedcpu,cpu)
    disk_usage = percentage(useddisk,disk)
    return render_template('dashboard.html', user = session['username'],ram=str(ram),cpu=str(cpu),disk=str(disk),coins=str(coins),ramval=str(ram_usage),cpuval=str(cpu_usage),diskval=str(disk_usage),useddisk=useddisk,usedcpu=usedcpu,usedram=usedram)

# Functions
def percentage(part, whole):
  return int(100 * float(part)/float(whole))

def get_user_info(username):
    users = get_users()
    return users[username]

def get_user_coins(username):
    users = get_users()
    return users[username]['coins']

def get_user_ram(username):
    users = get_users()
    return users[username]['ram']

def get_user_cpu(username):
    users = get_users()
    return users[username]['cpu']

def get_user_disk(username):
    users = get_users()
    return users[username]['disk']


def get_users():
    with open('users.json') as f:
        users = json.load(f)
    return users

def create_user(username, password,mail,firstname,lastname):
    users = get_users()
    password = hash_password(password) 
    # Get default coins and resources
    default_coins = configmanager.get_config()["users"]["default"]["coins"]
    default_cpu = configmanager.get_config()["users"]["default"]["cpu"]
    default_disk = configmanager.get_config()["users"]["default"]["disk"]
    default_ram = configmanager.get_config()["users"]["default"]["ram"]
    users[username] = {'password': password, 'mail': mail, 'firstname': firstname, 'lastname': lastname, "coins": default_coins, "cpu": default_cpu, "disk": default_disk, "ram": default_ram}
    with open('users.json', 'w') as f:
        json.dump(users, f)

def check_password(password, hashed_password):
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password

def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Run the app
port = configmanager.get_config()["app"]['port']
flask_logs = configmanager.get_config()["app"]["flask_logs"]
if __name__ == "__main__":
    try:
        resp = "0.3"
    except:
        print(Back.RED + "[ ERROR ] -> Could not get the latest version" + Style.RESET_ALL)
    if resp == "0.3":
        print(Fore.GREEN + "[ OK ] -> Version is up to date" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[ INFO ] -> Version is outdated" + Style.RESET_ALL)
    print(Fore.BLUE + "[ INFO ] -> Flasaktyl is online at port " + str(port) + Style.RESET_ALL)
    app.run(debug=debug, host='0.0.0.0', port=port)
    
