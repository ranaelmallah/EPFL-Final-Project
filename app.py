import bcrypt
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from email_validator import validate_email, EmailNotValidError
import re
import json
import os
from datetime import datetime

from auth_routes import auth_bp
from houses_routes import houses_bp
app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(houses_bp)

app.secret_key = "your_secret_key"  
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

USERS_FILE = "/users.json"
HOUSES_FILE = "/houses.json"

def load_houses():
    try:
        with open("houses.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] 



@app.route("/", methods=["GET"])
def index():
    houses = load_houses()
    return render_template("index.html", houses=houses)
    
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
