let userLatitude = null;  // Default to null
let userLongitude = null; // Default to null

// Function to get the user's geolocation
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            userLatitude = position.coords.latitude;
            userLongitude = position.coords.longitude;

            // Print coordinates to the console for debugging
            console.log("User's Latitude: " + userLatitude);
            console.log("User's Longitude: " + userLongitude);

            // Displaying the coordinates in the input fields
            document.getElementById('latitude').value = userLatitude !== null ? userLatitude.toString() : '';
            document.getElementById('longitude').value = userLongitude !== null ? userLongitude.toString() : '';

            // Optionally show the coordinates in the location input field
            document.getElementById('location').value = userLatitude && userLongitude 
                ? `Lat: ${userLatitude}, Lng: ${userLongitude}` 
                : 'Location not available';
        }, function() {
            console.warn("Geolocation failed or is not supported by this browser.");
            
            // Set latitude and longitude to empty string
            document.getElementById('latitude').value = '';
            document.getElementById('longitude').value = '';
            document.getElementById('location').value = 'Location not available';
        });
    } else {
        console.warn("Geolocation is not supported by this browser.");
        
        // Set latitude and longitude to empty string
        document.getElementById('latitude').value = '';
        document.getElementById('longitude').value = '';
        document.getElementById('location').value = 'Location not available';
    }
}

// Run the getUserLocation function on page load to get user's coordinates
window.onload = function() {
    getUserLocation();
};