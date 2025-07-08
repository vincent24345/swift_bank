import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5001"

def format_currency(amount):
    return "${:,.2f}".format(float(amount))

def list_accounts():
    res = requests.get(f"{BASE_URL}/accounts")
    if res.ok:
        print("\n📄 Accounts & Balances:")
        for acc in res.json():
            print(f"  🏦 {acc['name']}: {format_currency(acc['balance'])} {acc['currency']}")
    else:
        print("❌ Error fetching accounts.")

def transfer_funds():
    print("\n🚨 Initiating SWIFT Transfer:")
    sender = input("  Sender: ")
    recipient = input("  Recipient: ")
    amount = float(input("  Amount: "))
    note = input("  Note (optional): ")

    payload = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "currency": "USD",
        "note": note or "Suspicious transfer"
    }

    try:
        res = requests.post(f"{BASE_URL}/transfer", json=payload)
        if res.ok:
            print("✅ Transfer successful.")
        else:
            try:
                error_message = res.json().get("error", "Unknown error")
            except json.JSONDecodeError:
                error_message = f"Non-JSON error (HTTP {res.status_code}): {res.text}"
            print("❌ Transfer failed:", error_message)
    except requests.RequestException as e:
        print("❌ Network error during transfer:", str(e))

def check_balance():
    account = input("🔍 Account to check: ")
    res = requests.get(f"{BASE_URL}/balance/{account}")
    if res.ok:
        data = res.json()
        print(f"  💰 {data['account']}: {format_currency(data['balance'])} {data['currency']}")
    else:
        print("❌ Error fetching balance.")

def view_transactions():
    res = requests.get(f"{BASE_URL}/transactions")
    if res.ok:
        print("\n📜 Recent Transactions:")
        for tx in res.json()[:10]:
            print(f"  {tx['timestamp']}: {tx['sender']} → {tx['recipient']} :: {format_currency(tx['amount'])}")
    else:
        print("❌ Error fetching transactions.")

def check_firewall_status():
    print("🛡️ Firewall threshold is $50,000,000 USD.")

def view_firewall_logs():
    res = requests.get(f"{BASE_URL}/firewall-alerts")
    if res.ok:
        alerts = res.json().get("alerts", [])
        if alerts:
            print("🚨 Firewall Alerts:")
            for alert in alerts:
                print("  -", alert)
        else:
            print("✅ No alerts. Firewall has not blocked anything.")
    else:
        print("❌ Failed to retrieve firewall logs.")

def hack_gateway():
    res = requests.post(f"{BASE_URL}/hack", json={"target": "swift_gateway"})
    if res.ok:
        print("💥 SWIFT Gateway hacked!")
    else:
        print("❌ Hacking failed:", res.text)

def test_swift_validation():
    print("\n✅ SWIFT VALIDATION TEST")
    payload = {
        "amount": 10000,
        "currency": "USD",
        "recipient": "FederalReserveNY"
    }
    try:
        res = requests.post(f"{BASE_URL}/swift_gateway", json=payload)
        if res.ok:
            print("🟢", res.json().get("status", "Passed"))
        else:
            print("🔴", res.json().get("error", "Failed"))
    except requests.RequestException as e:
        print("❌ SWIFT test failed:", str(e))


def help_menu():
    print("""
Choose an option:
1. 🧾 View All Accounts
2. 💸 Execute Fake SWIFT Transfer
3. 📑 View Transaction History
4. 💳 Check Specific Account Balance
5. 🧱 View Firewall Alerts
6. 🕵️ Hack SWIFT Gateway
7. ✅ SWIFT Validation Test
8. 🛑 Exit
        """)


def interactive_menu():
    print("=== 🧨 Bangladesh Bank Heist Terminal ===")
    help_menu()
    while True:
        choice = input("Enter command (1-8): ").strip()
        if choice == "1":
            list_accounts()
        elif choice == "2":
            transfer_funds()
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            view_firewall_logs()
        elif choice == "6":
            hack_gateway()
        elif choice == "7":
            test_swift_validation()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("⚠️ Invalid choice, try again.")


if __name__ == "__main__":
    interactive_menu()
