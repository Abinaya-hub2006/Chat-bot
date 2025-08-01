// Runs when page is fully loaded
window.onload = function () {
    const startSelect = document.getElementById("start");
    const endSelect = document.getElementById("end");

    // Fill dropdowns with location names passed from Flask
    locations.forEach(loc => {
        const startOption = document.createElement("option");
        startOption.value = loc;
        startOption.text = loc;
        startSelect.appendChild(startOption);

        const endOption = document.createElement("option");
        endOption.value = loc;
        endOption.text = loc;
        endSelect.appendChild(endOption);
    });

    // Set default values if available
    if (locations.includes("MIT")) {
        startSelect.value = "MIT";
    }
    if (locations.includes("Kumaran Kundram Temple")) {
        endSelect.value = "Kumaran Kundram Temple";
    }
};

// Called when the "Get Route" button is clicked
function getRoute() {
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;
    const algo = document.getElementById("algo").value;

    // Clear previous results
    document.getElementById("routeResult").innerHTML = "Loading...";
    document.getElementById("mapFrame").src = "";

    fetch("/get_route", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ start, end, algo })
    })
    .then(response => response.json())
    .then(data => {
        const routeDiv = document.getElementById("routeResult");

        if (data.error) {
            routeDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
        } else {
            routeDiv.innerHTML = `<p><strong>Route:</strong> ${data.route.join(" → ")}</p>`;
            document.getElementById("mapFrame").src = "/map";
        }
    })
    .catch(error => {
        document.getElementById("routeResult").innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
    });
}
