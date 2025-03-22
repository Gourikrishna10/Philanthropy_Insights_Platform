document.addEventListener("DOMContentLoaded", () => {
    fetchInsights();
    fetchGenderData();
    fetchLocationData();
    fetchAgeData();
    fetchTrends();
});

// ✅ Fetch general insights
async function fetchInsights() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-insights");
        const data = await response.json();

        document.getElementById("totalDonations").textContent = `$${data.total_donations.toLocaleString()}`;
        document.getElementById("popularCause").textContent = data.most_popular_cause;
        document.getElementById("topDonor").textContent = data.top_donor;
    } catch (error) {
        console.error("❌ Error fetching insights:", error);
    }
}

// ✅ Fetch gender-wise donation data
async function fetchGenderData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-gender-donations");
        const data = await response.json();

        let text = "";
        for (const [gender, amount] of Object.entries(data)) {
            text += `<strong>${gender}:</strong> $${amount.toLocaleString()}<br>`;
        }
        document.getElementById("genderDonations").innerHTML = text;
    } catch (error) {
        console.error("❌ Error fetching gender data:", error);
    }
}

// ✅ Fetch location-wise donation data
async function fetchLocationData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-location-donations");
        const data = await response.json();

        let text = "";
        for (const [location, amount] of Object.entries(data).slice(0, 10)) {
            text += `<strong>${location}:</strong> $${amount.toLocaleString()}<br>`;
        }
        document.getElementById("locationDonations").innerHTML = text;
    } catch (error) {
        console.error("❌ Error fetching location data:", error);
    }
}

// ✅ Fetch age-wise donation data
async function fetchAgeData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-age-groups");
        const data = await response.json();

        let text = "";
        for (const [ageGroup, amount] of Object.entries(data)) {
            text += `<strong>${ageGroup}:</strong> $${amount.toLocaleString()}<br>`;
        }
        document.getElementById("ageDonations").innerHTML = text;
    } catch (error) {
        console.error("❌ Error fetching age data:", error);
    }
}

// ✅ Fetch monthly donation trends
async function fetchTrends() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-trends");
        const data = await response.json();

        let text = "";
        const sortedMonths = Object.keys(data).sort().slice(-6); // Last 6 months
        sortedMonths.forEach(month => {
            text += `<strong>${month}:</strong> $${data[month].toLocaleString()}<br>`;
        });

        document.getElementById("monthlyTrends").innerHTML = text;
    } catch (error) {
        console.error("❌ Error fetching trends:", error);
    }
}
