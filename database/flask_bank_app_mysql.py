from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
import random
from datetime import datetime


app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'vincent',  # Replace with your MySQL username
    'password': 'Vincent24345!',  # Replace with your MySQL password
    'database': 'BankDatabase'
}
# Firewall Simulation: Block high-value suspicious transactions
is_gateway_hacked = False
FIREWALL_THRESHOLD = 50000000  # Example: $50 million
FIREWALL_ALERT_LOG = []  # Store logs of blocked transactions

def init_db():
    """Initialize the database with tables and sample data"""
    # First, create the database if it doesn't exist
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            print(f"Database {DB_CONFIG['database']} created or already exists")
            
            # Switch to the bank_heist database
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Create accounts table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                balance DECIMAL(20, 2) NOT NULL,
                currency VARCHAR(10) NOT NULL
            )
            ''')
            
            # Create transactions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender VARCHAR(255) NOT NULL,
                recipient VARCHAR(255) NOT NULL,
                amount DECIMAL(20, 2) NOT NULL,
                currency VARCHAR(10) NOT NULL,
                note TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Check if accounts already exist to avoid duplicates
            cursor.execute("SELECT COUNT(*) FROM accounts")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert sample accounts for the Bangladesh Bank heist simulation
                sample_accounts = [
                    ('BangladeshBank', 1000000000, 'USD'),
                    ('ShadyAccountManila', 500000, 'USD'),
                    ('FederalReserveNY', 5000000000, 'USD'),
                    ('SWIFT_GATEWAY', 0, 'USD')
                ]
                
                # Insert accounts
                insert_query = "INSERT INTO accounts (name, balance, currency) VALUES (%s, %s, %s)"
                cursor.executemany(insert_query, sample_accounts)
                conn.commit()
                print("Sample accounts created")
            else:
                print("Accounts already exist, skipping sample data creation")
            
            conn.close()
            
    except Error as e:
        print(f"Error: {e}")

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/accounts', methods=['GET'])
def list_accounts():
    """List all accounts and their balances"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT name, balance, currency FROM accounts')
        accounts = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(accounts)
    except Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/transfer', methods=['POST'])
def transfer():
    # Simulate 10% chance of SWIFT Gateway failure
    if random.random() < 0.1:
        return jsonify({"error": "💣 SWIFT Gateway Down"}), 503

    """Process a transfer between accounts"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['sender', 'recipient', 'amount', 'currency']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    sender = data['sender']
    recipient = data['recipient']
    amount = float(data['amount'])
    currency = data['currency']
    note = data.get('note', '')
    

    # ✅ Simulate SQL injection detection 
    if "'; DROP" in sender.upper() or "--" in sender:
        return jsonify({"error": "Simulated SQL injection attempt detected and blocked"}), 400
    
        # Simulated firewall behavior
    if amount > FIREWALL_THRESHOLD:
        alert_msg = f"🚨 FIREWALL ALERT: Transfer of {amount} {currency} from {sender} to {recipient} BLOCKED"
        FIREWALL_ALERT_LOG.append(f"{datetime.now().isoformat()} - {alert_msg}")  #  Timestamped log
        print(alert_msg)
        return jsonify({"error": "Firewall blocked this high-value transaction due to suspicious activity."}), 403

    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(buffered=True)
        
        # Check if accounts exist
        cursor.execute('SELECT name FROM accounts WHERE name IN (%s, %s)', (sender, recipient))
        existing_accounts = [row[0] for row in cursor.fetchall()]
        
        if len(existing_accounts) < 2:
            # One or both accounts don't exist
            if sender not in existing_accounts:
                conn.close()
                return jsonify({"error": f"Invalid account name: {sender}"}), 400
                
            if recipient not in existing_accounts:
                conn.close()
                return jsonify({"error": f"Invalid account name: {recipient}"}), 400
        
        # Check if sender has sufficient balance
        cursor.execute('SELECT balance FROM accounts WHERE name = %s', (sender,))
        sender_balance = cursor.fetchone()[0]
        
        if float(sender_balance) < amount:
            conn.close()
            return jsonify({"error": "Insufficient funds"}), 400
        
        # Update sender balance
        cursor.execute('UPDATE accounts SET balance = balance - %s WHERE name = %s', (amount, sender))
        
        # Update recipient balance
        cursor.execute('UPDATE accounts SET balance = balance + %s WHERE name = %s', (amount, recipient))
        
        # Record the transaction
        cursor.execute('''
        INSERT INTO transactions (sender, recipient, amount, currency, note)
        VALUES (%s, %s, %s, %s, %s)
        ''', (sender, recipient, amount, currency, note))
        
        conn.commit()
        
        # Get updated balances
        cursor.execute('SELECT name, balance FROM accounts WHERE name IN (%s, %s)', (sender, recipient))
        updated_balances = {}
        for name, balance in cursor:
            updated_balances[name] = float(balance)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": f"Transferred {amount} {currency} from {sender} to {recipient}",
            "updated_balances": updated_balances
        })
    
    except Error as e:
        if conn.is_connected():
            conn.rollback()
            conn.close()
        return jsonify({"error": str(e)}), 500
    
    

@app.route('/balance/<account_name>', methods=['GET'])
def get_balance(account_name):
    """Get the balance for a specific account"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT balance, currency FROM accounts WHERE name = %s', (account_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result:
            return jsonify({"error": "Account not found"}), 404
        
        return jsonify({
            "account": account_name,
            "balance": float(result[0]),
            "currency": result[1]
        })
    except Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Get list of all transactions"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
        transactions = cursor.fetchall()
        
        # Convert Decimal objects to float for JSON serialization
        for transaction in transactions:
            transaction['amount'] = float(transaction['amount'])
            # Convert datetime to string
            transaction['timestamp'] = transaction['timestamp'].isoformat()
            
        cursor.close()
        conn.close()
        return jsonify(transactions)
    except Error as e:
        conn.close()
        return jsonify({"error": str(e)}), 500
    
@app.route('/firewall_alerts', methods=['GET'])
def get_firewall_alerts():
    """Return a list of blocked transactions flagged by the firewall"""
    return jsonify({"logs": FIREWALL_ALERT_LOG})


@app.route('/firewall_status', methods=['GET'])
def firewall_status():
    """Return firewall activation status and threshold"""
    return jsonify({
        "active": True,
        "threshold": FIREWALL_THRESHOLD
    })


@app.route('/swift_gateway', methods=['POST'])
def swift_gateway():
    global is_gateway_hacked

    if is_gateway_hacked:
        return jsonify({"status": "Bypassed SWIFT validation - gateway compromised"}), 200

    data = request.get_json()
    amount = float(data.get("amount", 0))
    currency = data.get("currency", "USD")
    recipient = data.get("recipient", "")

    if currency != "USD":
        return jsonify({"error": "❌ Currency mismatch"}), 400
    if recipient.lower() in ["shadyaccountmanila", "fakefoundation"]:
        return jsonify({"error": "❌ Recipient failed validation"}), 403
    if datetime.now().weekday() >= 5:
        return jsonify({"error": "❌ Transfers not allowed on weekends"}), 403
    if amount > FIREWALL_THRESHOLD:
        FIREWALL_ALERT_LOG.append(data)
        return jsonify({"error": "🚨 Transfer blocked by SWIFT firewall"}), 403

    return jsonify({"status": "✅ SWIFT check passed"}), 200


@app.route('/hack', methods=['POST'])
def hack():
    global is_gateway_hacked
    data = request.get_json()
    if data.get("target") == "swift_gateway":
        is_gateway_hacked = True
        return jsonify({"status": "SWIFT gateway hacked!"})
    return jsonify({"error": "Invalid target"}), 400

@app.route('/reset_gateway', methods=['POST'])
def reset_gateway():
    global is_gateway_hacked
    is_gateway_hacked = False
    return jsonify({"status": "SWIFT gateway reset to secure mode."})

# Initialize DB and run app
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change port from 5000 to 5001