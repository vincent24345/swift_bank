from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    to = data['to']
    amount = data['amount']

    # Simulate SWIFT routing to receiving bank
    host_map = {
        "Bank1": "http://bank1:5000/receive",
        "Bank2": "http://bank2:5000/receive"
    }

    if to not in host_map:
        return jsonify({"error": "Invalid recipient bank"}), 400

    res = requests.post(host_map[to], json={"amount": amount})
    return res.content, res.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0')
