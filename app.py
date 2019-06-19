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
r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
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
    start_time = time.time()
    num = int(request.form['num'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Mag','Query Count'])
    for i in range(num):
        val = round(random.uniform(2,5),1)
        cur = cnxn.cursor()
        a = 'select * from all_month WHERE mag = '+str(val)
       #cur.execute("select * from all_month WHERE mag = ?" ,(val,))
        v = str(val)
        if r.get(a):
            print ('Cached')
            c.append('Cached')
            #print (r.get(a))
            rows.append(r.get(a))
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select count(*) from all_month WHERE mag = ?",(val,))
            get = cur.fetchone();
            rows.append(get)
            r.set(a,str(get))
        count = rows[i][0]
        #print (rows[0][0])
        points.append([val, count])

    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", rows=[c], etime=elapsed_time, p=points)

if __name__ == '__main__':
    app.run()

r.flushdb()
