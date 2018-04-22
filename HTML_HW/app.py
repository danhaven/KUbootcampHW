from flask import Flask, request, send_from_directory
app = Flask(__name__)

@app.route("/index.html")
def home():
    return send_from_directory('', 'index.html')

@app.route("/maxtemp.html")
def Maxtemp():
    return send_from_directory('', 'maxtemp.html')

@app.route("/data.html")
def Data():
    return send_from_directory('', 'data.html')

@app.route("/cloudiness.html")
def Cloudiness():
    return send_from_directory('', 'cloudiness.html')

@app.route("/humidity.html")
def Humidity():
    return send_from_directory('', 'humidity.html')

@app.route("/comparison.html")
def Comparison():
    return send_from_directory('', 'comparison.html')

@app.route("/windspeed.html")
def Windspeed():
    return send_from_directory('windspeed.png', 'windspeed.html')

if __name__ == "__main__":
  app.run(debug=True)
