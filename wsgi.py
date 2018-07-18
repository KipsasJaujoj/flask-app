from flask import Flask
from flask import flash, render_template, request, redirect
import MySQLdb
application = Flask(__name__)

@application.route("/")
def index():	
    user = "remote-admin"
    passwd = "Some-pass!23"
    dbhost = "172.30.53.4"
    dbname = "smart-recycling-bins"
    db = MySQLdb.connect(host=dbhost, user=user, passwd=passwd, db=dbname)        
    cur = db.cursor()
    cur.execute("""SELECT * FROM `sensor_data` ORDER BY timestamp DESC LIMIT 1""")
    for (mac, data, timestamp) in cur:
	    templateData = {
        'mac': mac,
        'distance': data,
        'time': timestamp
		}
    cur.close()
    db.close()		
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    application.run(debug=True)