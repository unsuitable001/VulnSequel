from flask import Flask, render_template, request, url_for, redirect
import os
import cx_Oracle

from flask.helpers import flash 
conn = cx_Oracle.connect(os.getenv('dbcred', 'dbms/dbms1234@localhost:1521'))
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    assert request.method == 'GET'
    return render_template('index.html', name='VulnSequel')

@app.route('/profile')
def profile():
    assert request.method == 'GET'
    return 'Hello Admin'

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        rows = cursor.execute("SELECT * FROM USERS WHERE username='" + username + "' AND pass='" + password + "'").fetchone()
        if not rows:
            flash('username or password is wrong')
            return redirect(url_for('home'))
        else:
            for row in rows:
                print(row)
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('home'))
