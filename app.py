from flask import Flask, redirect, render_template, request, url_for, session, flash
import sqlite3
import random
import datetime
import smtplib
from email.mime.text import MIMEText

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

    return render_template("select_role.html")

@app.route("/admin-login", methods = [ "POST", "GET" ])
def admin_login():

    admin_username = "agent"
    admin_password = "agent123"

    return render_template("admin_login.html")

@app.route("/agent-login", methods = [ "POST", "GET" ])
def agent_login():

    # conn.fetchOne

        
    


    return render_template("agent_login.html")

@app.route("/register-citizen", methods=[ "POST", "GET" ])
def register_citizen():

    if request.method == "POST":
        first_name = request.form["teamName"]
        middle_name = request.form["spread"]
        last_name = request.form["amount"]
        email = request.form["email"]
        date_of_birth = request.form["date_of_birth"]
        gender = request.form["gender"]

        # generate random int for the user id
            ## call generate citizen id function

        # pass sign_up_info to the db if I can 
        sign_up_info = (first_name, middle_name, last_name, email, date_of_birth, gender, citizen_id)

        # call Erin's send email function

    else:
        ()

    

    return render_template("index.html")

@app.route("/view-citizens")
def view_citizens():

    return render_template("view_citizens.html")

@app.route("/view-citizen")
def view_citizen():

    return render_template("view_citizen.html")

# Erin's function for sending email 
## def send_email(email, user_id):

# generate id function

# def generate_citizen_id():

    # citizen_id = ''.join(str(random.randint(0, 9)) for _ in range(9))

        # return citizen_ID
    


if __name__ == '__main__':
    app.run(debug=True) 