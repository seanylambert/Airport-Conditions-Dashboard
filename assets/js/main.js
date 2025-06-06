// JavaScript logic for fetchin and displaying weather data

// Confirm script connection to html
console.log("main.js loaded");

// Handle Enter key press in the ICAO input box
document.getElementById("airportInput").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent page reload
    document.getElementById("fetchBtn").click(); // Trigger button click
  }
});

document.getElementById("fetchBtn").addEventListener("click", () => {
  const icaoCode = document.getElementById("airportInput").value.trim().toUpperCase();
  
  // Handle empty user input
  if (!icaoCode) {
    alert("Please enter a valid ICAO code (e.g., KRHV).");
    return;
  }

  const apiUrl = `http://127.0.0.1:5000/metar?station=${icaoCode}`;

  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      console.log("METAR data:", data);

      if (Array.isArray(data) && data.length > 0) {
        const metar = data[0];

        document.getElementById("rawMetar").textContent = metar.rawOb || "Unavailable";
        document.getElementById("name").textContent = metar.name || "N/A";
        document.getElementById("obsTime").textContent = metar.localObsTime || metar.obsTime || "N/A";
        document.getElementById("temp").textContent = metar.temp !== undefined ? `${metar.temp} °C` : "N/A";
        document.getElementById("dewp").textContent = metar.dewp !== undefined ? `${metar.dewp} °C` : "N/A";
        document.getElementById("wind").textContent =
          metar.windDir !== undefined && metar.windSpeed !== undefined
            ? `${metar.windDir}° at ${metar.windSpeed} kt`
            : "Calm or data unavailable";
        document.getElementById("visib").textContent = metar.visib !== undefined ? `${metar.visib} SM` : "N/A";

        const altimInHg = (metar.altim / 33.8639).toFixed(2);
        document.getElementById("altim").textContent = `${altimInHg} inHg (${metar.altim} hPa)`;

        const cloudInfo = metar.clouds && metar.clouds.length > 0
          ? metar.clouds.map(c => `${c.cover} at ${c.baseFt} ft`).join(', ')
          : "Clear or not reported";
        document.getElementById("clouds").textContent = cloudInfo;

        //  Show the METAR section
        document.getElementById("metarSection").style.display = "block";
      } else {
        alert("No METAR data found. Check the ICAO code and try again.");
      }
    })
    .catch(error => {
      console.error("Error fetching METAR data:", error);
      document.getElementById("metarSection").style.display = "none";
      alert("There was an error fetching the data. Try again.");
    });
});