from flask import Flask, render_template, request, jsonify, send_from_directory
import folium
import os
import math

from map_data import locations_graph, coordinates
from routing_algorithms import bfs, dfs, ucs, astar, greedy, ids, dls, ao_star

app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------- Heuristic for A*, Greedy, AO* (Euclidean in lat/lng space) ----------
def heuristic(a, b):
    (x1, y1), (x2, y2) = coordinates[a], coordinates[b]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

@app.route("/")
def home():
    # Locations for dropdowns
    return render_template("index.html", locations=sorted(list(locations_graph.keys())))

@app.route("/get_route", methods=["POST"])
def get_route():
    data = request.get_json(force=True)
    start = data.get("start", "").strip()
    end = data.get("end", "").strip()
    algo = data.get("algo", "bfs").lower()

    if not start or not end:
        return jsonify({"error": "Start and End locations are required."}), 400
    if start not in locations_graph or end not in locations_graph:
        return jsonify({"error": "Invalid Start or End location."}), 400
    if start not in coordinates or end not in coordinates:
        return jsonify({"error": "Missing coordinates for Start or End location."}), 400

    # -------- choose algorithm --------
    if algo == "bfs":
        path = bfs(locations_graph, start, end)
    elif algo == "dfs":
        path = dfs(locations_graph, start, end)
    elif algo == "ucs":
        path = ucs(locations_graph, start, end)
    elif algo == "astar":
        path = astar(locations_graph, start, end, coordinates)
    elif algo == "greedy":
        path = greedy(locations_graph, start, end, coordinates)
    elif algo == "ids":
        path = ids(locations_graph, start, end, max_depth=50)
    elif algo == "dls":
        # You can pass limit from UI later if you want
        path = dls(locations_graph, start, end, limit=6)
    elif algo == "ao":
        path = ao_star(locations_graph, start, end, coordinates)
    else:
        return jsonify({"error": f"Invalid algorithm: {algo}"}), 400

    if not path:
        return jsonify({"error": "No path found."}), 404

    # -------- Build Folium map --------
    fmap = folium.Map(location=coordinates[start], zoom_start=15)

    # draw all nodes faintly
    for node, (lat, lng) in coordinates.items():
        folium.CircleMarker(
            location=[lat, lng],
            radius=4,
            popup=node,
            fill=True,
            fill_opacity=0.6,
            opacity=0.6
        ).add_to(fmap)

    # highlight the path (red polyline) and blue markers
    for i, node in enumerate(path):
        color = "blue"
        if i == 0:
            color = "orange"
        elif i == len(path) - 1:
            color = "green"

        folium.Marker(
            location=coordinates[node],
            popup=node,
            icon=folium.Icon(color=color)
        ).add_to(fmap)

        if i < len(path) - 1:
            a, b = path[i], path[i + 1]
            folium.PolyLine(
                locations=[coordinates[a], coordinates[b]],
                weight=5,
                opacity=0.9
            ).add_to(fmap)

    # save map to templates/map.html (overwrites)
    map_path = os.path.join(app.template_folder, "map.html")
    fmap.save(map_path)

    return jsonify({"route": path})

@app.route("/map")
def show_map():
    # After first /get_route call, map.html exists & is a complete HTML by Folium
    if os.path.exists(os.path.join(app.template_folder, "map.html")):
        return render_template("map.html")
    # initial placeholder before first route
    return render_template("map.html")

# static file helper (optional)
@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
