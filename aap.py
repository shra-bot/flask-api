import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS properly
 
app = Flask(__name__)
CORS(app)  # Enable CORS for the app
 
# Replace with your actual Azure OpenAI details
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure your key is stored securely
OPENAI_ENDPOINT = "https://chatbbgarage.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-09-01"
 
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
 
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400
 
        # Send request to Azure OpenAI
        response = requests.post(
            OPENAI_ENDPOINT,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "api-key": OPENAI_API_KEY,  # Add this line to authenticate
                "Content-Type": "application/json"
            },
            json={
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 100
            }
        )
 
        if response.status_code != 200:
            return jsonify({"error": "Failed to get response from OpenAI", "details": response.text}), response.status_code
 
        return jsonify(response.json())
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == "__main__":
    app.run(port=5000)
