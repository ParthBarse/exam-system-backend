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
import re

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
        data = request.form

        # Validate required fields
        # required_fields = ["first_name", "last_name", "email", "phn", "dob", "address", "fathers_occupation", "mothers_occupation", "how_you_got_to_know", "employee_who_reached_out_to_you", "district", "state", "pincode", "status"]
        # for field in required_fields:
        #     if field not in data or not data[field]:
        #         raise ValueError(f"Missing or empty value for the required field: {field}")

        # Check if email and phn are not repeating
        students_db = db["students_db"]
        existing_student_email = students_db.find_one({"email": data["email"]})
        existing_student_phn = students_db.find_one({"phn": data["phn"]})

        if existing_student_email:
            raise ValueError(f"Email '{data['email']}' is already registered.")

        if existing_student_phn:
            raise ValueError(f"Phone number '{data['phn']}' is already registered.")

        # Generate a unique ID for the student using UUID
        sid = str(uuid.uuid4().hex)

        # Calculate age based on the provided date of birth
        age = calculate_age(data["dob"])

        student = {
            "sid": sid,
            "first_name": data["first_name"],
            "middle_name": data.get("middle_name", ""),
            "last_name": data["last_name"],
            "parents_name": data.get("parents_name", ""),
            "email": data["email"],
            "phn": str(data["phn"]),
            "parents_phn": data.get("parents_phn", ""),
            "parents_email": data.get("parents_email", ""),
            "dob": data["dob"],
            "age": str(age),
            "address": data["address"],
            "fathers_occupation": data["fathers_occupation"],
            "mothers_occupation": data["mothers_occupation"],
            "how_you_got_to_know": data["how_you_got_to_know"],
            "employee_who_reached_out_to_you": data["employee_who_reached_out_to_you"],
            "district": data["district"],
            "state": data["state"],
            "pincode": str(data["pincode"]),
            "status": "Active"
        }

        # Store the student information in the MongoDB collection
        students_db.insert_one(student)

        return jsonify({"message": "Student registered successfully", "sid": sid})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error


@app.route('/updateStudent', methods=['PUT'])
def update_student():
    try:
        data = request.form

        # Check if sid is provided
        if 'sid' not in data:
            raise ValueError("Missing 'sid' in the request.")

        # Find the student based on sid
        students_db = db["students_db"]
        student = students_db.find_one({"sid": data['sid']})

        if not student:
            return jsonify({"error": f"No student found with sid: {data['sid']}"}), 404  # Not Found

        # Update the student information with the received data
        for key, value in data.items():
            if key != 'sid':
                student[key] = value

        # Update the student in the database
        students_db.update_one({"sid": data['sid']}, {"$set": student})

        return jsonify({"message": f"Student with sid {data['sid']} updated successfully"})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
    try:
        students_db = db["students_db"]
        # Get the sid from request parameters
        sid = request.args.get('sid')

        if not sid:
            return jsonify({"error": "Missing 'sid' parameter in the request."}), 400  # Bad Request

        # Find the student based on sid
        student = students_db.find_one({"sid": sid})

        if not student:
            return jsonify({"error": f"No student found with sid: {sid}"}), 404  # Not Found

        # Delete the student from the database
        students_db.delete_one({"sid": sid})

        return jsonify({"message": f"Student with sid {sid} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getStudent', methods=['GET'])
def get_student():
    try:
        # Get the sid from request parameters
        sid = request.args.get('sid')

        if not sid:
            return jsonify({"error": "Missing 'sid' parameter in the request."}), 400  # Bad Request

        # Find the student based on sid
        students_db = db["students_db"]
        student = students_db.find_one({"sid": sid}, {"_id": 0})  # Exclude the _id field from the response

        if not student:
            return jsonify({"error": f"No student found with sid: {sid}"}), 404  # Not Found

        return jsonify({"student": student})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    

def build_filter_query(params):
    filter_query = {}

    for key, value in params.items():
        if value:
            # For 'age-group', parse l_age and g_age and add to the filter query
            if key == 'age-group':
                l_age, g_age = value.split(',')
                filter_query['age'] = {"$gte": int(l_age), "$lte": int(g_age)}

            # For other parameters, use regex for partial matching
            else:
                filter_query[key] = re.compile(f".*{re.escape(value)}.*", re.IGNORECASE)

    return filter_query

@app.route('/filterStudents', methods=['POST'])
def filter_students():
    try:
        # Get filter parameters from request parameters
        filter_params = request.json

        # Build the filter query
        filter_query = build_filter_query(filter_params)

        # Find students based on the filter query
        students_db = db["students_db"]
        students = students_db.find(filter_query, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        student_list = list(students)

        return jsonify({"students": student_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/addCamp', methods=['POST'])
def add_camp():
    try:
        data = request.form

        # Validate required fields
        # required_fields = ["camp_name", "chess_prefix", "camp_place", "camp_fee", "camp_description", "fee_discount", "discount_date", "final_fee"]
        # for field in required_fields:
        #     if field not in data or not data[field]:
        #         raise ValueError(f"Missing or empty value for the required field: {field}")

        # Generate a unique ID for the camp using UUID
        camp_id = str(uuid.uuid4().hex)

        camp = {
            "camp_id": camp_id,
            "camp_name": data["camp_name"],
            "chess_prefix": data["chess_prefix"],
            "camp_place": data["camp_place"],
            "camp_fee": float(data["camp_fee"]),  # assuming camp_fee is a float
            "camp_description": data["camp_description"],
            "fee_discount": float(data["fee_discount"]),  # assuming fee_discount is a float
            "discount_date": data["discount_date"],
            "final_fee": float(data["final_fee"])  # assuming final_fee is a float
        }

        # Store the camp information in the MongoDB collection
        camps_db = db["camps_db"]
        camps_db.insert_one(camp)

        return jsonify({"message": "Camp added successfully", "camp_id": camp_id})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/updateCamp', methods=['PUT'])
def update_camp():
    try:
        data = request.form

        # Check if camp_id is provided
        if 'camp_id' not in data:
            raise ValueError("Missing 'camp_id' in the request.")

        # Find the camp based on camp_id
        camps_db = db["camps_db"]
        camp = camps_db.find_one({"camp_id": data['camp_id']})

        if not camp:
            return jsonify({"error": f"No camp found with camp_id: {data['camp_id']}"}), 404  # Not Found

        # Update the camp information with the received data
        for key, value in data.items():
            if key != 'camp_id':
                # If the value is provided, update the field; otherwise, keep the existing value
                if value:
                    camp[key] = float(value) if key.endswith('_fee') else value

        # Update the camp in the database
        camps_db.update_one({"camp_id": data['camp_id']}, {"$set": camp})

        return jsonify({"message": f"Camp with camp_id {data['camp_id']} updated successfully"})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run()





