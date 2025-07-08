from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["github_webhooks"]
collection = db["events"]

@app.route("/", methods=["GET"])
def home():
    return "GitHub Webhook Listener is running."


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "push":
        if not data.get("head_commit"):
            return jsonify({"message": "No head commit data"}), 400
        author = data["pusher"]["name"]
        to_branch = data["ref"].split("/")[-1]
        request_id = data["head_commit"]["id"]
        timestamp = datetime.strptime(data["head_commit"]["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        event_data = {
            "request_id": request_id,
            "author": author,
            "action": "PUSH",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp.isoformat()
        }

    elif event_type == "pull_request":
        pr = data.get("pull_request")
        if not pr:
            return jsonify({"message": "No pull_request data"}), 400

        author = pr["user"]["login"]
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]
        request_id = str(pr["number"])
        merged = pr.get("merged", False)

        timestamp_raw = pr["merged_at"] if merged else pr["created_at"]
        if timestamp_raw is None:
            return jsonify({"message": "No valid timestamp"}), 400
        timestamp = datetime.strptime(timestamp_raw, "%Y-%m-%dT%H:%M:%SZ")

        action_type = "MERGE" if merged else "PULL_REQUEST"

        event_data = {
            "request_id": request_id,
            "author": author,
            "action": action_type,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp.isoformat()
        }

    else:
        return jsonify({"message": "Unsupported event"}), 400

    collection.insert_one(event_data)
    return jsonify({"message": "Event received"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event["_id"] = str(event["_id"])
    return jsonify(events), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
