from flask import Flask
from flask_login import login_user
from flask import request, session
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from datetime import datetime
import random
import json
import pandas as pd
from email.mime.text import MIMEText
import smtplib
import uuid

app = Flask(__name__)
CORS(app)

client = MongoClient(
    'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority')
app.config['MONGO_URI'] = 'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'a6d217d048fdcd227661b755'
db = client['mcf_db']
# db2 = client['BnB_all_customers']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "ic2023wallet@gmail.com"
app.config['MAIL_PASSWORD'] = "irbnexpguzgxwdgx"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return 'home page'


# ------------------------------------------------------------------------------------------------------------


@app.route("/getAllStudents", methods=["GET"])
def getAllStudents():
    users = db["students_db"]
    ans = []
    ans = list(users.find({},{'_id':0}))
    return jsonify({"students":ans})

def calculate_age(dob):
    try:
        birth_date = datetime.strptime(dob, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        raise ValueError("Invalid date of birth format. Please use 'dd-mm-yyyy'.")

@app.route('/registerStudent', methods=['POST'])
def register_student():
    try:
        data = request.json

        # Validate required fields
        required_fields = ["first_name", "last_name", "email", "phn", "dob", "address", "fathers_occupation", "mothers_occupation", "how_you_got_to_know", "employee_who_reached_out_to_you", "district", "state", "pincode", "status"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing or empty value for the required field: {field}")

        # Generate a unique ID for the student using UUID
        sid = str(uuid.uuid4().hex)

        # Calculate age based on the provided date of birth
        age = calculate_age(data["dob"])

        # Construct the student document
        student = {
            "sid": sid,
            "first_name": data["first_name"],
            "middle_name": data.get("middle_name", ""),
            "last_name": data["last_name"],
            "parents_name": data.get("parents_name", ""),
            "email": data["email"],
            "phn": data["phn"],
            "parents_phn": data.get("parents_phn", ""),
            "parents_email": data.get("parents_email", ""),
            "dob": data["dob"],
            "age": age,
            "food_option": data.get("food_option", ""),
            "dress_code": data.get("dress_code", ""),
            "address": data["address"],
            "camp": data.get("camp", ""),
            "fathers_occupation": data["fathers_occupation"],
            "mothers_occupation": data["mothers_occupation"],
            "how_you_got_to_know": data["how_you_got_to_know"],
            "employee_who_reached_out_to_you": data["employee_who_reached_out_to_you"],
            "landmark": data.get("landmark", ""),
            "pick_up_point": data.get("pick_up_point", ""),
            "district": data["district"],
            "state": data["state"],
            "pincode": data["pincode"],
            "status": data["status"]
        }

        # Store the student information in the MongoDB collection
        students_db = db['students_db']
        students_db.insert_one(student)

        return jsonify({"message": "Student registered successfully", "sid": sid})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run()










