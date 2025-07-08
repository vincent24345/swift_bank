import mysql.connector
from mysql.connector import Error

# Database configuration - Update these values
DB_CONFIG = {
    'host': 'localhost',
    'user': 'vincent',         # Replace with your MySQL username
    'password': 'Vincent24345!', # Replace with your MySQL password
    'database': 'BankDatabase'
}

def setup_database():
    """Create and initialize the bank database with sample accounts"""
    try:
        # First connect without specifying database
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Drop database if it exists
            cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
            print(f"Dropped existing database: {DB_CONFIG['database']}")
            
            # Create new database
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"Created new database: {DB_CONFIG['database']}")
            
            # Switch to the bank_heist database
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Create accounts table
            cursor.execute('''
            CREATE TABLE accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                balance DECIMAL(20, 2) NOT NULL,
                currency VARCHAR(10) NOT NULL
            )
            ''')
            print("Created accounts table")
            
            # Create transactions table
            cursor.execute('''
            CREATE TABLE transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender VARCHAR(255) NOT NULL,
                recipient VARCHAR(255) NOT NULL,
                amount DECIMAL(20, 2) NOT NULL,
                currency VARCHAR(10) NOT NULL,
                note TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            print("Created transactions table")
            
            # Insert sample accounts for the Bangladesh Bank heist simulation
            sample_accounts = [
                ('BangladeshBank', 1000000000, 'USD'),    # Bangladesh Bank with initial balance
                ('ShadyAccountManila', 500000, 'USD'),    # The receiver in Manila
                ('FederalReserveNY', 5000000000, 'USD'),  # Fed account where the money was held
                ('SWIFT_GATEWAY', 0, 'USD')               # SWIFT system account for tracking
            ]
            
            # Insert accounts
            insert_query = "INSERT INTO accounts (name, balance, currency) VALUES (%s, %s, %s)"
            cursor.executemany(insert_query, sample_accounts)
            conn.commit()
            
            print("Sample accounts created:")
            for account in sample_accounts:
                print(f"  - {account[0]}: {account[1]} {account[2]}")
            
            cursor.close()
            conn.close()
            print(f"\nDatabase setup completed successfully!")
            
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Setting up MySQL database for Bangladesh Bank Heist simulation...")
    setup_database()
    print("\nRun your Flask application to start using the database!")
    print("\nNote: Make sure MySQL server is running and credentials are correct in the script.")