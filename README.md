# LatencyBeat: Real-Time Latency Monitoring App

LatencyBeat is a **containerized full-stack application** designed to monitor network latency in real-time. Due to a distributed architecture, the system provides **instant data visualization** through **WebSockets**, leveraging a robust asynchronous pipeline.

## Architecture & Pipeline
LatencyBeat was built to demonstrate a **production-grade data pipeline**, ensuring the main web thread remains non-blocking while handling continuous data streams.

- **Producer**: A Celery Beat scheduler triggers a heartbeat (ping) task every 5 seconds.
- **Worker**: Celery Workers process the task, generating simulated latency metrics and performing database I/O.
- **Message Broker**: Redis acts as the middleman, facilitating communication between the Django application and the Celery workers.
- **Real-Time Delivery**: Django Channels (ASGI) pushes data to the frontend via WebSockets.
- **Data Persistence**: PostgreSQL handles history storage with time series indexing for greater visualization.
- **Orchestration**: The entire environment is containerized using Docker and Docker Compose.

## Key Features
- **Real-time data streaming** using live Chart.js visualization.
- **On-load history data priming** ensures charts are populated with the last 20 data points (latency ms) immediately upon page entry.
- **Automated heartbeat** (a background service) simulates real-world latency metrics across all registered devices.
- **Modern, responsive UI** improves accessibility and readability (clean typography, high-contrast, limited color palettes are implemented using Tailwind and Bootstrap).
- **Full CRUD Logic** allows dynamically add and monitor new network nodes with WebSocket rooms.

## Tech Stack
- **Frontend:** Tailwind CSS, Bootstrap 5, Chart.js, JavaScript
- **Backend:** Python, Django
- **Real-Time:** Django Channels (WebSockets)
- **Database:** PostgreSQL
- **Task Queue:** Celery, Redis
- **DevOps:** Docker, Docker Compose

## Installation & Local Development
This project is fully containerized. To run the app, ensure you have Docker Desktop installed:

1. Clone the repository
``` git clone https://github.com/ekaterinaekaterinicheva/latencybeat-monitoring-dashboard.git ```

2. Configure environment
Create a ```.env``` file in the root folder (see ```.env.example```).

3. Run ```docker-compose up --build``` to build the images for each service.

4. Initialize Database
Run ```docker-compose exec web python manage.py migrate```

5. Access the Dashboard via ```http://localhost:8000```.

## Engineering Insights

During the development of LatencyBeat, I focused on solving several distributed system challenges. Precisely, I:

- implemented get_or_create logic in the task worker to prevent database duplication during concurrent heartbeats,

- used json_script to securely pass history data from Python to the client-side, which reduced initial page load latency, and

- configured a Docker network to allow seamless communication between the Web, Redis, and Postgres services.
