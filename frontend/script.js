const API_BASE = "http://127.0.0.1:5000";
const TRANSACTION_TYPES = [
    "All", "Received", "Payment", "Airtime", "CashPower", "Transfer",
    "Deposit", "Withdrawal", "BankTransfer", "ThirdParty", "Bundle"
];

// Store chart instances globally
let typeChartInstance = null;
let monthlyChartInstance = null;
let hourlyChartInstance = null;

// Pagination state
let currentPage = 1;
const perPage = 5;
let allData = [];

async function fetchData(page = 1, search = "", forContacts = false) {
    try {
        const params = forContacts 
            ? `?page=1&per_page=1000&search=${encodeURIComponent(search)}`
            : `?page=${page}&per_page=${perPage}&search=${encodeURIComponent(search)}`;
        const res = await fetch(`${API_BASE}/data${params}`);
        if (!res.ok) throw new Error("Failed to fetch data");
        const { data: fetchedData, total, page: current, per_page } = await res.json();
        allData = fetchedData;
        currentPage = current;
        const totalPages = Math.ceil(total / per_page);
        populateTable();
        renderCharts();
        renderContactsTab();
        renderPatternsTab();
        document.getElementById("pageInfo").textContent = `Page ${currentPage} of ${totalPages || 1}`;
        document.getElementById("prevPage").disabled = currentPage === 1;
        document.getElementById("nextPage").disabled = currentPage === totalPages || totalPages === 0;
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch transactions");
    }
}

function populateTable() {
    const tbody = document.querySelector("#transactions tbody");
    tbody.innerHTML = "";
    allData.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="p-3">${row.date}</td>
            <td class="p-3">${row.message}</td>
            <td class="p-3">${row.type}</td>
            <td class="p-3">${row.amount ?? "N/A"} RWF</td>
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
    try {
        const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
        const result = await res.json();
        alert(result.message || "Data saved successfully!");
        if (res.ok) {
            currentPage = 1;
            await fetchData();
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        alert("Failed to upload XML file");
    }
}

function renderCharts() {
    const types = {};
    const months = {};
    allData.forEach(row => {
        types[row.type] = (types[row.type] || 0) + 1;
        months[row.date?.slice(0, 7) || "Unknown"] = (months[row.date?.slice(0, 7) || "Unknown"] || 0) + 1;
    });

    if (typeChartInstance) {
        typeChartInstance.destroy();
        typeChartInstance = null;
    }
    if (monthlyChartInstance) {
        monthlyChartInstance.destroy();
        monthlyChartInstance = null;
    }
    if (hourlyChartInstance) {
        hourlyChartInstance.destroy();
        hourlyChartInstance = null;
    }

    renderPieChart(types);
    renderBarChart(months);
    renderHourlyChart();
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
                legend: { position: "top" }
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

function renderHourlyChart() {
    const hourly = Array(24).fill(0);
    allData.forEach(row => {
        const hour = new Date(row.date).getHours();
        hourly[hour]++;
    });

    const ctx = document.getElementById("hourlyChart").getContext("2d");
    hourlyChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
            datasets: [{
                label: "Hourly Transactions",
                data: hourly,
                backgroundColor: "#FBBF24"
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}

function generateColors(n) {
    return Array.from({ length: n }, () => `hsl(${Math.random() * 360}, 70%, 60%)`);
}

function renderContactsTab() {
    const contacts = {};
    allData.forEach(row => {
        const match = row.message.match(/(078|072|073|079)\d{7}/);
        if (match) {
            const contact = match[0];
            contacts[contact] = (contacts[contact] || 0) + 1;
        }
    });
    console.log("Extracted contacts:", contacts, "Total messages:", allData.length, "Messages:", allData.map(row => row.message));
    const topContacts = Object.entries(contacts).sort((a, b) => b[1] - a[1]).slice(0, 5);
    document.getElementById("topContactsList").innerHTML = topContacts.length > 0 
        ? topContacts.map(([contact, count]) => `
            <div class="flex justify-between p-2 border-b">
                <span>${contact}</span>
                <span>${count} transactions</span>
            </div>
        `).join("")
        : "<p class='p-2 text-gray-500'>No contacts found</p>";
}

function renderPatternsTab() {
    // Handled by renderHourlyChart in renderCharts
}

// Pagination event listeners
document.getElementById("prevPage").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        fetchData(currentPage, document.getElementById("searchInput").value);
    }
});

document.getElementById("nextPage").addEventListener("click", () => {
    currentPage++;
    fetchData(currentPage, document.getElementById("searchInput").value);
});

document.getElementById("searchInput").addEventListener("input", () => {
    currentPage = 1;
    fetchData(1, document.getElementById("searchInput").value);
});

document.getElementById("reloadBtn").addEventListener("click", () => {
    currentPage = 1;
    fetchData();
});

document.getElementById("xmlFile").addEventListener("change", handleXMLUpload);

// Highlight active card and filter
document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("click", () => {
        document.querySelectorAll(".card").forEach(c => c.classList.remove("active"));
        card.classList.add("active");
        const type = card.dataset.type;
        document.getElementById("searchInput").value = type === "All" ? "" : type;
        currentPage = 1;
        fetchData(1, type === "All" ? "" : type);
    });
});

document.querySelectorAll(".tab-button").forEach(button => {
    button.addEventListener("click", () => {
        document.querySelectorAll(".tab-button").forEach(btn => btn.classList.remove("active"));
        button.classList.add("active");
        document.querySelectorAll(".tab-content").forEach(content => content.classList.add("hidden"));
        document.getElementById(button.id.replace("tab-", "") + "-content").classList.remove("hidden");
        if (button.id === "tab-contacts") {
            fetchData(1, document.getElementById("searchInput").value, true);
        }
    });
});

window.onload = () => {
    fetchData();
    lucide.createIcons();
};