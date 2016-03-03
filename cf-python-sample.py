__author__ = '212391398'

from flask import Flask
import os
import json
import psycopg2

app = Flask(__name__)

port = None
vcap = None
jdbc_uri = None
database_name = None
username = None
password_str = None
db_host = None
db_port = None
connected = False
conn = None
cur = None

### Application Configuration
portStr = os.getenv("VCAP_APP_PORT")

if portStr is not None:
    port = int(portStr)

services = os.getenv("VCAP_SERVICES")

if services is not None:
    vcap = json.loads(services)

if vcap is not None:
    postgres = vcap['postgres'][0]['credentials']
    if postgres is not None:
        jdbc_uri = postgres['jdbc_uri']
        database_name = postgres['database']
        username = postgres['username']
        password_str = postgres['password']
        db_host = postgres['host']
        db_port = postgres['port']
else:
    database_name = '<DATABASE_NAME>'
    username = '<USERNAME>'
    password_str = '<PASSWORD>'
    db_host = 'localhost'
    db_port = 5432

try:
    conn = psycopg2.connect(database=database_name, user=username, password=password_str, host=db_host, port=db_port)
    connected = True
    cur = conn.cursor()
except:
    connected = False

### APIs

### users api - GET - retrieve users
@app.route('/users', methods=['GET'])
def get_forecasts():
    response = ''
    query = 'SELECT * FROM sample.users'
    if cur is not None:
        cur.execute(query)
        conn.commit()
        rows = cur.fetchall()
        response = json.dumps(rows)
    return response

### Main api - GET - provides connection info
@app.route('/')
def main():
    response = '<h1>Database Connection Info</h1><hr>'

    if jdbc_uri is not None:
        response += '<b>jdbc_uri:</b> ' + jdbc_uri + "<BR>"

    if database_name is not None:
        response += '<b>database:</b> ' + database_name + "<BR>"

    if username is not None:
        response += '<b>username:</b> ' + username + "<BR>"

    if password_str is not None:
        response += '<b>password:</b> ' + password_str + "<BR>"

    if db_host is not None:
        response += '<b>host:</b> ' + db_host + "<BR>"

    if db_port is not None:
        response += '<b>port:</b> ' + str(db_port) + "<BR>"

    response += '<hr>'

    if connected is True:
        response += '<font color="#00FF00"><b>Database connection is active</b></font>'
    else:
        response += '<font color="#FF0000"><b>Database is not connected</b></font>'

    return response

### Main application
if __name__ == '__main__':
    if port is not None:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()