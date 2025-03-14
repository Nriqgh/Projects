from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Slack Webhook URL
SLACK_WEBHOOK_URL = "test_webhook" #webhook.

@app.route("/notion-webhook", methods=["POST"])
def notion_webhook():
    print("Received request from Notion")  # Debugging line
    print(request.headers)  # Print headers for debugging
    print(request.json)  # Print full JSON payload

    try:
        data = request.json  # Get Notion payload

        # Check if Notion sent a valid payload
        if not data or "data" not in data:
            return jsonify({"error": "Invalid request"}), 400

        # Extract policy name
        policy_name = data["data"]["properties"]["Policy Name"]["title"][0]["text"]["content"]

        # Slack message format
        slack_message = {
            "text": f"📢 New Policy Acknowledgment: *{policy_name}*\nView Policy: {data['data']['url']}"
        }

        # Send the message to Slack
        response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Sent to Slack"}), 200
        else:
            return jsonify({"error": "Failed to send to Slack", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # Change to 5001

