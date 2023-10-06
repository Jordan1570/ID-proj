import sqlite3
import random
import datetime

#just testing this out
conn = sqlite3.connect('snn_user_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        date_of_birth DATE,
        email TEXT UNIQUE,
        gender TEXT,
        user_id TEXT UNIQUE
    )
''')

first_name = input("Enter first name: ")
middle_name = input("Enter middle name (or 'NA' if none): ")
last_name = input("Enter last name: ")
dob_str = input("Enter date of birth (MM-DD-YYYY): ")
email = input("Enter email address: ")

while True:
    gender = input("Enter gender (M/F): ").strip().upper()
    if gender in ('M', 'F'):
        break
    else:
        print("Invalid input. Please enter 'M' for Male or 'F' for Female.")

date_of_birth = datetime.datetime.strptime(dob_str, "%m-%d-%Y")

cursor.execute('SELECT user_id FROM users WHERE first_name = ? AND last_name = ? AND date_of_birth = ?', (first_name, last_name, date_of_birth))
existing_user = cursor.fetchone()

if existing_user:
    print(f"User already exists with ID: {existing_user[0]}")
else:
    user_id = ''.join(str(random.randint(0, 9)) for _ in range(9))

    try:
        cursor.execute('''
            INSERT INTO users (first_name, middle_name, last_name, date_of_birth, email, gender, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, middle_name, last_name, date_of_birth, email, gender, user_id))
        print(f"New user created with ID: {user_id}")

        conn.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)
        
conn.close()
