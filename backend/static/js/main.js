// static/js/main.js

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

document.getElementById('icao-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const icao = document.getElementById('icao').value.toUpperCase();
  const response = await fetch(`http://127.0.0.1:5000/metar-history?icao=${icao}`);
  const data = await response.json();

  const container = document.getElementById('results');
  if (data.length === 0) {
    container.innerHTML = "<p>No historical METARs found for this station.</p>";
    return;
  }

  const rows = data.map(m => `
    <tr>
      <td>${m.observation_time}</td>
      <td>${m.temperature_c ?? '—'}</td>
      <td>${m.dewpoint_c ?? '-'}</td>
      <td>${m.wind_dir_degrees ?? '—'}</td>
      <td>${m.wind_speed_kt ?? '—'}</td>
      <td>${m.visibility_statute_mi ?? '—'}</td>
      <td>${m.elevation ?? '-'}</td>
      <td>${m.cloud_cover ?? '-'}</td>
      <td>${m.cloud_base ?? '-'}</td>
    </tr>
  `).join('');

  container.innerHTML = `
    <table border="1">
      <thead>
        <tr>
          <th>Time (UTC)</th>
          <th>Temp (°C)</th>
          <th>Dewpoint (°C)</th>
          <th>Wind Dir (°)</th>
          <th>Wind Speed (kn)</th>
          <th>Visibility (SM)</th>
          <th>Elevation (m)</th>
          <th>Cloud Cover (ft)</th>
          <th>Cloud Base (ft)</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
});


document.getElementById('icao-form2').addEventListener('submit', async function (e) {
  e.preventDefault();

  const icao2 = document.getElementById('icao2').value.trim().toUpperCase();
  const response = await fetch(`http://127.0.0.1:5000/historic-rawMETAR?icao=${icao2}`);
  const data = await response.json();

  const container = document.getElementById('historic_rawMETAR_results');

  if (!Array.isArray(data) || data.length === 0) {
    container.innerHTML = "<p>No historical METARs found for this station.</p>";
    return;
  }

  const rows = data.map(m => `
    <tr>
      <td>${m.observation_time || '—'}</td>
      <td>${m.raw_text || '—'}</td>
    </tr>
  `).join('');

  container.innerHTML = `
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
      <thead>
        <tr>
          <th>Time (UTC)</th>
          <th>rawMETAR</th>
        </tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>
  `;
});









// document.addEventListener('DOMContentLoaded', () => {
//   const input = document.getElementById('airportInput');
//   const header = document.getElementById('metarHeader');

//   input.addEventListener('input', () => {
//     const code = input.value.toUpperCase();
//     if (code.length === 4) {
//       header.textContent = `Current METAR Conditions for ${code}`;
//     } else {
//       header.textContent = 'Current METAR Conditions';
//     }
//   });
// });