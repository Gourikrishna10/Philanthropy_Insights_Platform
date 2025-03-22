document.addEventListener("DOMContentLoaded", function() {
    console.log("✅ script.js loaded!");

    let charts = {};

    function createChart(canvasId, type, labels, values, labelText, colors) {
        const ctx = document.getElementById(canvasId)?.getContext("2d");
        if (!ctx) {
            console.error(`❌ Canvas element '${canvasId}' not found.`);
            return;
        }

        if (charts[canvasId]) charts[canvasId].destroy();

        charts[canvasId] = new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: labelText,
                    data: values,
                    backgroundColor: colors || ["#FF5733", "#C70039", "#900C3F", "#581845"],
                    borderColor: "#ffffff",
                    borderWidth: 1,
                    hoverBackgroundColor: "#D988B9"
                }]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1000,
                    easing: "easeInOutQuart"
                },
                plugins: {
                    legend: { display: false }
                },
                scales: { 
                    y: { beginAtZero: true, grid: { color: "#555" } }, 
                    x: { grid: { color: "#333" } } 
                }
            }
        });
    }

    // Fetch and update charts
    function fetchAndUpdateChart(apiUrl, chartId, chartType, chartLabel, colors) {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                console.log(`✅ Data for ${chartLabel}:`, data);
                createChart(chartId, chartType, Object.keys(data), Object.values(data), chartLabel, colors);
            })
            .catch(error => console.error(`❌ Error fetching ${chartLabel}:`, error));
    }

    fetchAndUpdateChart("http://127.0.0.1:5000/get-trends", "donationTrendsChart", "line", "Monthly Donations ($)", "#FF5733");
    fetchAndUpdateChart("http://127.0.0.1:5000/get-age-groups", "ageTrendsChart", "bar", "Donations by Age", ["#FF5733", "#C70039", "#900C3F", "#581845"]);
    fetchAndUpdateChart("http://127.0.0.1:5000/get-gender-trends", "genderTrendsChart", "bar", "Donations by Gender", ["#E63946", "#F4A261", "#2A9D8F"]);
    fetchAndUpdateChart("http://127.0.0.1:5000/get-location-trends", "locationTrendsChart", "bar", "Donations by Location", ["#E76F51", "#F4A261", "#E9C46A", "#2A9D8F", "#264653"]);

    // Filters Section
    const genderSelect = document.getElementById("gender");
    const ageSelect = document.getElementById("age");
    const locationSelect = document.getElementById("location");
    const applyFiltersBtn = document.getElementById("applyFilters");
    let filteredChart;

    // Ensure elements exist before adding event listeners
    if (!genderSelect || !ageSelect || !locationSelect || !applyFiltersBtn) {
        console.error("❌ One or more filter elements are missing!");
        return;
    }

    // Load locations dynamically from Flask API
    fetch("http://127.0.0.1:5000/get-locations")
        .then(response => response.json())
        .then(data => {
            data.forEach(location => {
                const option = document.createElement("option");
                option.value = location;
                option.textContent = location;
                locationSelect.appendChild(option);
            });
        })
        .catch(error => console.error("❌ Error loading locations:", error));

    // Function to fetch and update chart based on filters
    function updateFilteredChart() {
        const gender = genderSelect.value;
        const age = ageSelect.value;
        const location = locationSelect.value;

        fetch(`http://127.0.0.1:5000/get-filtered-data?gender=${gender}&age=${age}&location=${location}`)
            .then(response => response.json())
            .then(data => {
                if (filteredChart) filteredChart.destroy(); // Clear previous chart

                const ctx = document.getElementById("filteredChart").getContext("2d");
                filteredChart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: Object.keys(data),
                        datasets: [{
                            label: "Donation Amount",
                            data: Object.values(data),
                            backgroundColor: "#ff6b6b",
                            borderColor: "#e44d4d",
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            })
            .catch(error => console.error("❌ Error fetching filtered data:", error));
    }

    // Event listener for Apply Filters button
    applyFiltersBtn.addEventListener("click", updateFilteredChart);
});
