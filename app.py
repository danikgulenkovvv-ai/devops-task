import os
import redis
from flask import Flask, request

app = Flask(__name__)
cache = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)
LOG_FILE = "/app/logs/events.log"

@app.route("/")
def index():
    msg = request.args.get("msg", "ping")
    count = cache.incr("events_count")
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"Event #{count}: {msg}\n")
        
    with open(LOG_FILE, "r") as f:
        history = f.read().replace("\n", "<br>")
        
    return f"<h2>Всего событий: {count}</h2><hr>{history}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
