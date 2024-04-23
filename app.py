from flask import Flask, render_template, request, redirect, url_for, jsonify
from geopy.distance import distance

app = Flask(__name__)

# Sample hospital data (replace with actual hospital data)
hospitals = [
    {"name": "Hospital A", "latitude": 40.73061, "longitude": -73.935242, "image": "hospital_a.jpg", "website": "https://hospital_a.com"},
    {"name": "Hospital B", "latitude": 40.748817, "longitude": -73.985428, "image": "hospital_b.jpg", "website": "https://hospital_b.com"},
    {"name": "Hospital C", "latitude": 40.707851, "longitude": -74.003002, "image": "hospital_c.jpg", "website": "https://hospital_c.com"}
    # Add more hospitals with latitude, longitude, image, and website
]

def find_nearest_hospital(user_lat, user_lon):
    # Calculate distances to all hospitals
    distances = []
    for hospital in hospitals:
        hosp_lat, hosp_lon = hospital["latitude"], hospital["longitude"]
        dist = distance((user_lat, user_lon), (hosp_lat, hosp_lon)).km
        distances.append((hospital, dist))

    # Sort distances to find the nearest hospital
    distances.sort(key=lambda x: x[1])
    nearest_hospital, nearest_distance = distances[0]

    return nearest_hospital

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    # Retrieve latitude and longitude parameters from the URL
    user_lat = float(request.args.get('lat'))
    user_lon = float(request.args.get('lon'))

    # Find the nearest hospital
    nearest_hospital = find_nearest_hospital(user_lat, user_lon)

    return render_template('result.html', hospital=nearest_hospital)

if __name__ == '__main__':
    app.run(debug=True)
