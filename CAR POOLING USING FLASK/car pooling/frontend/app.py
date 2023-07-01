from flask import Flask, render_template, request, redirect, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

backend_url = "http://localhost:2000"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/myride")
def myride():
    response = requests.get(f"{backend_url}/myrides/"+session["user"])
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
        return render_template("myrides.html",myrides=response_data)
    else:
        return "Failed to fetch ride data"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        response = requests.post(f"{backend_url}/register", json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })

        if response.status_code == 200:
            return redirect("/")
            alert("registered successfully")
        else:
            return "Failed to register user"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        response = requests.post(f"{backend_url}/login", json={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            session["user"] = response.json().get("user_id")
            return redirect("/dashboard")
        else:
            return "Invalid email or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user_id = session["user"]
        response = requests.get(f"{backend_url}/dashboard/{user_id}")

        if response.status_code == 200:
            role = response.json().get("role")
            if role == "user":
                return redirect("/user_dashboard")
            elif role == "driver":
                return redirect("/driver_dashboard")
            else:
                return "Invalid role"

    return redirect("/login")
@app.route("/user_dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route("/driver_dashboard")
def driver_dashboard():
    response = requests.get(f"{backend_url}/rides")
    if response.status_code == 200:
        response_data = response.json()
        return render_template("driver_dashboard.html",rides=response_data)
    else:
        return "Failed to fetch ride data"

     
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/profile")
def profile():
    if "user" in session:
        user_id = session["user"]
        response = requests.get(f"{backend_url}/profile/{user_id}")

        if response.status_code == 200:
            user_data = response.json().get("user")
            return render_template("profile.html", user=user_data)

    return redirect("/login")

@app.route("/submit_ride", methods=["POST"])
def submit_ride():
    if "user" in session:
        user_id = session["user"]
        payment = request.form["payment"]
        duration = request.form["duration"]
        destination = request.form["destination"]
        pickup_time = request.form["pickup_time"]
        starting_point = request.form["starting_point"]

        response = requests.post(f"{backend_url}/submit_ride", json={
            "user_id": user_id,
            "payment": payment,
            "duration": duration,
            "destination": destination,
            "pickup_time": pickup_time,
            "starting_point": starting_point
        })

        if response.status_code == 200:
            print("Ride submitted successfully")
        else:
            print("Failed to submit ride")

    return redirect("/user_dashboard")


@app.route("/accept/<id>",methods=['POST','GET'])
def accept(id):
    print('accept:',id)
    id1=session["user"]
    response =requests.get(f"{backend_url}/accept/"+id+"/"+id1)
    if response.status_code == 200:
            print (response.text)
            print("accepted successfully")
    else:
            print("accepting failed")
    return redirect("/driver_dashboard")


    
@app.route("/reject/<id>",methods=['GET','POST'])
def reject(id):
    print('reject:',id)
    response = requests.get(f"{backend_url}/reject/"+id)
    print(response.text)
    if response.status_code == 200:
            print("rejecting successfully")
    else:
            print("rejecting failed")
    return redirect("/driver_dashboard")
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
