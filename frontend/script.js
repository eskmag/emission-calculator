document.getElementById("emission-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  // Konverter tallfelter (alle input values er strings!)
  const fieldsToNumber = [
    "km_car", "km_bus", "km_train",
    "short_flights", "medium_flights", "long_flights",
    "kwh_electricity", "kwh_oil", "kwh_gas", "kwh_wood"
  ];
  fieldsToNumber.forEach(key => data[key] = Number(data[key] || 0));

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error("API-feil");

    const result = await response.json();

    document.getElementById("result").innerHTML = `
      <h2>Resultat</h2>
      <p>Transport: ${result.transport.toFixed(2)} kg CO₂</p>
      <p>Mat: ${result.food.toFixed(2)} kg CO₂</p>
      <p>Energi: ${result.energy.toFixed(2)} kg CO₂</p>
      <hr />
      <p><strong>Total: ${result.total.toFixed(2)} kg CO₂</strong></p>
    `;
  } catch (err) {
    document.getElementById("result").innerHTML = `<p style="color:red;">Feil: ${err.message}</p>`;
  }
});
