"""
Main application to demonstrate CRUD operations for the ERD-based system.
Edit the database path for your SQLite database.
"""
import sqlite3

DB_PATH = 'test.db'

def add_client():
    name = input('Enter client name: ')
    phone = input('Enter client phone: ')
    address = input('Enter client address: ')
    payment_info = input('Enter payment info: ')
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS CLIENT (
            CLIENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            PHONE TEXT NOT NULL,
            ADDRESS TEXT NOT NULL,
            PAYMENT_INFO TEXT
        )''')
        cursor.execute('INSERT INTO CLIENT (NAME, PHONE, ADDRESS, PAYMENT_INFO) VALUES (?, ?, ?, ?)',
                       (name, phone, address, payment_info))
        conn.commit()
        print('Client added.')

def list_clients():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS CLIENT (
            CLIENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            PHONE TEXT NOT NULL,
            ADDRESS TEXT NOT NULL,
            PAYMENT_INFO TEXT
        )''')
        cursor.execute('SELECT CLIENT_ID, NAME, PHONE, ADDRESS FROM CLIENT')
        rows = cursor.fetchall()
        print('Clients:')
        for row in rows:
            print(f'- {row[0]}: {row[1]}, {row[2]}, {row[3]}')

def print_clients():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS CLIENT (
            CLIENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            PHONE TEXT NOT NULL,
            ADDRESS TEXT NOT NULL,
            PAYMENT_INFO TEXT
        )''')
        cursor.execute('SELECT * FROM CLIENT')
        rows = cursor.fetchall()
        print('All client records:')
        for row in rows:
            print(row)

def update_client():
    client_id = input('Enter client ID to update: ')
    new_name = input('Enter new name: ')
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE CLIENT SET NAME = ? WHERE CLIENT_ID = ?', (new_name, client_id))
        if cursor.rowcount:
            print(f'Client {client_id} updated.')
        else:
            print('Client not found.')
        conn.commit()

def delete_client():
    client_id = input('Enter client ID to delete: ')
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM CLIENT WHERE CLIENT_ID = ?', (client_id,))
        if cursor.rowcount:
            print(f'Client {client_id} deleted.')
        else:
            print('Client not found.')
        conn.commit()

def main_menu():
    while True:
        print('\n--- Client Management Menu (SQLite, Raw Queries) ---')
        print('1. Add client')
        print('2. List clients')
        print('3. Update client')
        print('4. Delete client')
        print('5. Print all client records')
        print('0. Exit')
        choice = input('Select an option: ')
        if choice == '1':
            add_client()
        elif choice == '2':
            list_clients()
        elif choice == '3':
            update_client()
        elif choice == '4':
            delete_client()
        elif choice == '5':
            print_clients()
        elif choice == '0':
            print('Exiting.')
            break
        else:
            print('Invalid option. Please try again.')

if __name__ == '__main__':
    main_menu()
