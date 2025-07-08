# bank_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated in-memory bank accounts
accounts = {
    "vincent": {"balance": 1000},
    "alice": {"balance": 750},
    "bob": {"balance": 300}
}

@app.route("/accounts", methods=["GET"])
def get_accounts():
    return jsonify(accounts)

@app.route("/transfer", methods=["POST"])
def transfer():
    data = request.get_json()
    sender = data["sender"]
    recipient = data["recipient"]
    amount = data["amount"]

    if sender not in accounts or recipient not in accounts:
        return jsonify({"error": "Invalid account name"}), 400

    if accounts[sender]["balance"] < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    accounts[sender]["balance"] -= amount
    accounts[recipient]["balance"] += amount

    return jsonify({
        "message": f"Transferred ${amount} from {sender} to {recipient}",
        "accounts": accounts
    })

if __name__ == "__main__":
    app.run(debug=True)

