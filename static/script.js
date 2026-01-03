async function runAI() {
  const res = await fetch("/analyze", { method: "POST" });
  const data = await res.json();

  const labels = data.map(r => r.risk_name);
  const scores = data.map(r => r.score);

  document.getElementById("results").innerHTML = data.map(r => `
    <div class="card">
      <h3>${r.risk_name}</h3>
      <p><b>Scenario:</b> ${r.scenario}</p>
      <p><b>Score:</b> ${r.score}</p>
      <p>${r.reason}</p>
    </div>
  `).join("");

  new Chart(document.getElementById("riskChart"), {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Risk Score",
        data: scores
      }]
    }
  });
}
