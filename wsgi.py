from flask import Flask
from flask import flash, render_template, request, redirect
import MySQLdb
import os
from datetime import datetime
from collections import OrderedDict
import sys

application = Flask(__name__)

@application.route("/")
def index():	
    user = "remote-admin"
    passwd = "Some-pass!23"
    dbhost = os.environ["MYSQL_SERVICE_HOST"]
    dbname = "smart-recycling-bins"
    db = MySQLdb.connect(host=dbhost, user=user, passwd=passwd, db=dbname)        
    cur = db.cursor()
    cur.execute("""SELECT * FROM `sensor_data` ORDER BY timestamp DESC LIMIT 100""")
    data = cur.fetchall()
    parsed_data = OrderedDict()
    for (id, mac_id, distance, datetime_object) in data:
        date_time = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        if date_time in parsed_data:
            parsed_data[date_time].update({ mac_id: { "distance": distance }})
        else:
            parsed_data.update({ date_time: { mac_id: { "distance": distance }}})
    for i in parsed_data:
        if len(parsed_data[i]) < 4:
            parsed_data.pop(i)
    templateData = {}
    templateData['distance_data'] = OrderedDict(sorted(parsed_data.items()))
    templateData['version'] = sys.version
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    application.run(debug=True)