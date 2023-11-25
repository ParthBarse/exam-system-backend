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

@app.route("/getInactiveStudents", methods=["GET"])
def getInactiveStudents():
    users = db["students_db"]
    ans = []
    ans = list(users.find({"status":"inactive"},{'_id':0}))
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
            "status": "Active",
            "camp_id": data.get("camp_id", ""),
            "camp_category": data.get("camp_category", ""),
            "batch_id": data.get("batch_id", ""),
            "food_option": data.get("food_option", ""),
            "dress_code": data.get("dress_code", ""),
            "pick_up_point": data.get("pick_up_point", ""),
            "height": data.get("height", ""),
            "weight": data.get("weight", ""),
            "blood_group": data.get("blood_group", ""),
            "payment_option": data.get("payment_option", ""),
            "school_name": data.get("school_name", ""),
            "gender": data.get("gender", ""),
            "standard": data.get("standard", ""),
            "wp_no": data.get("wp_no", ""),
            "payment_status": data.get("payment_status", "Pending")
        }

        # Store the student information in the MongoDB collection
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id":data.get("batch_id")}, {"_id":0})
        if batch:
            if int(batch["students_registered"]) >= int(batch["batch_intake"]):
                students_db.insert_one(student)
                batches_db.update_one({"batch_id": data.get("batch_id")}, {"$set": {"students_registered":int(batch["students_registered"]+1)}})
                return jsonify({"message": "Student registered successfully", "sid": sid})
            else:
                return jsonify({"message": "Batch is Already Full !"})

        # return jsonify({"message": "Student registered successfully", "sid": sid})

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
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id":data.get("batch_id")}, {"_id":0})
        if batch:
            if int(batch["students_registered"]) <= int(batch["batch_intake"]):
                students_db.update_one({"sid": data['sid']}, {"$set": student})
                return jsonify({"message": f"Student with sid {data['sid']} updated successfully"})
            else:
                return jsonify({"message": "Batch is Already Full !"},400)
        else:
            return jsonify({"message": "Batch not Found !"},400)
            
        # students_db.update_one({"sid": data['sid']}, {"$set": student})
        # return jsonify({"message": f"Student with sid {data['sid']} updated successfully"})

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

        # If camp_id and batch_id are available in the student data, fetch additional information
        camp_id = student.get("camp_id", "")
        batch_id = student.get("batch_id", "")

        # Fetch camp details if camp_id is present
        camp_details = {}
        if camp_id:
            camps_db = db["camps_db"]
            camp_details = camps_db.find_one({"camp_id": camp_id}, {"_id": 0})

        # Fetch batch details if batch_id is present
        batch_details = {}
        if batch_id:
            batches_db = db["batches_db"]
            batch_details = batches_db.find_one({"batch_id": batch_id}, {"_id": 0})

        # Combine student, camp, and batch details
        response_data = {
            "student": student,
            "camp_details": camp_details,
            "batch_details": batch_details
        }

        return jsonify(response_data)

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
            "camp_status" : data["camp_status"],
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
    
@app.route('/getAllCamps', methods=['GET'])
def get_all_camps():
    try:
        camps_db = db["camps_db"]
        camps = camps_db.find({}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        camp_list = list(camps)

        return jsonify({"camps": camp_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getAllBatches', methods=['GET'])
def get_all_batches():
    try:
        batches_db = db["batches_db"]
        batches = batches_db.find({}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        batches_list = list(batches)

        return jsonify({"camps": batches_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getCamp', methods=['GET'])
def get_camp():
    try:
        # Get the camp_id from request parameters
        camp_id = request.args.get('camp_id')

        if not camp_id:
            return jsonify({"error": "Missing 'camp_id' parameter in the request."}), 400  # Bad Request

        # Find the camp based on camp_id
        camps_db = db["camps_db"]
        camp = camps_db.find_one({"camp_id": camp_id}, {"_id": 0})  # Exclude the _id field from the response

        if not camp:
            return jsonify({"error": f"No camp found with camp_id: {camp_id}"}), 404  # Not Found

        return jsonify({"camp": camp})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/deleteCamp', methods=['DELETE'])
def delete_camp():
    try:
        # Get the camp_id from request parameters
        camp_id = request.args.get('camp_id')

        if not camp_id:
            return jsonify({"error": "Missing 'camp_id' parameter in the request."}), 400  # Bad Request

        # Find the camp based on camp_id
        camps_db = db["camps_db"]
        camp = camps_db.find_one({"camp_id": camp_id})

        if not camp:
            return jsonify({"error": f"No camp found with camp_id: {camp_id}"}), 404  # Not Found

        # Delete the camp from the database
        camps_db.delete_one({"camp_id": camp_id})

        return jsonify({"message": f"Camp with camp_id {camp_id} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/addBatch', methods=['POST'])
def add_batch():
    try:
        data = request.form

        # Validate required fields
        required_fields = ["batch_name", "start_date", "end_date", "company", "duration", "batch_intake", "camp_id"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing or empty value for the required field: {field}")

        # Parse start_date and end_date to datetime objects
        start_date = data["start_date"]
        end_date = data["end_date"]

        # Generate a unique ID for the batch using UUID
        batch_id = str(uuid.uuid4().hex)

        batch = {
            "batch_id": batch_id,
            "batch_name": data["batch_name"],
            "start_date": start_date,
            "end_date": end_date,
            "company": data["company"],
            "duration": data["duration"],
            "batch_intake": int(data["batch_intake"]),
            "students_registered": 0,
            "camp_id": data["camp_id"]
        }

        # Store the batch information in the MongoDB collection
        batches_db = db["batches_db"]
        batches_db.insert_one(batch)

        return jsonify({"message": "Batch added successfully", "batch_id": batch_id})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@app.route('/updateBatch', methods=['POST'])
def update_batch():
    try:
        data = request.form

        # Check if batch_id is provided
        if 'batch_id' not in data:
            raise ValueError("Missing 'batch_id' in the request.")

        # Find the batch based on batch_id
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id": data['batch_id']})

        if not batch:
            return jsonify({"error": f"No batch found with batch_id: {data['batch_id']}"}), 404  # Not Found

        # Update the batch information with the received data
        for key, value in data.items():
            if key != 'batch_id':
                # If the value is provided, update the field; otherwise, keep the existing value
                if value:
                    batch[key] = int(value) if key == 'batch_intake' else value

        # Update the batch in the database
        batches_db.update_one({"batch_id": data['batch_id']}, {"$set": batch})

        return jsonify({"message": f"Batch with batch_id {data['batch_id']} updated successfully", "camp_id":batch['camp_id']})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getBatches', methods=['GET'])
def get_batches():
    try:
        # Get the camp_id from request parameters
        camp_id = request.args.get('camp_id')

        if not camp_id:
            return jsonify({"error": "Missing 'camp_id' parameter in the request."}), 400  # Bad Request

        # Find batches based on camp_id
        batches_db = db["batches_db"]
        batches = batches_db.find({"camp_id": camp_id}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        batch_list = list(batches)

        return jsonify({"batches": batch_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getBatch', methods=['GET'])
def get_batch():
    try:
        # Get the batch_id from request parameters
        batch_id = request.args.get('batch_id')

        if not batch_id:
            return jsonify({"error": "Missing 'batch_id' parameter in the request."}), 400  # Bad Request

        # Find the batch based on batch_id
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id": batch_id}, {"_id": 0})  # Exclude the _id field from the response

        if not batch:
            return jsonify({"error": f"No batch found with batch_id: {batch_id}"}), 404  # Not Found

        return jsonify({"batch": batch})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/deleteBatch', methods=['DELETE'])
def delete_batch():
    try:
        # Get the batch_id from request parameters
        batch_id = request.args.get('batch_id')

        if not batch_id:
            return jsonify({"error": "Missing 'batch_id' parameter in the request."}), 400  # Bad Request

        # Find the batch based on batch_id
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id": batch_id})

        if not batch:
            return jsonify({"error": f"No batch found with batch_id: {batch_id}"}), 404  # Not Found

        # Delete the batch from the database
        batches_db.delete_one({"batch_id": batch_id})

        return jsonify({"message": f"Batch with batch_id {batch_id} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/activateStudent', methods=['GET'])
def activate_student():
    try:
        # Get the sid from request parameters
        sid = request.args.get('sid')

        if not sid:
            return jsonify({"error": "Missing 'sid' parameter in the request."}), 400  # Bad Request

        # Find the student based on sid
        students_db = db["students_db"]
        student = students_db.find_one({"sid": sid}, {"_id": 0})

        if not student:
            return jsonify({"error": f"No student found with sid: {sid}"}), 404  # Not Found

        # Update the status to "Active"
        students_db.update_one({"sid": sid}, {"$set": {"status": "active"}})

        return jsonify({"message": f"Student with sid {sid} is now active."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/generateReport', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()

        # Get parameters from the JSON data
        sid = data.get('sid')
        rank = data.get('rank')
        report_date = data.get('report_date')
        report_camp_name = data.get('report_camp_name')
        in_charge = data.get('in_charge')
        cqy = data.get('cqy')
        discipline = data.get('discipline')
        physical_fitness = data.get('physical_fitness')
        courage = data.get('courage')
        leadership = data.get('leadership')
        initiative = data.get('initiative')
        interpersonal_relations = data.get('interpersonal_relations')
        team_building = data.get('team_building')
        training = data.get('training')

        # Check if sid is provided
        if not sid:
            return jsonify({"error": "Missing 'sid' parameter in the request."}), 400  # Bad Request

        # Find the student based on sid
        students_db = db["students_db"]
        student = students_db.find_one({"sid": sid}, {"_id": 0})

        if not student:
            return jsonify({"error": f"No student found with sid: {sid}"}), 404  # Not Found

        # Update the student record with the report details
        students_db.update_one(
            {"sid": sid},
            {"$set": {
                "rank": rank,
                "report_date": report_date,
                "report_camp_name": report_camp_name,
                "in_charge": in_charge,
                "cqy": cqy,
                "discipline": discipline,
                "physical_fitness": physical_fitness,
                "courage": courage,
                "leadership": leadership,
                "initiative": initiative,
                "interpersonal_relations": interpersonal_relations,
                "team_building": team_building,
                "training": training
            }}
        )

        return jsonify({"message": f"Report generated for student with sid {sid}."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run()





