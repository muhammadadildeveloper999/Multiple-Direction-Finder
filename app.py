from flask import Flask, render_template, request
import googlemaps
import random

app = Flask(__name__)

gmaps = googlemaps.Client(key="AIzaSyAEMeWgeUm5zc7D4mjUdh_gkdRdyYf_ZcU")

@app.route('/')
def show_map():
    return render_template('map.html', directions=None, start_location=None)

@app.route('/calculate_directions', methods=['POST'])
def calculate_directions():
    address = request.form['address']
    radius = float(request.form['radius'])  # Get the radius from the form

    start_location = None

    geocode_result = gmaps.geocode(address)

    if geocode_result:
        user_latitude = geocode_result[0]['geometry']['location']['lat']
        user_longitude = geocode_result[0]['geometry']['location']['lng']

        num_points = 5

        nearby_points = []

        for _ in range(num_points):
            random_distance = random.uniform(1, radius)  # Use the provided radius
            random_angle = random.uniform(0, 360)
            destination_location = {
                "lat": user_latitude + (random_distance / 111.32) * (180 / 3.141592653589793),
                "lng": user_longitude + (random_distance / 111.32) * (180 / 3.141592653589793) / (40008000 / 360)
            }
            nearby_points.append(destination_location)

        directions_data = []
        for point in nearby_points:
            directions = get_directions({"lat": user_latitude, "lng": user_longitude}, point)
            directions_data.append(directions)

        start_location = {"lat": user_latitude, "lng": user_longitude}

        return render_template('map.html', start_location=start_location, nearby_points=nearby_points, directions=directions_data)

    else:
        return render_template('map.html', directions=None, start_location=None)


def get_directions(origin, destination):
    directions = gmaps.directions(origin, destination, mode="driving")
    return directions

if __name__ == '__main__':
    app.run(debug=True)

