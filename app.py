from flask import Flask, render_template, jsonify
import geocoder
from geopy.distance import distance

app = Flask(__name__)

# Sample hospital data (replace with actual hospital data)
hospitals = [
    {"name": "Hospital A", "latitude": 40.73061, "longitude": -73.935242},
    {"name": "Hospital B", "latitude": 40.748817, "longitude": -73.985428},
    {"name": "Hospital C", "latitude": 40.707851, "longitude": -74.003002}
    # Add more hospitals with latitude and longitude
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_hospital', methods=['POST'])
def find_hospital():
    # Get user's location based on IP address using geocoder
    user_location = geocoder.ip('me').latlng
    user_lat, user_lon = user_location

    # Calculate distances to all hospitals
    distances = []
    for hospital in hospitals:
        hosp_lat, hosp_lon = hospital["latitude"], hospital["longitude"]
        dist = distance((user_lat, user_lon), (hosp_lat, hosp_lon)).km
        distances.append((hospital["name"], dist))

    # Sort distances to find the nearest hospital
    distances.sort(key=lambda x: x[1])
    nearest_hospital = {"name": distances[0][0], "distance": distances[0][1]}

    return jsonify(nearest_hospital)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
