from flask import Blueprint, request, session, render_template, redirect, url_for, jsonify,flash
import json
import uuid  
import os

houses_bp = Blueprint("houses", __name__)
HOUSES_FILE = "houses.json"

class House:
    def __init__(self, house_name, contact, location, description, image="../static/imges/header.jpg", user=None, id=None):
        self.id = id or str(uuid.uuid4())  
        self.house_name = house_name
        self.contact = contact
        self.location = location
        self.description = description
        self.image = image
        self.user = user 

    def to_dict(self):
        return {
            "id": self.id,
            "house_name": self.house_name,
            "contact": self.contact,
            "location": self.location,
            "description": self.description,
            "image": self.image,
            "user": self.user
        }

    @staticmethod
    def load_houses():
        if not os.path.exists(HOUSES_FILE):
            return []
        try:
            with open(HOUSES_FILE, "r") as file:
                return [House(**house) for house in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading houses: {e}")
            return []

    @staticmethod
    def save_houses(houses):
        try:
            with open(HOUSES_FILE, "w") as file:
                json.dump([house.to_dict() for house in houses], file, indent=4)
        except Exception as e:
            print(f"Error saving houses: {e}")

@houses_bp.route("/dashboard" , methods=["GET"] )
def dashboard():
    if not session.get("logged_in"): 
        flash("You must be logged in to access the dashboard.", "warning")
        return redirect(url_for("auth.login"))  

    return render_template("dashboard.html")


@houses_bp.route("/add_house", methods=["POST"])
def add_house():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    data = request.form 
    house_name = data.get("house_name", "").strip()
    contact = data.get("contact", "").strip()
    location = data.get("location", "").strip()
    description = data.get("description", "").strip()
    image = data.get("image", "../static/imges/header.jpg") 
    if not house_name or not contact or not location or not description:
        return "All fields are required!", 400

    houses = House.load_houses()
    new_house = House(house_name, contact, location, description, image, user=session.get("user"))
    houses.append(new_house)
    House.save_houses(houses)

    return redirect(url_for("houses.view_houses"))


@houses_bp.route("/edit_house/<house_id>", methods=["POST"])
def edit_house(house_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    houses = House.load_houses()
    for house in houses:
        if house.id == house_id and house.user == session.get("user"):
            house.house_name = request.form.get("house_name", house.house_name)
            house.contact = request.form.get("contact", house.contact)
            house.location = request.form.get("location", house.location)
            house.description = request.form.get("description", house.description)
            house.image = request.form.get("image", house.image)
            House.save_houses(houses)
            return redirect(url_for("houses.view_houses"))
    return "House not found or unauthorized", 404        

# حذف منزل
@houses_bp.route("/delete_house/<house_id>", methods=["POST"])
def delete_house(house_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    houses = House.load_houses()
    houses = [house for house in houses if not (house.id == house_id and house.user == session.get("user"))]
    House.save_houses(houses)

    return redirect(url_for("houses.view_houses"))
@houses_bp.route("/view_houses", methods=["GET"])
def view_houses():
    houses = House.load_houses()
    return render_template("dashboard.html", houses=houses) 

@houses_bp.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))  
    
    user_email = session["user"]
    houses = [house for house in House.load_houses() if house.user == user_email]

    return render_template("profile.html", user=user_email, houses=houses)