from flask import Flask
import os
import random
import time

import pyodbc
import pandas as pd
import redis as redis
from flask import Flask, render_template, request
import sqlite3 as sql

from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT','5000'))
myHostname = "flyingjaguar.redis.cache.windows.net"
myPassword = "3azkQQEBo5hhkEhjS7GrD+RF8AmdpJtsjWst5KxqEYY="
server = 'charan.database.windows.net'
database = 'MyDB'
username = 'charan123'
password = 'Smokescreen@5'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/options', methods=['POST', 'GET'])
def options():
    num = int(request.form['num'])
    rows = []
    get = []
    c = []
    points = []
    style = {'role':'style'}
    annotation = {'role':'annotation'}
    points.append(['Mag','Query Count',style,annotation])
    for i in range(num):
        val = round(random.uniform(2,5),1)
        cur = cnxn.cursor()
        cur.execute("select count(*) from all_month WHERE mag = ?",(val,))
        get = cur.fetchone();
        rows.append(get)
        count = rows[i][0]
        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
        points.append([val, count,color[0],count])
    return render_template("list1.html", rows=[c], p=points)



if __name__ == '__main__':
    app.run()

