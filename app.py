from flask import Flask, render_template, request, redirect, url_for
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Simulated hospital data (replace with actual data source)
hospitals = [
    {"name": "Hospital Guru Kirpa, Best Rehab Center in Punjab", "lat": 31.096134, "lng": 75.778770},
    {"name": "Hospital Ahmedabad Civil Hospital, Ahmedabad, Gujarat, India", "lat": 23.053967, "lng": 72.603844},
    {"name": "Advanced Centre for Eyes, Kitchlu Nagar, Ludhiana, Punjab, India", "lat": 30.912411, "lng": 75.819412},
    {"name": "Apple Hospital, Surat, Gujarat, India", "lat": 	21.182947, "lng": 72.831581},
    {"name": "Padmini Nursing Home, Chetpet, Chennai, Tamil Nadu, India", "lat": 	13.072790, "lng": 80.234421},
    {"name": "Vihar Hospital, Anand, Gujarat, India", "lat": 22.554609, "lng": 	72.967361}
    # Add more hospitals with their coordinates
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_nearest_hospital', methods=['POST'])
def find_nearest_hospital():
    # Get user's current location from form submission
    user_lat = float(request.form['latitude'])
    user_lng = float(request.form['longitude'])

    # Find the nearest hospital
    nearest_hospital = find_nearest_hospital(user_lat, user_lng)

    if nearest_hospital:
        return redirect(url_for('hospital', hospital_name=nearest_hospital['name']))
    else:
        return "No hospitals found nearby."

@app.route('/hospital/<hospital_name>')
def hospital(hospital_name):
    hospital = next((h for h in hospitals if h['name'] == hospital_name), None)
    if hospital:
        return render_template('hospital.html', hospital=hospital)
    else:
        return "Hospital not found."

def find_nearest_hospital(user_lat, user_lng):
    nearest_hospital = None
    min_distance = float('inf')

    for hospital in hospitals:
        distance = calculate_distance(user_lat, user_lng, hospital['lat'], hospital['lng'])
        if distance < min_distance:
            min_distance = distance
            nearest_hospital = hospital

    return nearest_hospital

def calculate_distance(lat1, lng1, lat2, lng2):
    # Convert latitude and longitude from degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    
    # Radius of the Earth in kilometers
    R = 6371.0 
    
    # Haversine formula to calculate distance between two points
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

if __name__ == '__main__':
    app.run(debug=True)
