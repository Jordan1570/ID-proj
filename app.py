from flask import Flask, redirect, render_template, request, url_for, session, flash
import sqlite3
import random
import datetime
import smtplib
from email.mime.text import MIMEText

# sqlite3 connection
conn = sqlite3.connect('mydatabase.db')
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

app = Flask(__name__)

@app.route("/")
def hello_world():
    
    return render_template("index.html")

@app.route("/select-role", methods = ["POST", "GET"]) 
def select_role():

    # maybe two diff passwords for agent and admin?

    # Do logic for if admin or agent
    # admin = request.form["admin"]
    # agent = request.form["agent"]

    # if admin:
    #     # give access to read update delete
    
    # if agent:
    #     # give access to only create
            # re render index.html
        

    return render_template("select_role.html")

# admin login
@app.route("/admin-login", methods = [ "POST", "GET" ])
def admin_login():

    # admin credentials
    admin_username = "admin"
    admin_password = "admin123"

    return render_template("admin_login.html")


# agent login
@app.route("/agent-login", methods = [ "POST", "GET" ])
def agent_login():

    # conn.fetchOne

        
    


    return render_template("agent_login.html")

# register citizen
@app.route("/register-citizen", methods=[ "POST", "GET" ])
def register_citizen():
        if request.method == "POST":
            first_name = request.form["first_name"]
            middle_name = request.form["middle_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            date_of_birth = request.form["date_of_birth"]
            gender = request.form["gender"]

            conn = sqlite3.connect('mydatabase.db')
            cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # conn.close()
            return "Email already registered. Please choose another."
        
        user_id = generate_citizen_id()
        

        cursor.execute('INSERT INTO users (first_name, middle_name, last_name, email, date_of_birth, gender, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (first_name, middle_name, last_name, email, date_of_birth, gender, user_id))
        conn.commit()
        # conn.close()

        send_code_to_email(email, user_id)

        return "Registration successful!"

# view citizen
@app.route("/view-citizen/<int:user_id>")
def view_citizen(user_id):
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        # Execute an SQL query to select the user with the specified user_id
        cursor.execute("SELECT id, first_name, middle_name, last_name, email, date_of_birth, gender, user_id FROM users WHERE id = ?", (user_id,))
        
        user = cursor.fetchone()

        conn.close()

        return render_template("view_citizen.html", user=user)

    except Exception as e:
        return f"An error occurred: {str(e)}"

# update citizen
@app.route("/update-citizen/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    if request.method == "POST":
        # Get the updated information from the form
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]

        # Connect to the database and execute an SQL query to update the user's information
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET first_name=?, middle_name=?, last_name=?, email=? WHERE id=?", (first_name, middle_name, last_name, email, user_id))
        conn.commit()
        conn.close()

        return redirect("/view-citizens")

    else:
        # Display the update form with the current user's information
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, first_name, middle_name, last_name, email FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()

        conn.close()

        return render_template("update_citizen.html", user_id=user_id, user=user)

# delete citizen
@app.route("/delete-citizen/<int:user_id>")
def delete_citizen(user_id):
    try:
        # Connect to the database and execute an SQL query to delete the user
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

        return redirect("/view-citizens")

    except Exception as e:
        return f"An error occurred: {str(e)}"

# View all citizens
@app.route("/view-citizens")
def view_citizens():
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        # Execute an SQL query to select all users
        cursor.execute("SELECT id, first_name, middle_name, last_name, email, date_of_birth, gender, user_id FROM users")

        # Fetch all user data
        users = cursor.fetchall()

        conn.close()

        # Render the HTML template and pass the user data
        return render_template("view_citizens.html", users=users)

    except Exception as e:
        return f"An error occurred: {str(e)}"


# erin's function to send code to email 
def send_code_to_email(email, user_id):
    # Email configuration
    SMTP_SERVER = "smtp.gmail.com"  
    SMTP_PORT = 587  
    SMTP_USERNAME = "Enter Email" 
    SMTP_PASSWORD = "Enter Password"

    msg = MIMEText(f"Your generated code is: {user_id}")
    msg["Subject"] = "Your Generated Code"
    msg["From"] = SMTP_USERNAME
    msg["To"] = email

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Send the email
        server.sendmail(SMTP_USERNAME, [email], msg.as_string())

        # Disconnect from the server
        server.quit()
        print(f"Code sent to {email}")
    except smtplib.SMTPException as e:
        print("SMTP error:", e)

def generate_citizen_id():

    citizen_id = ''.join(str(random.randint(0, 9)) for _ in range(9))

    return citizen_id
    


if __name__ == '__main__':
    app.run(debug=True) 