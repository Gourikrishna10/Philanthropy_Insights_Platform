document.addEventListener("DOMContentLoaded", function() {
    fetch("http://localhost:5000/api/donation-summary")
    .then(response => response.json())
    .then(data => {
        let summaryDiv = document.getElementById("summary");
        summaryDiv.innerHTML = `
            <p><strong>Total Donations:</strong> $${data.total_donations}</p>
            <p><strong>Most Popular Cause:</strong> ${data.most_popular_cause}</p>
            <p><strong>Top Donor:</strong> ${data.top_donor} ($${data.top_donation_amount})</p>
        `;
    })
    .catch(error => console.error("Error fetching donation summary:", error));
});
