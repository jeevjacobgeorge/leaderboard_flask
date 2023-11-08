from flask import Flask,render_template,request,session,redirect
from flask_session import Session

#configure app
app = Flask(__name__)

#configure session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

DETAILS = {"mufun@mulearn":"karmaisgood"}

#database code
import sqlite3
# Connect to or create a new SQLite database (e.g., mydb.db)
conn = sqlite3.connect('leaderboard.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table (e.g., 'mytable') with some sample columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS points_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        points INTEGER
    )
''')
# Commit the changes and close the database connection
conn.commit()
conn.close()

from cs50 import SQL
db = SQL("sqlite:///leaderboard.db")

#leaderboard page route is /
@app.route("/")
def index():
	table = db.execute("SELECT * FROM points_table ORDER BY points DESC")
	return render_template("leaderboard.html",rows=table,no=min(len(table),10))

#admin routes
@app.route("/mulogin", methods=["GET","POST"])
def mulogin():
		if request.method == "POST":
				session["Username"] = request.form.get("username_form")
				session["Password"] = request.form.get("password_form")
				return redirect("/muadmins")
		return render_template("login.html")

@app.route("/muadmins")
def muadmins():
	un = session.get("Username")
	pw = session.get("Password")
	if un in DETAILS and DETAILS[un] == pw:
		table = db.execute("SELECT * FROM points_table ORDER BY code")
		return render_template("dashboard.html",username=session.get("Username"),rows=table)
	else:
		#flash("Invalid Username or password",'error')
		return redirect("/mulogin")

@app.route("/add_class",methods=["POST"])
def add_class():
	code_form = request.form.get("class_code").upper()
	if code_form is not None:
		table = db.execute("SELECT * FROM points_table WHERE code= ?",code_form)
		if len(table) == 0:
			db.execute("INSERT INTO points_table(code,points) VALUES(?, 0)",code_form)
		return redirect("/muadmins")

@app.route("/add_points",methods=["POST"])
def add_points():
	code_form = request.form.get("class_code")
	points = int(request.form.get("points"))
	if 'dec' in request.form:
		points *= -1
	# codes_db = db.execute("SELECT code FROM points_table")
	if points is not None:  		#and code_form in codes_db
		db.execute("UPDATE points_table SET points = points + ? WHERE code = ?",points,code_form)
	return redirect("/muadmins")

@app.route("/logout")
def logout():	
	session["Username"] = None
	session["Password"] = None
	return redirect("/mulogin")















