from flask import Flask, redirect, render_template, request, url_for, session, flash

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

@app.route("/create-citizen", methods=["POST", "GET"])
def create_citizen():

    if request.method == "POST":
        first_name = request.form["teamName"]
        middle_name = request.form["spread"]
        last_name = request.form["amount"]
        email = request.form["email"]
        date_of_birth = request.form["date_of_birth"]
        gender = request.form["gender"]

    else:
        ()

    

    return render_template("index.html")

@app.route("/view-citizens")
def view_citizens():

    return render_template("view_citizens.html")

@app.route("/view-citizen")
def view_citizen():

    return render_template("view_citizen.html")

if __name__ == '__main__':
    app.run(debug=True) 