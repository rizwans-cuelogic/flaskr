import os
import sqlite3

from flask import Flask,request,session,url_for,abort,render_template,flash,g,redirect

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(
	DATABASE = os.path.join(app.root_path,'flaskr.db'),
	SECRET_KEY = 'development key',
	USERNAME = 'admin',
	PASSWORD = 'admin123',
))

app.config.from_envvar('FLASKR_SETTINGS',silent=True)

def db_connect():
	rv= sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
	db = get_db()
	with app.open_resource('schema.sql',mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

def get_db():
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db = db_connect()
	return g.sqlite_db
	
@app.teardown_appcontext
def close_db(error):

	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()

@app.cli.command('initdb')

def initdb_command():
	init_db()
	print('initializes database')

@app.route('/')
def index():
	db = get_db()
	cur = db.execute('select title,text from entries order by id desc')
	entries= cur.fetchall()
	return render_template('show_entries.html',entries=entries)

@app.route('/add',methods=['POST'])
def add_entries():
	if not session.get('logged_in'):
		abort(401)

	db = get_db()
	db.execute('insert into entries(title,text) values (?,?)',
				[request.form['title'],request.form['text']]
		)
	db.commit()
	flash('New Entry is successfully posted')
	return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
	error= None
	if request.method =='POST':
		if request.form['username']	!= app.config['USERNAME']:
			error = 'Invalid Username'
		if request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Password'
		session['logged_in'] = True
		flash('you are loggged in ')
		return redirect(url_for('index'))

	return render_template('login.html',error=error)		

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('you are logged out')
	return redirect(url_for('index'))	

