import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:5001"  # Changed from 5000 to 5001
TOTAL_HEIST_AMOUNT = 951000000  # ~$951 million attempted in the actual heist
TRANSACTION_AMOUNTS = [
    81000000,  # First successful transfer
    20000000,  # Second successful transfer
    30000000,  # Third successful transfer
    150000000, # Fourth successful transfer
    30000000,  # Fifth transfer attempt
    150000000  # Sixth transfer attempt
]

def format_currency(amount):
    """Format amount as currency"""
    return "${:,.2f}".format(float(amount))

def check_bank_balances():
    """Check all account balances before starting"""
    response = requests.get(f"{BASE_URL}/accounts")
    if response.status_code == 200:
        print("Current account balances:")
        accounts = response.json()
        for account in accounts:
            print(f"  {account['name']}: {format_currency(account['balance'])} {account['currency']}")
    else:
        print(f"Error fetching accounts: {response.text}")
    print("\n" + "-"*50 + "\n")

def execute_transfer(sender, recipient, amount, currency="USD", note="Project funding"):
    """Execute a single transfer between accounts"""
    payload = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "currency": currency,
        "note": note
    }
    
    print(f"Attempting transfer: {format_currency(amount)} {currency}")
    print(f"From: {sender}")
    print(f"To: {recipient}")
    print(f"Note: {note}")
    
    # Add timestamp to simulate real transaction records
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Timestamp: {timestamp}")
    
    response = requests.post(
        f"{BASE_URL}/transfer",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("TRANSFER SUCCESSFUL")
        if "updated_balances" in result:
            for account, balance in result["updated_balances"].items():
                print(f"  {account} new balance: {format_currency(balance)} {currency}")
    else:
        print(f"TRANSFER FAILED: {response.json().get('error', 'Unknown error')}")
    
    print("\n" + "-"*50 + "\n")
    
    return response.status_code == 200

def simulate_command_interface():
    print("Welcome to the 💣 Heist Terminal 💻")
    print("Type `help` to see available commands.")

    while True:
        cmd = input(">> ").strip().lower()

        if cmd.startswith("hack swift_gateway"):
            requests.post(f"{BASE_URL}/hack", json={"target": "swift_gateway"})
            print("💥 Hacked the SWIFT gateway!")

        elif cmd.startswith("spoof"):
            print("🔄 Spoofing sender identity...")

        elif cmd == "transfer":
            try:
                amount = float(input("Enter amount to transfer: "))
                sender = input("Sender account name: ")
                recipient = input("Recipient account name: ")
                note = input("Transaction note: ")
                payload = {
                    "sender": sender,
                    "recipient": recipient,
                    "amount": amount,
                    "currency": "USD",
                    "note": note
                }
                response = requests.post(f"{BASE_URL}/transfer", json=payload)
                print(f"✅ Status: {response.status_code}")
                print(response.json())
            except Exception as e:
                print(f"❌ Transfer failed: {e}")

        elif cmd.startswith("balance"):
            account = cmd.split(" ")[1] if len(cmd.split()) > 1 else input("Account name: ")
            response = requests.get(f"{BASE_URL}/balance/{account}")
            if response.status_code == 200:
                data = response.json()
                print(f"{data['account']} balance: ${data['balance']:.2f} {data['currency']}")
            else:
                print("❌ Error:", response.json().get("error", "Unknown error"))

        elif cmd == "firewall status":
            response = requests.get(f"{BASE_URL}/firewall_status")
            if response.status_code == 200:
                status = response.json()
                print("🛡️ Firewall is ACTIVE" if status["active"] else "🛡️ Firewall is INACTIVE")
                print(f"Threshold: ${status['threshold']}")
            else:
                print("❌ Failed to get firewall status")

        elif cmd == "alert log":
            response = requests.get(f"{BASE_URL}/firewall_alerts")
            if response.status_code == 200:
                logs = response.json().get("logs", [])
                if not logs:
                    print("📭 No alerts logged.")
                else:
                    print("⚠️ Firewall Alerts:")
                    for alert in logs:
                        print(f" - {alert}")
            else:
                print("❌ Failed to get alert log")

        elif cmd == "log":
            response = requests.get(f"{BASE_URL}/transactions")
            for tx in response.json()[:5]:
                print(f"{tx['timestamp']} {tx['sender']} ➡️ {tx['recipient']} (${tx['amount']})")

        elif cmd == "history":
            response = requests.get(f"{BASE_URL}/transactions")
            if response.status_code == 200:
                txs = response.json()
                print(f"📜 Transaction history ({len(txs)} total):")
                for tx in txs:
                    print(f"{tx['timestamp']} {tx['sender']} ➡️ {tx['recipient']} ${tx['amount']:.2f}")
            else:
                print("❌ Failed to retrieve transactions")

        elif cmd == "help":
            print("""
Available commands:
  hack swift_gateway       - Simulate hacking the SWIFT gateway
  spoof                    - Simulate sender identity spoofing
  transfer                 - Prompt to perform a transfer via the /transfer API
  balance <account>        - Check account balance via /balance/<account>
  firewall status          - Check if firewall is active and its threshold
  alert log                - View blocked transaction alert logs
  log                      - View the latest 5 transactions
  history                  - View full transaction history
  help                     - Show this command list
  exit                     - Exit the terminal
""")

        elif cmd == "exit":
            print("👋 Goodbye.")
            break

        else:
            print("❌ Unknown command. Type `help` to see options.")



def simulate_bangladesh_heist():
    """Simulate the Bangladesh Bank heist"""
    print("=" * 60)
    print("=== BANGLADESH BANK HEIST SIMULATION - MYSQL VERSION ===")
    print("=" * 60)
    print("\nStarting simulation at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Check initial balances
    print("\n[INITIAL STATE]")
    check_bank_balances()
    
    # In the real heist, hackers got access to SWIFT credentials
    print("[STAGE 1] Initiating fraudulent SWIFT transfers\n")
    
    successful_transfers = 0
    total_stolen = 0
    
    # Simulate the transfer attempts
    for i, amount in enumerate(TRANSACTION_AMOUNTS):
        print(f"[TRANSFER ATTEMPT #{i+1}]")
        
        # In the real heist, the hackers used different recipient names
        # For simplicity, we're using just one recipient account here
        success = execute_transfer(
            "BangladeshBank", 
            "ShadyAccountManila", 
            amount,
            note=f"Project funding - transfer {i+1}"
        )
        
        if success:
            successful_transfers += 1
            total_stolen += amount
        
        # Add delay between transfers
        if i < len(TRANSACTION_AMOUNTS) - 1:
            print(f"Waiting 3 seconds before next transfer...\n")
            time.sleep(3)
    
    # Summary
    print("=" * 60)
    print("=== HEIST SIMULATION SUMMARY ===")
    print("=" * 60)
    print(f"Total transfer attempts: {len(TRANSACTION_AMOUNTS)}")
    print(f"Successful transfers: {successful_transfers}")
    print(f"Failed transfers: {len(TRANSACTION_AMOUNTS) - successful_transfers}")
    print(f"Total amount stolen: {format_currency(total_stolen)} USD")
    print(f"Success rate: {(successful_transfers/len(TRANSACTION_AMOUNTS))*100:.1f}%")
    
    # Check final balances
    print("\n[FINAL STATE]")
    check_bank_balances()
    
    # View transaction history
    print("[TRANSACTION HISTORY]")
    response = requests.get(f"{BASE_URL}/transactions")
    if response.status_code == 200:
        transactions = response.json()
        print(f"All transactions recorded: {len(transactions)}")
        for tx in transactions[:5]:  # Show only the first 5 for brevity
            print(f"  {tx['timestamp']}: {tx['sender']} -> {tx['recipient']}: {format_currency(tx['amount'])} {tx['currency']}")
        
        if len(transactions) > 5:
            print(f"  ... and {len(transactions) - 5} more transactions")
    
    # Historical context
    print("\n[HISTORICAL CONTEXT]")
    print("In the actual 2016 Bangladesh Bank heist:")
    print("- Hackers attempted to steal ~$951 million")
    print("- Only $81 million was successfully transferred due to:")
    print("  * A spelling error ('fandation' instead of 'foundation') raised suspicions")
    print("  * The unusual number of transfers to private entities raised alerts")
    print("  * A correspondent bank questioned some of the transfers")
    print("- The Federal Reserve Bank of New York blocked 30 transactions worth ~$850 million")

    

if __name__ == "__main__":
  if __name__ == "__main__":
    print("Welcome to the Bangladesh Bank Heist Terminal\n")
    print("Choose an option:")
    print("1. Run full heist simulation")
    print("2. Enter interactive terminal (SWIFT-like interface)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        simulate_bangladesh_heist()
    elif choice == "2":
        simulate_command_interface()
    else:
        print("Invalid choice. Exiting.")
