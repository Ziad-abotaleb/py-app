# Reliability Engineering — Task 1

## What's included
- `app.py` / `requirements.txt` / `Dockerfile` — Flask API with `/health` and `/metrics`
- `monitor.py` — checks `/health` every 30s, logs to `monitor_log.jsonl`
- `dashboard/index.html` — live status dashboard (status, response time, request count)

## Run locally
```bash
docker build -t reliability-app .
docker run -p 5000:5000 reliability-app
```
Visit `http://localhost:5000/health` — should return `{"status": "healthy"}`.

## Deploy to ghaymah.systems
Ghaymah's platform-specific upload steps (CLI or web console) aren't something
I could verify — check their docs/dashboard for the exact push/deploy command.
General flow for any container platform:
1. Build the image: `docker build -t reliability-app .`
2. Push it to the registry ghaymah gives you (usually `docker login` + `docker push`,
   or a `git push` if they build from your repo).
3. Point the platform's health check at `/health`.
4. Note the public URL it gives you — you'll need it for the monitor and dashboard.

## Run the monitor
```bash
python monitor.py https://your-app-url.ghaymah.systems
```
Prints a status line every 30s and appends JSON records to `monitor_log.jsonl`.

## Use the dashboard
Open `dashboard/index.html` in a browser, paste your deployed app's URL into the
field, click **Connect**. It polls `/health` and `/metrics` every 5s.

⚠️ If the dashboard is opened as a local file and the API is on another domain,
you'll hit CORS errors. Add this to `app.py` if needed:
```python
from flask_cors import CORS
CORS(app)
```
(and add `flask-cors` to `requirements.txt`)
