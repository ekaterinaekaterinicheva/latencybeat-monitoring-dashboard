// Initialize the Chart
const ctx = document.getElementById('dashboard-chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Timestamps or indices go here
        datasets: [{
            label: 'Device Latency (ms)',
            data: [], // Real-time values go here
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            fill: true,
            tension: 0.4 // Makes the line curvy
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Establish WebSocket connection
// dashboardSlug is passed from the HTML template script tag
const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}/`);

socket.onmessage = function (e) {
    // Parse the data sent from Django Consumers
    const data = JSON.parse(e.data);
    console.log('Data received:', data);

    // Update chart logic
    // The server is assumed to send an object like the following: { "value": 10, "time": "11:00" }
    const newValue = data.value;
    const newLabel = data.time || new Date().toLocaleTimeString(); // Use provided time or fallback to current time

    // Add data to the chart arrays
    chart.data.labels.push(newLabel);
    chart.data.datasets[0].data.push(newValue);

    // Keep only the last 15 points so that the chart doesn't get too messy
    if (chart.data.labels.length > 15) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }

    // Update the chart
    chart.update();
};

// Handle sending data from the UI to the server
const inputField = document.getElementById('data-input');
const sendBtn = document.getElementById('submit-btn');

sendBtn.onclick = function () {
    const value = inputField.value;
    if (value) {
        socket.send(JSON.stringify({
            'message': value,
        }));
        inputField.value = ''; // Clear input after sending
    }
};

// Standard Connection Logging
socket.onopen = (e) => console.log('WebSocket connected');
socket.onerror = (e) => console.error('WebSocket error:', e);
socket.onclose = (e) => console.log('WebSocket closed');