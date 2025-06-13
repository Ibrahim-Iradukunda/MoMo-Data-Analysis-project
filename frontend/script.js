const API_BASE = "http://127.0.0.1:5000";

// Store chart instances globally
let typeChartInstance = null;
let monthlyChartInstance = null;

// Pagination state
let currentPage = 1;
const rowsPerPage = 5; // Reduced to 5 for demo; adjust as needed
let allData = [];

async function fetchData() {
  try {
    const res = await fetch(`${API_BASE}/data`);
    if (!res.ok) throw new Error('Failed to fetch data');
    const data = await res.json();
    allData = data; // Store all data for pagination
    populateTable(data);
    renderCharts(data);
  } catch (error) {
    console.error('Error fetching data:', error);
    alert('Failed to fetch transactions');
  }
}

function populateTable(data) {
  const tbody = document.querySelector("#transactions tbody");
  tbody.innerHTML = "";
  const filter = document.getElementById("searchInput").value.toLowerCase();

  // Filter data by date or type
  const filteredData = data.filter(row => {
    const dateMatch = row.date.slice(0, 10).includes(filter);
    const typeMatch = row.type.toLowerCase().includes(filter);
    return dateMatch || typeMatch;
  });

  // Calculate pagination
  const totalRows = filteredData.length;
  const totalPages = Math.ceil(totalRows / rowsPerPage);
  currentPage = Math.min(currentPage, totalPages || 1);

  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  const paginatedData = filteredData.slice(start, end);

  // Populate table with paginated data
  paginatedData.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.date}</td>
      <td>${row.message}</td>
      <td>${row.type}</td>
      <td>${row.amount ?? 'N/A'}</td>
    `;
    tbody.appendChild(tr);
  });

  // Update pagination controls
  const pageInfo = document.getElementById("pageInfo");
  pageInfo.textContent = `Page ${currentPage} of ${totalPages || 1}`;
  document.getElementById("prevPage").disabled = currentPage === 1;
  document.getElementById("nextPage").disabled = currentPage === totalPages || totalPages === 0;
}

function uploadXML() {
  document.getElementById("xmlFile").click();
}

async function handleXMLUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData
    });
    const result = await res.json();
    alert(result.message || 'Data saved successfully!'); // Confirm data saved
    if (res.ok) {
      currentPage = 1; // Reset to first page
      await fetchData(); // Reload data after upload
    }
  } catch (error) {
    console.error('Error uploading file:', error);
    alert('Failed to upload XML file');
  }
}

function renderCharts(data) {
  const types = {};
  const months = {};

  data.forEach(row => {
    const type = row.type;
    const month = row.date?.slice(0, 7) || 'Unknown';
    types[type] = (types[type] || 0) + 1;
    months[month] = (months[month] || 0) + 1;
  });

  // Destroy existing charts
  if (typeChartInstance) {
    typeChartInstance.destroy();
    typeChartInstance = null;
  }
  if (monthlyChartInstance) {
    monthlyChartInstance.destroy();
    monthlyChartInstance = null;
  }

  renderPieChart(types);
  renderBarChart(months);
}

function renderPieChart(types) {
  const ctx = document.getElementById("typeChart").getContext("2d");
  typeChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(types),
      datasets: [{
        label: "Transaction Count by Type",
        data: Object.values(types),
        backgroundColor: generateColors(Object.keys(types).length)
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' }
      }
    }
  });
}

function renderBarChart(months) {
  const ctx = document.getElementById("monthlyChart").getContext("2d");
  monthlyChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(months).sort(),
      datasets: [{
        label: "Monthly Transaction Count",
        data: Object.values(months),
        backgroundColor: "rgba(54, 162, 235, 0.7)"
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

function generateColors(n) {
  return Array.from({ length: n }, () =>
    `hsl(${Math.random() * 360}, 70%, 60%)`
  );
}

// Pagination event listeners
document.getElementById("prevPage").addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage--;
    populateTable(allData); // Use all data for pagination
  }
});

document.getElementById("nextPage").addEventListener("click", () => {
  currentPage++;
  populateTable(allData); // Use all data for pagination
});

document.getElementById("searchInput").addEventListener("input", () => {
  currentPage = 1; // Reset to first page on search
  populateTable(allData);
});

document.getElementById("reloadBtn").addEventListener("click", () => {
  currentPage = 1; // Reset to first page on reload
  fetchData();
});

window.onload = fetchData;





// Highlight active card and filter
document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("click", () => {
    const selectedType = card.dataset.type;

    // Highlight selected card
    document.querySelectorAll(".card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");

    // Update search input with type (except "All")
    document.getElementById("searchInput").value = selectedType === "All" ? "" : selectedType;
    currentPage = 1;
    populateTable(allData);
  });
});
