from flask import Flask,render_template,url_for,jsonify,request
import json
import uuid
import re
import os
app =Flask(__name__)


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/dashboard")
def dashboard():
   return render_template("dashboard.html")

@app.route("/profile")
def profile():
   return render_template("profile.html")

@app.route("/signup")
def signup():
   return render_template("signup.html")

@app.route("/about")
def about():
   return render_template("about.html")




DATA_USER_FILE = "users.json"
class User:
    def __init__(self, id, username, email, hashed_password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = hashed_password

        def hash_password(self):
            return bcrypt.

class House:
    def __init__(self, id, name, address, description, image):
        self.id = str(uuid.uuid4())
        self.name = name
        self.adress=address
        self.description=description
        self.image=image

# Function to read JSON data
def read_users():
    if os.path.exists(DATA_USER_FILE):
        with open(DATA_USER_FILE, "r") as file:
            return json.load(file)
    return []

# Function to write JSON data
def write_users(users):
    with open(DATA_USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or len(username) < 3:
        return jsonify({"success": False, "message": "Username must be at least 3 characters long."})

    if not email or "@" not in email or "." not in email:
        return jsonify({"success": False, "message": "Invalid email format."})

    if not password or len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters long."})

    users = read_users()

    # Check if email already exists
    for user in users:
        if user["email"] == email:
            return jsonify({"success": False, "message": "Email already exists. Please log in."})

    # Save new user
    users.append({"username": username, "email": email, "password": password})
    write_users(users)

    return jsonify({"success": True, "message": "User registered successfully."})

@app.route("/signup-page")
def signup_page():
    return render_template("../templates/signup.html")
# ==================================================================================

DATA_FILE = "houses.json"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/houses", methods=["GET"])
def get_houses():
    return jsonify(load_data())

@app.route("/houses", methods=["POST"])
def add_house():
    data = load_data()
    new_house = request.json
    data.append(new_house)
    save_data(data)
    return jsonify({"message": "House added successfully!"}), 201

@app.route("/houses/<int:index>", methods=["PUT"])
def update_house(index):
    data = load_data()
    if 0 <= index < len(data):
        data[index] = request.json
        save_data(data)
        return jsonify({"message": "House updated successfully!"})
    return jsonify({"error": "Invalid index"}), 400

@app.route("/houses/<int:index>", methods=["DELETE"])
def delete_house(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
        return jsonify({"message": "House deleted successfully!"})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    app.run(debug=True)


# @app.route("/forgetpassword")
# def forgetpassword():
#     return render_template("forgetpassword.html")  

# @app.route("/reset")
# def resetpassword():
#     return render_template("resetpass.html") 

