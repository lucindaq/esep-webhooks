from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
slack_url = os.getenv("SLACK_URL")
if not slack_url:
    raise ValueError("SLACK_URL environment variable not set")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data received"}), 400

    if 'issue' in data:
        issue_url = data['issue']['html_url']
        post_to_slack(issue_url)

    return jsonify({"message": "Webhook received"}), 200

def post_to_slack(issue_url):
    payload = {"text": f"New issue created: {issue_url}"}
    try:
        response = requests.post(slack_url, json=payload)
        if response.status_code == 200:
            print("Message posted to Slack successfully")
        else:
            print(f"Failed to post to Slack: {response.status_code}")
    except Exception as e:
        print(f"Error posting to Slack: {e}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
