async function predict() {
  const data = {
    traffic: document.getElementById("traffic").value,
    pollution: document.getElementById("pollution").value,
    power_usage: document.getElementById("power_usage").value,
    water_use: document.getElementById("water_use").value,
    complaints: document.getElementById("complaints").value,
  };

  const res = await fetch('/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });

  const result = await res.json();
  document.getElementById("output").innerHTML = `
    <h2>${result.mood}</h2>
    <p>Score: ${result.score}</p>
    <p>🧠 Suggestion: ${result.suggestion}</p>
  `;

  speak(result.mood + " " + result.suggestion);
}
