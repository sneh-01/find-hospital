document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([0, 0], 13); // Default view at (0, 0) with zoom level 13

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Function to find user's location and display nearby hospitals
    function findNearestHospitals() {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var userLat = position.coords.latitude;
                var userLng = position.coords.longitude;

                // Update map view to user's location
                map.setView([userLat, userLng], 13);

                // Add marker for user's location
                L.marker([userLat, userLng], {icon: L.icon({iconUrl: 'https://leafletjs.com/examples/custom-icons/leaf-green.png', shadowUrl: 'https://leafletjs.com/examples/custom-icons/leaf-shadow.png', iconSize: [38, 95], shadowSize: [50, 64], iconAnchor: [22, 94], shadowAnchor: [4, 62], popupAnchor: [-3, -76]}) }).addTo(map).bindPopup('Your Location').openPopup();

                // Fetch hospitals data from the server
                fetch('/get_hospitals')
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(hospital => {
                            L.marker([hospital.lat, hospital.lng]).addTo(map)
                                .bindPopup(`<b>${hospital.name}</b><br>Distance: ${calculateDistance(userLat, userLng, hospital.lat, hospital.lng).toFixed(2)} km`);
                        });
                    })
                    .catch(error => console.error('Error fetching hospitals:', error));
            }, function(error) {
                console.error('Geolocation error:', error.message);
                alert('Geolocation service failed. Please enable location access.');
            });
        } else {
            console.error('Geolocation not supported.');
            alert('Geolocation is not supported by this browser.');
        }
    }

    // Helper function to calculate distance between two points (in kilometers)
    function calculateDistance(lat1, lon1, lat2, lon2) {
        var R = 6371; // Radius of the Earth in kilometers
        var dLat = (lat2 - lat1) * Math.PI / 180;
        var dLon = (lon2 - lon1) * Math.PI / 180;
        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180)
