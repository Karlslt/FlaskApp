#from flask import Flask
#from flask import Flask, render_template
#from flask import Flask, render_template, request
from flask import Flask, render_template, json, request, flash, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/\?RT'
mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'karltang'
app.config['MYSQL_DATABASE_PASSWORD'] = 'willingK'
app.config['MYSQL_DATABASE_DB'] = 'bucket_list'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
	return render_template('index.html')
	
@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp', methods=['POST','GET'])
def signUp():		
	try:
		# read the posted values from the UI
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		
		if _name in session:
			abort(401)
			
		# validate the received values
		if _name and _email and _password:
			conn = mysql.connect()
			cursor = conn.cursor()
			#_hashed_password = generate_password_hash(_password)
			#cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
			cursor.callproc('sp_createUser', (_name, _email, _password))
			data = cursor.fetchall()
			
			if len(data) is 0:
				conn.commit()
				flash('User created successfully !')
				session['username'] = _name
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
			return json.dumps({'html':'<span>All fields good !!</span>'})
		else:
			return json.dumps({'html':'<span>Enter the required fields !!</span>'})
	finally:
		#session.pop('username', None)
		cursor.close()
		conn.close()
		
if __name__ == '__main__':
	app.run()