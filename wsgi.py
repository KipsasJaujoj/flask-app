from flask import Flask
application = Flask(__name__)

@application.route("/")
def index():	
    templateData = {
        'mac': "44:55:66:77:88:99",
        'distance': 42.58,
        'time': "09:33"
    }
    return render_template('templates/index.html')

if __name__ == "__main__":
    application.run(debug=True)