const btn = document.getElementById("findRoute");
const out = document.getElementById("output");
const mapLink = document.getElementById("mapLink");

btn.addEventListener("click", async () => {
  const start = document.getElementById("start").value;
  const end = document.getElementById("end").value;
  const algo = document.getElementById("algo").value;

  out.innerHTML = "Finding route...";
  mapLink.innerHTML = "";

  try {
    const res = await fetch("/get_route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start, end, algo })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: "Unknown error" }));
      out.innerHTML = `<div class="error">${err.error || "Failed to get route"}</div>`;
      return;
    }

    const data = await res.json();
    const route = data.route || [];
    out.innerHTML = `<h3>Route (${algo.toUpperCase()}):</h3><p>${route.join(" ➜ ")}</p>`;
    mapLink.innerHTML = `<a class="map-btn" href="/map" target="_blank">🌍 View Map</a>`;
  } catch (e) {
    out.innerHTML = `<div class="error">Network error. Check server logs.</div>`;
  }
});
