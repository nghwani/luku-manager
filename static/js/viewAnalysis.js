document.addEventListener("DOMContentLoaded", function () {
    fetch("/purchase_data/")
        .then(response => response.json())
        .then(data => {
            // Handle the data structure from purchase_data endpoint
            const chartData = {
                date: data.date,      // Match backend field names
                amount: data.amount,
                units: data.units
            };
            updateCharts(chartData);
        })
        .catch(error => console.error("Error fetching data:", error));

    // Handle form submission for filtering
    document.getElementById("filterForm").addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent form from reloading the page

        const formData = new FormData(this);
        
        // Get the CSRF token from the form
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/purchase_data_filter/", {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
        })
        .catch(error => console.error("Error fetching filtered data:", error));
    });
});

// Store chart instances globally
const charts = {};

// Function to create or update a chart
function createChart(canvasId, label, data, type, bgColor, borderColor) {
    const ctx = document.getElementById(canvasId).getContext("2d");

    // Destroy the previous chart if it exists
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    // Create a new chart and store it
    charts[canvasId] = new Chart(ctx, {
        type: type,
        data: {
            labels: data.date,  // Using date consistently
            datasets: [{
                label: label,
                data: data.values,
                backgroundColor: bgColor,
                borderColor: borderColor,
                borderWidth: 2,
                pointRadius: 4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: 'Date', font: { size: 14 } } },
                y: { title: { display: true, text: label, font: { size: 14 } }, beginAtZero: true }
            }
        }
    });
}

// Function to update both charts
function updateCharts(data) {
    createChart(
        "amountChart", 
        "Amount Spent (TZS)", 
        { date: data.date, values: data.amount }, 
        "bar", 
        "rgba(0,0,255,0.6)", 
        "blue"
    );
    
    createChart(
        "unitsChart", 
        "Energy Units Purchased (KWh)", 
        { date: data.date, values: data.units }, 
        "line", 
        "rgba(0,255,0,0.2)", 
        "green"
    );
}