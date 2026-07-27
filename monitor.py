"""
Simple uptime monitor.
Pings the app's /health endpoint every 30 seconds, prints and logs the result.

Usage:
    python monitor.py https://your-app-url.ghaymah.systems
"""

import sys
import time
import json
from datetime import datetime, timezone
import urllib.request
import urllib.error

CHECK_INTERVAL_SECONDS = 30
LOG_FILE = "monitor_log.jsonl"


def check_health(base_url: str) -> dict:
    url = base_url.rstrip("/") + "/health"
    start = time.time()
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            status = "UP" if response.status == 200 else "DEGRADED"
            return {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "http_code": response.status,
                "response_time_ms": elapsed_ms,
            }
    except (urllib.error.URLError, TimeoutError) as e:
        elapsed_ms = round((time.time() - start) * 1000, 2)
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "DOWN",
            "http_code": None,
            "response_time_ms": elapsed_ms,
            "error": str(e),
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <app_base_url>")
        sys.exit(1)

    base_url = sys.argv[1]
    print(f"Monitoring {base_url}/health every {CHECK_INTERVAL_SECONDS}s. Ctrl+C to stop.")

    while True:
        result = check_health(base_url)
        print(f"[{result['timestamp']}] {result['status']} "
              f"({result['response_time_ms']} ms)")

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(result) + "\n")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
