const API_BASE = "http://127.0.0.1:5000";

async function fetchData() {
  const res = await fetch(`${API_BASE}/data`);
  const data = await res.json();
  populateTable(data);
  renderCharts(data);
}

function populateTable(data) {
  const tbody = document.querySelector("#transactions tbody");
  tbody.innerHTML = "";

  const filter = document.getElementById("searchInput").value.toLowerCase();

  data
    .filter(row => {
      return (
        row.type.toLowerCase().includes(filter) ||
        row.amount?.toString().includes(filter)
      );
    })
    .forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.date}</td>
        <td>${row.message}</td>
        <td>${row.type}</td>
        <td>${row.amount ?? ''}</td>
      `;
      tbody.appendChild(tr);
    });
}

function uploadXML() {
  document.getElementById("xmlFile").click();
}

async function handleXMLUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData
  });

  const result = await res.json();
  alert(result.message);
  fetchData();
}

function renderCharts(data) {
  const types = {};
  const months = {};

  data.forEach(row => {
    const type = row.type;
    const month = row.date?.slice(0, 7);

    types[type] = (types[type] || 0) + 1;
    months[month] = (months[month] || 0) + 1;
  });

  renderPieChart(types);
  renderBarChart(months);
}

function renderPieChart(types) {
  const ctx = document.getElementById("typeChart").getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(types),
      datasets: [{
        label: "Transaction Count by Type",
        data: Object.values(types),
        backgroundColor: generateColors(Object.keys(types).length)
      }]
    }
  });
}

function renderBarChart(months) {
  const ctx = document.getElementById("monthlyChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(months),
      datasets: [{
        label: "Monthly Transaction Count",
        data: Object.values(months),
        backgroundColor: "rgba(54, 162, 235, 0.7)"
      }]
    }
  });
}

function generateColors(n) {
  return Array.from({ length: n }, () =>
    `hsl(${Math.random() * 360}, 70%, 60%)`
  );
}

document.getElementById("searchInput").addEventListener("input", fetchData);
window.onload = fetchData;
document.getElementById("reloadBtn").addEventListener("click", fetchData);

