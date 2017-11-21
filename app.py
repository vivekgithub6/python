import os
import psycopg2
from flask import Flask, render_template
import urlparse
from os.path import exists
from os import makedirs
import logging
from logging.handlers import RotatingFileHandler
from flask import request

cur = None
if os.environ.get('DATABASE_URL') == None:
    print("Warning:'DATABASE_URL' not set")
else:
	urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
	
cur = conn.cursor()
app = Flask(__name__)

@app.route('/')
def hello():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return 'Hello World!'

@app.route('/Accounts')
def Accounts():
    try:
        my_list = []
        if cur != None:
            cur.execute("""SELECT name from salesforceaccounts.Account""")
            rows = cur.fetchall()
            response = ''
            
            for row in rows:
                my_list.append(row[0])

        return render_template('template.html',  results=my_list)
    except Exception as e:
        print ("e")
        return []

    
if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()

	
