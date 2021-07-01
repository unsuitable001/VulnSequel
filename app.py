import os
import random
import string

import cx_Oracle
from flask import Flask, redirect, render_template, request, session, url_for
from flask.helpers import flash

conn = cx_Oracle.connect(os.getenv('dbcred', 'dbms/dbms1234@localhost:1521'))
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    assert request.method == 'GET'
    res = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase +
                             string.digits, k = 6))
    cursor.execute(f"UPDATE USERS SET PASS = '{res}' WHERE username='webadmin'")
    conn.commit()
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
        attrs = cursor.execute(f"SELECT * FROM BOOKS WHERE LOWER(BOOK_NAME) LIKE LOWER('%{book}%')").fetchall()
        if not attrs:
            flash('unable to find any book')
            return redirect(url_for('profile'))
        else:
            return render_template('profile.html', name='profile', user=session['username'], books=attrs)

@app.route('/secure/profile', methods=['GET', 'POST'])
def secureProfile():
    if session.get('username') is None:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('profile.html', name='profile', user=session['username'])
    else:
        book = request.form.get('book')
        print(book)
        attrs = cursor.execute("""
        SELECT * FROM BOOKS WHERE LOWER(BOOK_NAME) LIKE LOWER('%' || :bookname || '%')
        """, bookname = book).fetchall()
        if not attrs:
            flash('unable to find any book')
            return redirect(url_for('secureProfile'))
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
