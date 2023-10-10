import sqlite3
import random
import datetime

conn = sqlite3.connect('id_user_data.db')
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

# Admin credentials
admin_username = "admin"
admin_password = "admin123"

# Agent role
agent_role = "agent"

# Authenticating users 
def authenticate_user():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == admin_username and password == admin_password:
            return "admin"
        elif username == agent_role:
            return agent_role
        else:
            print("Invalid username or password. Try again.")

# Erin this is the section where the email being sent out should be added to from lines 41-60
def create_user(conn, first_name, middle_name, last_name, date_of_birth, email, gender):
    try:
        cursor = conn.cursor() 
        
        
        cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"User with email '{email}' already exists with ID: {existing_user[0]}")
        else:
            user_id = ''.join(str(random.randint(0, 9)) for _ in range(9))
            cursor.execute('''
                INSERT INTO users (first_name, middle_name, last_name, date_of_birth, email, gender, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, middle_name, last_name, date_of_birth, email, gender, user_id))
            conn.commit()
            print(f"New user created with ID: {user_id}")
    except sqlite3.Error as e:
        print("SQLite error:", e)

def get_user_by_email(conn, email):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_data = cursor.fetchone()
    return user_data

def update_user(conn, user_id, new_email):
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET email = ? WHERE user_id = ?', (new_email, user_id))
        conn.commit()
        print("User data updated successfully.")
    except sqlite3.Error as e:
        print("SQLite error:", e)

def delete_user(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        print("User deleted successfully.")
    except sqlite3.Error as e:
        print("SQLite error:", e)

conn = sqlite3.connect('id_user_data.db')

# If admin these are the options available to him/her
print("Welcome to the User Management System")
user_role = authenticate_user()

if user_role == "admin":
    while True:
        print("Choose an option:")
        print("1. Read User by Email")
        print("2. Update User Email")
        print("3. Delete User")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")
        
        if choice == '1':
            email = input("Enter email address to search: ")
            user_data = get_user_by_email(conn, email)
            if user_data:
                print("User found:")
                print(user_data)
            else:
                print("User not found.")
        
        elif choice == '2':
            user_id = input("Enter user ID to update email: ")
            new_email = input("Enter new email address: ")
            update_user(conn, user_id, new_email)
        
        elif choice == '3':
            user_id = input("Enter user ID to delete: ")
            delete_user(conn, user_id)
        
        elif choice == '4':
            break

elif user_role == agent_role:
    while True:
        print("Choose an option:")
        print("1. Create User")
        print("2. Exit")
        
        choice = input("Enter your choice (1/2): ")
        
        if choice == '1':
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
            create_user(conn, first_name, middle_name, last_name, date_of_birth, email, gender)
        
        elif choice == '2':
            break

conn.close()
