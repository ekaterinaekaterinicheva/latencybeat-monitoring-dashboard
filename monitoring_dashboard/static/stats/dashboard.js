console.log("Hello, World!!");

const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}/`);
console.log(socket);

socket.onmessage = function (e) {
    console.log('Server: ' + e.data);
};

socket.onopen = function (e) {
    console.log('WebSocket connection opened');
    socket.send(JSON.stringify({
        'message': 'Hello from client!',
    }));
};

socket.onerror = function (e) {
    console.error('WebSocket error:', e);
};

socket.onclose = function (e) {
    console.log('WebSocket connection closed');
};