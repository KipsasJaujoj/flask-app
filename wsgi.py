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
    cur.execute("""SELECT * FROM `sensor_data` ORDER BY timestamp DESC LIMIT 100""")
    time_list = []
    data_json = {}
    for (id, mac_id, distance, datetime) in cur:
        date_time = datetime.strftime("%Y-%m-%d %H:%M:%S")
        templateData = {
        'id': id,
        'mac': mac_id,
        'distance': distance,
        'time': date_time
        }
        data_json['id'] = {}
        data_json['id']['data'] = {}
        data_json['id']['data']['id'] = id
        data_json['id']['data']['mac_id'] = mac_id
        data_json['id']['data']['distance'] = distance
        data_json['id']['data']['time'] = date_time
        if not date_time in time_list:
            time_list.append(date_time)    
    templateData['dataset'] = cur.fetchall()
    test_device = templateData['dataset'][0][1]
    templateData['test_device'] = test_device
    templateData['time_list'] = sorted(time_list)
    values = []
    for j in templateData['time_list']:
        for i in data_json:
            if data_json[i]['data']['mac_id'] == test_device:
                if j == data_json[i]['data']['time']:
                    values.append(data_json[i]['data']['distance'])
                    break
    templateData['distances'] = values
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    application.run(debug=True)