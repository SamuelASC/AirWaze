# app.py
from flask import Flask, render_template, jsonify
import folium
import random
import math

app = Flask(__name__)

class QuadTreeNode:
    def __init__(self, bounds):
        self.bounds = bounds
        self.drones = []
        self.children = None

# Function to insert a drone into the quadtree
def insert_drone(node, drone):
    if not node.bounds.contains(drone["lat"], drone["lon"]):
        return False

    if len(node.drones) < 4 or node.bounds.width <= 0.001:
        node.drones.append(drone)
        return True

    if node.children is None:
        subdivide(node)

    for child in node.children:
        if insert_drone(child, drone):
            return True

    return False

# Function to subdivide a quadtree node
def subdivide(node):
    min_lat, max_lat = node.bounds.min_lat, node.bounds.max_lat
    min_lon, max_lon = node.bounds.min_lon, node.bounds.max_lon
    mid_lat = (min_lat + max_lat) / 2
    mid_lon = (min_lon + max_lon) / 2

    node.children = [
        QuadTreeNode(Bounds(min_lat, mid_lat, min_lon, mid_lon)),
        QuadTreeNode(Bounds(min_lat, mid_lat, mid_lon, max_lon)),
        QuadTreeNode(Bounds(mid_lat, max_lat, min_lon, mid_lon)),
        QuadTreeNode(Bounds(mid_lat, max_lat, mid_lon, max_lon))
    ]

    for drone in node.drones:
        for child in node.children:
            if child.bounds.contains(drone["lat"], drone["lon"]):
                insert_drone(child, drone)

    node.drones = []

class Bounds:
    def __init__(self, min_lat, max_lat, min_lon, max_lon):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon

    @property
    def width(self):
        return self.max_lon - self.min_lon

    def contains(self, lat, lon):
        return (
            self.min_lat <= lat <= self.max_lat and self.min_lon <= lon <= self.max_lon
        )

    def intersects(self, bounds):
        return not (
            bounds.max_lon < self.min_lon
            or bounds.min_lon > self.max_lon
            or bounds.max_lat < self.min_lat
            or bounds.min_lat > self.max_lat
        )

# Quadtree root node
quadtree_root = QuadTreeNode(Bounds(-22.03, -21.98, -47.96, -47.88))

# Function to generate the map
def generate_map():
    # Create a folium map centered on São Carlos, Brazil
    map_airwaze = folium.Map(location=[-22.0014, -47.8977], zoom_start=13)

    # Generate dummy drone locations
    num_drones = 100
    drone_locations = []
    for _ in range(num_drones):
        lat = random.uniform(-22.001, -21.999)
        lon = random.uniform(-47.899, -47.898)
        drone = {"lat": lat, "lon": lon}
        drone_locations.append(drone)

        # Insert drone into the quadtree
        insert_drone(quadtree_root, drone)

    # Add drone markers to the map
    for location in drone_locations:
        folium.Marker(
            [location["lat"], location["lon"]], popup="Dummy Drone"
        ).add_to(map_airwaze)

    return map_airwaze._repr_html_()

# Function to detect collisions between drones
def detect_collisions(node, min_distance, result):
    for drone in node.drones:
        for other_drone in node.drones:
            if drone != other_drone:
                distance = calculate_distance(drone["lat"], drone["lon"], other_drone["lat"], other_drone["lon"])
                if distance < min_distance:
                    result.append((drone, other_drone))

    if node.children is not None:
        for child in node.children:
            detect_collisions(child, min_distance, result)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the distance between two points using the Haversine formula
    R = 6371000  # Earth's radius in meters
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance

# Endpoint to provide updated drone positions as JSON data
@app.route("/get_drone_positions")
def get_drone_positions():
    # Generate new dummy drone locations
    num_drones = 200
    drone_positions = []
    for _ in range(num_drones):
        lat = random.uniform(-22.03, -21.98)
        lon = random.uniform(-47.96, -47.88)
        drone = {"lat": lat, "lon": lon}
        drone_positions.append(drone)

        # Update drone position in the quadtree
        insert_drone(quadtree_root, drone)

    # Detect drone collisions
    min_distance = 10  # Adjust this value based on your collision criteria (in meters)
    collisions = []
    detect_collisions(quadtree_root, min_distance, collisions)

    return jsonify({"drones": drone_positions, "collisions": collisions})

# Endpoint to render the initial map
@app.route("/")
def index():
    # Render the template with the initial map
    return render_template("index.html", map=generate_map())

if __name__ == "__main__":
    app.run(debug=True)
