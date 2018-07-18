from flask import Flask
from flask import flash, render_template, request, redirect
application = Flask(__name__)

@application.route("/")
def index():	
    templateData = {
        'mac': "44:55:66:77:88:99",
        'distance': 42.58,
        'time': "09:33"
    }
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    application.run(debug=True)