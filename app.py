from flask import Flask, render_template, request
import os
import cx_Oracle

conn = cx_Oracle.connect(os.getenv('dbcred', 'dbms/dbms1234@localhost:1521'))
cursor = conn.cursor()

app = Flask(__name__)


@app.route('/')
def hello():
    assert request.method == 'GET'
    return render_template('index.html', name='VulnSequel')
