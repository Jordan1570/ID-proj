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

# Role selection
@app.route("/", methods=["POST", "GET"])
def select_role():
    if request.method == "POST":
        role = request.form.get("role")  # Check which role was selected

        if role == "admin":
            return redirect("/admin-login?role=admin")  # Pass role=admin as a query parameter
        elif role == "agent":
            return redirect("/register-citizen")

    return render_template("select_role.html")

# Admin login
@app.route("/admin-login", methods=["POST", "GET"])
def admin_login():
    admin_password = "admin123"

    # Check if the role query parameter is present and set to "admin"
    role = request.args.get("role")
    
    if role != "admin":
        return redirect("/")  # Redirect to the role selection page if the role is not "admin"

    if request.method == "POST":
        entered_password = request.form.get("admin_password")
        if entered_password == admin_password:
            return redirect("/view-citizens")
        else:
            # Password is incorrect, show an error message
            error_message = "Incorrect password. Please try again."
            return render_template("admin_login.html", error_message=error_message)
    
    return render_template("admin_login.html")


@app.route("/register-citizen", methods=[ "POST", "GET" ])
def register_citizen():

        if request.method == "POST":

            conn = sqlite3.connect('mydatabase.db')
            cursor = conn.cursor()

            first_name = request.form["first_name"]
            middle_name = request.form["middle_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            date_of_birth = request.form["date_of_birth"]
            gender = request.form["gender"]

            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()


        # Check if the email already exists

            if not existing_user:
            # conn.close()
        
                user_id = generate_citizen_id()
        
                cursor.execute('INSERT INTO users (first_name, middle_name, last_name, email, date_of_birth, gender, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (first_name, middle_name, last_name, email, date_of_birth, gender, user_id))
                conn.commit()
                # conn.close()

                send_code_to_email(email, user_id)

        return render_template("index.html")

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