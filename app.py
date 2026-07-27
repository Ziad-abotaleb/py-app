import time
from flask import Flask, jsonify

app = Flask(__name__)

# In-memory stats (reset on restart)
stats = {
    "request_count": 0,
    "start_time": time.time(),
}


@app.before_request
def track_request():
    stats["request_count"] += 1


@app.route("/")
def home():
    return jsonify({
        "message": "API is running",
        "uptime_seconds": round(time.time() - stats["start_time"], 2)
    })


@app.route("/health")
def health():
    """Used by the monitoring script and load balancer/platform health checks."""
    return jsonify({"status": "healthy"}), 200


@app.route("/metrics")
def metrics():
    """Used by the dashboard to show request count and uptime."""
    return jsonify({
        "request_count": stats["request_count"],
        "uptime_seconds": round(time.time() - stats["start_time"], 2)
    })


if __name__ == "__main__":
    # 0.0.0.0 so it's reachable inside the container
    app.run(host="0.0.0.0", port=5000)
