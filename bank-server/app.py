from flask import Flask, request, jsonify
import os

app = Flask(__name__)
BANK_NAME = os.environ.get("BANK_NAME", "UnknownBank")
BALANCE = 1000  # default balance

@app.route('/balance', methods=['GET'])
def balance():
    return jsonify({"bank": BANK_NAME, "balance": BALANCE})

@app.route('/receive', methods=['POST'])
def receive():
    global BALANCE
    data = request.json
    amount = data.get("amount", 0)
    BALANCE += amount
    return jsonify({"message": f"{BANK_NAME} received {amount}", "new_balance": BALANCE})

@app.route('/send', methods=['POST'])
def send():
    global BALANCE
    data = request.json
    amount = data.get("amount", 0)
    to_bank = data.get("to")
    if amount > BALANCE:
        return jsonify({"error": "Insufficient funds"}), 400

    # Call SWIFT messaging server
    import requests
    res = requests.post("http://swift:5000/transfer", json={
        "from": BANK_NAME,
        "to": to_bank,
        "amount": amount
    })

    if res.status_code == 200:
        BALANCE -= amount
        return jsonify({"message": f"Sent {amount} to {to_bank}", "new_balance": BALANCE})
    else:
        return jsonify({"error": "SWIFT transfer failed"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')
