# Bidirectional, weighted graph (distances are approximate km for demo)
locations_graph = {
    "Chrompet Railway Station": {"MIT": 0.5, "Chrompet Bus Stand": 0.7, "GST Road Chrompet": 0.4},
    "MIT": {"Chrompet Railway Station": 0.5, "Chrompet Market": 0.6, "Kamaraj Street": 0.5},
    "Chrompet Bus Stand": {"Chrompet Railway Station": 0.7, "Saravana Stores Chrompet": 0.6, "Hasthinapuram Main Road": 1.2},
    "Saravana Stores Chrompet": {"Chrompet Bus Stand": 0.6, "Chrompet Market": 0.8, "Chrompet Signal": 0.9},
    "Chrompet Market": {"MIT": 0.6, "Saravana Stores Chrompet": 0.8, "Radha Nagar": 1.2},
    "GST Road Chrompet": {"Chrompet Railway Station": 0.4, "Chrompet Signal": 0.7, "Pallavaram Signal": 1.6},
    "Chrompet Signal": {"Saravana Stores Chrompet": 0.9, "GST Road Chrompet": 0.7, "Tambaram Sanatorium": 1.7},
    "Hasthinapuram Main Road": {"Chrompet Bus Stand": 1.2, "Kumaran Kundram Temple": 1.0, "Radha Nagar": 1.0},
    "Kumaran Kundram Temple": {"Hasthinapuram Main Road": 1.0, "Kumaran Nagar": 0.7},
    "Kumaran Nagar": {"Kumaran Kundram Temple": 0.7, "Thiruneermalai Road": 1.0},
    "Radha Nagar": {"Chrompet Market": 1.2, "Hasthinapuram Main Road": 1.0, "Balaji Nagar": 0.8},
    "Balaji Nagar": {"Radha Nagar": 0.8, "Nemilichery": 1.4},
    "Nemilichery": {"Balaji Nagar": 1.4, "Pammal": 2.0},
    "Pammal": {"Nemilichery": 2.0, "Pallavaram Bus Stand": 1.8, "Thiruneermalai Road": 2.2},
    "Pallavaram Bus Stand": {"Pammal": 1.8, "Pallavaram Railway Station": 0.8, "Pallavaram Signal": 0.7},
    "Pallavaram Railway Station": {"Pallavaram Bus Stand": 0.8, "Tirusulam Bridge": 1.5},
    "Tirusulam Bridge": {"Pallavaram Railway Station": 1.5, "Chennai Airport Metro": 1.2},
    "Chennai Airport Metro": {"Tirusulam Bridge": 1.2},
    "Pallavaram Signal": {"Pallavaram Bus Stand": 0.7, "GST Road Chrompet": 1.6},
    "Tambaram Sanatorium": {"Chrompet Signal": 1.7, "Tambaram Bus Stand": 1.2},
    "Tambaram Bus Stand": {"Tambaram Sanatorium": 1.2, "Tambaram Railway Station": 0.5},
    "Tambaram Railway Station": {"Tambaram Bus Stand": 0.5, "Tambaram Market": 0.7},
    "Tambaram Market": {"Tambaram Railway Station": 0.7, "West Tambaram": 1.4},
    "West Tambaram": {"Tambaram Market": 1.4, "Selaiyur": 2.2},
    "Selaiyur": {"West Tambaram": 2.2, "Sembakkam": 1.6},
    "Sembakkam": {"Selaiyur": 1.6, "Medavakkam": 3.0},
    "Medavakkam": {"Sembakkam": 3.0, "Perumbakkam": 3.5},
    "Perumbakkam": {"Medavakkam": 3.5, "Sholinganallur": 4.5},
    "Sholinganallur": {"Perumbakkam": 4.5, "Thoraipakkam": 3.5},
    "Thoraipakkam": {"Sholinganallur": 3.5}
}

# Ensure strict bidirection (in case you hand-edit later)
for u in list(locations_graph.keys()):
    for v, w in list(locations_graph[u].items()):
        locations_graph.setdefault(v, {})
        if u not in locations_graph[v]:
            locations_graph[v][u] = w

# Approx coordinates (lat, lng)
coordinates = {
    "Chrompet Railway Station": [12.9507, 80.1402],
    "MIT": [12.9489, 80.1383],
    "Chrompet Bus Stand": [12.9515, 80.1415],
    "Saravana Stores Chrompet": [12.9528, 80.1428],
    "Chrompet Market": [12.9498, 80.1398],
    "GST Road Chrompet": [12.9545, 80.1420],
    "Chrompet Signal": [12.9562, 80.1441],
    "Hasthinapuram Main Road": [12.9465, 80.1432],
    "Kumaran Kundram Temple": [12.9437, 80.1482],
    "Kumaran Nagar": [12.9447, 80.1472],
    "Radha Nagar": [12.9442, 80.1451],
    "Balaji Nagar": [12.9430, 80.1465],
    "Nemilichery": [12.9398, 80.1502],
    "Pammal": [12.9678, 80.1442],
    "Pallavaram Bus Stand": [12.9670, 80.1503],
    "Pallavaram Railway Station": [12.9675, 80.1491],
    "Tirusulam Bridge": [12.9810, 80.1630],
    "Chennai Airport Metro": [12.9823, 80.1639],
    "Pallavaram Signal": [12.9657, 80.1525],
    "Tambaram Sanatorium": [12.9603, 80.1472],
    "Tambaram Bus Stand": [12.9621, 80.1495],
    "Tambaram Railway Station": [12.9632, 80.1508],
    "Tambaram Market": [12.9650, 80.1525],
    "West Tambaram": [12.9678, 80.1540],
    "Selaiyur": [12.9275, 80.1470],
    "Sembakkam": [12.9220, 80.1488],
    "Medavakkam": [12.9145, 80.1700],
    "Perumbakkam": [12.8990, 80.1930],
    "Sholinganallur": [12.9020, 80.2270],
    "Thoraipakkam": [12.9460, 80.2330],
    "Thiruneermalai Road": [12.9573, 80.1284],
    "Kamaraj Street": [12.9496, 80.1375],
}
