from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/alert", methods=["POST"])
def send_alert():
    data = request.get_json()
    avg_mood = data.get("avgMood", "N/A")

    message = {
        "content": f"⚠️ **Mood Alert**: Team morale is low!\nAverage mood is {avg_mood}"
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        if response.status_code == 204:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failed", "code": response.status_code}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
