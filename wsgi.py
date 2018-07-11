from flask import Flask
application = Flask(__name__)

@application.route("/")
def index():	
#	time, temp, hum = getData()
	templateData = {
		'mac': "44:55:66:77:88:99",
		'distance': 42.58,
		'time': "09:33"
	}
	return render_template('index.html', **templateData)
	
if __name__ == "__main__":
    application.run()
