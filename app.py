from flask import Flask, render_template, request, url_for, redirect, session
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get('username') is None:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('profile.html', name='profile', user=session['username'])
    else:
        book = request.form.get('book')
        print(book)
        attrs = cursor.execute("SELECT * FROM BOOKS WHERE LOWER(BOOK_NAME) LIKE LOWER('%" + book + "%')").fetchall()
        if not attrs:
            flash('unable to find any book')
            return redirect(url_for('profile'))
        else:
            return render_template('profile.html', name='profile', user=session['username'], books=attrs)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if(request.method == 'POST'):
        session.pop('username', None)
        username = request.form.get('username')
        password = request.form.get('password')
        attrs = cursor.execute("SELECT * FROM USERS WHERE username='" + username + "' AND pass='" + password + "'").fetchone()
        if not attrs:
            flash('username or password is wrong')
            return redirect(url_for('home'))
        else:
            session['username'] = attrs[0]
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
