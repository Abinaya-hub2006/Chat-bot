from flask import Flask, render_template, request, jsonify
import folium
import os

from map_data import locations_graph, coordinates
from routing_algorithms import bfs, dfs

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", locations=list(locations_graph.keys()))



@app.route('/get_route', methods=['POST'])
def get_route():
    data = request.get_json()
    start = data.get("start", "").strip()
    end = data.get("end", "").strip()
    algo = data.get("algo", "bfs").lower()

    if not start or not end:
        return jsonify({"error": "Start and End locations are required."}), 400

    if start not in coordinates or end not in coordinates:
        return jsonify({"error": "Invalid Start or End location."}), 400

    if algo == "bfs":
        path = bfs(locations_graph, start, end)
    elif algo == "dfs":
        path = dfs(locations_graph, start, end)
    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    if not path:
        return jsonify({"error": "No path found."}), 404

    # Create Folium Map
    folium_map = folium.Map(location=coordinates[start], zoom_start=15)

    for i in range(len(path) - 1):
        folium.Marker(location=coordinates[path[i]], popup=path[i], icon=folium.Icon(color='blue')).add_to(folium_map)
        folium.PolyLine(locations=[coordinates[path[i]], coordinates[path[i + 1]]], color='red').add_to(folium_map)

    folium.Marker(location=coordinates[path[-1]], popup=path[-1], icon=folium.Icon(color='green')).add_to(folium_map)

    folium_map.save("templates/map.html")

    return jsonify({"route": path})


@app.route('/map')
def show_map():
    return render_template("map.html")


if __name__ == '__main__':
    app.run(debug=True)
