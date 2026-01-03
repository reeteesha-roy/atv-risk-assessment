fetch("/analyze")
  .then(res => res.json())
  .then(data => {

    const labels = data.map(r => r.risk_name);
    const scores = data.map(r => r.score);

    const ctx = document.getElementById("riskChart").getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Risk Score",
          data: scores,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });

  });
