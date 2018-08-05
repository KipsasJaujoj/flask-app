from flask import Flask
from flask import flash, render_template, request, redirect
import MySQLdb
import os
from datetime import datetime
from collections import OrderedDict

application = Flask(__name__)
config = { "floors": {4: { "ec:fa:bc:e:a6:95_1": "general" , "ec:fa:bc:e:a6:95_2": "general", "ec:fa:bc:e:a6:95_3": "glass", "ec:fa:bc:e:a6:95_4": "paper" }},
           "colors": [ "#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#dd4c25", "#cebf1a", "#67d117", "#09bc2d", "#0fc1aa", "#1111c4", "#7f0fc4", "#c90e7e" ]
         }

@application.route("/")
def index():	
    user = "remote-admin"
    passwd = "Some-pass!23"
    dbhost = os.environ["MYSQL_SERVICE_HOST"]
    dbname = "smart-recycling-bins"
    db = MySQLdb.connect(host=dbhost, user=user, passwd=passwd, db=dbname)        
    cur = db.cursor()
    cur.execute("""SELECT * FROM `sensor_data` ORDER BY timestamp DESC LIMIT 200""")
    data = cur.fetchall()
    parsed_data = OrderedDict()
    for (id, mac_id, distance, datetime_object) in data:
        date_time = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        if date_time in parsed_data:
            parsed_data[date_time].update({ mac_id: { "distance": distance }})
        else:
            parsed_data.update({ date_time: { mac_id: { "distance": distance }}})
    filtered_data = OrderedDict()
    for i in parsed_data:
        if len(parsed_data[i]) == 4:
            filtered_data.update({i: parsed_data[i]})
    templateData = {}
    templateData['distance_data'] = OrderedDict(sorted(filtered_data.items()))
    templateData['config'] = config
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    application.run(debug=True)