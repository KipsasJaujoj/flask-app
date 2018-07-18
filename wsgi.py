from flask import Flask
from flask import flash, render_template, request, redirect
import MySQLdb
import os
from datetime import datetime

application = Flask(__name__)

@application.route("/")
def index():	
    user = "remote-admin"
    passwd = "Some-pass!23"
    dbhost = os.environ["MYSQL_SERVICE_HOST"]
    dbname = "smart-recycling-bins"
    db = MySQLdb.connect(host=dbhost, user=user, passwd=passwd, db=dbname)        
    cur = db.cursor()
    cur.execute("""SELECT * FROM `sensor_data` ORDER BY timestamp DESC LIMIT 1""")
    for (id, mac_id, distance, datetime) in cur:
	    templateData = {
		'id': id,
        'mac': mac_id,
        'distance': distance,
        'time': datetime.strftime("%Y-%m-%d %H:%M:%S"),
		}
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    application.run(debug=True)