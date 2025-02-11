from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__)


db_path = os.path.join(os.getcwd(), "users.json")


class User:
    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = generate_password_hash(password)

    def to_dict(self):
        return {"fullname": self.fullname, "email": self.email, "password": self.password}


def load_users():
    if not os.path.exists(db_path):
        return []
    with open(db_path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_users(users):
    with open(db_path, "w") as file:
        json.dump(users, file, indent=4)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form
        print("Received data:", data)
        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        
        if not fullname or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.signup"))

        users = load_users()
        if any(user['email'] == email for user in users):
            flash("Email already exists. Please use a different email.", "error")
            return redirect(url_for("auth.signup"))

        new_user = User(fullname, email, password) 
        users.append(new_user.to_dict())  
        save_users(users)

        session['user'] = email
        flash("Signup successful!", "success")
        return redirect(url_for("houses.dashboard"))

    except Exception as e:
        print("Error in signup:", str(e))  
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

@auth_bp.route('/signup', methods=['GET'])
def signup_page():
    return render_template("signup.html")


@auth_bp.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    users = load_users()
    user_data = next((user for user in users if user['email'] == email), None)

    if not user_data:
        flash("Invalid email.", "error")
        return redirect(url_for("auth.login"))

    if not check_password_hash(user_data['password'], password):
        flash("Invalid password.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = email
    session['logged_in'] = True
    flash("Login successful!", "success")
    return redirect(url_for("houses.dashboard"))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")  


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))
@auth_bp.route("/profile", methods=["GET"])
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    users = load_users()
    user_data = next((user for user in users if user["email"] == session["user"]), None)

    if not user_data:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for("auth.login"))

    return render_template("profile.html", user=user_data)
