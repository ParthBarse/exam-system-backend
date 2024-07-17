from flask import Flask
from flask import request, session , make_response
from pymongo import MongoClient
from flask import Flask, request, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import datetime
from datetime import datetime
import random
import json
from email.mime.text import MIMEText
import smtplib
import uuid
import re
import os
import requests
from io import BytesIO
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import threading
import multiprocessing
import time
import zipfile
import requests
import base64

#--------------------------------------------------------------------------------

file_dir = "/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/exam_files/"
files_url = "https://files.bnbdevelopers.in"
files_base_dir = "/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/"
files_base_url = "https://files.bnbdevelopers.in/exam_files/"

# file_dir = "/home/mcfcamp-files/htdocs/files.mcfcamp.in/mcf_files/"
# files_url = "https://files.mcfcamp.in"
# files_base_dir = "/home/mcfcamp-files/htdocs/files.mcfcamp.in/"
# files_base_url = "https://files.mcfcamp.in/mcf_files/"

#----------------------------------------------------------------------------------



app = Flask(__name__)
CORS(app)

client = MongoClient(
    'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority')
app.config['MONGO_URI'] = 'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority'

# client = MongoClient(
#     'mongodb+srv://mcfcamp:mcf123@mcf.nyh46tl.mongodb.net/')
# app.config['MONGO_URI'] = 'mongodb+srv://mcfcamp:mcf123@mcf.nyh46tl.mongodb.net/'

app.config['SECRET_KEY'] = 'a6d217d048fdcd227661b755'
db = client['exam_system']
db2 = client['students_exam_answers']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "ic2023wallet@gmail.com"
app.config['MAIL_PASSWORD'] = "irbnexpguzgxwdgx"

host = ""


# notificationFlag = True

def getNotfStat():
    settings_db = db['count_db']
    data = settings_db.find_one({"found":"2"})
    if data :
        notificationFlag=data['status']
    else:
        notificationFlag="on"
    print("Notification - ",notificationFlag)
    return notificationFlag


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return 'home page'

def generate_new_receipt_no():
    count_db = db['count_db']
    c_data = count_db.find_one({"found":"1"})
    sr_no = int(c_data['sr_no'])
    count_db.update_one({"found":"1"}, {"$set": {"sr_no":int(sr_no+1)}})
    new_receipt_no = str("2024-"+str(int(sr_no+1)))
    return new_receipt_no


#-----------------------------------------------------------------------------------------

#---------------------- System Synchronization Module ------------------------------------

file_directory = file_dir

def save_file(file, uid):
    try:
        # Get the file extension from the original filename
        original_filename = file.filename
        _, file_extension = os.path.splitext(original_filename)

        # Generate a unique filename using UUID and append the original file extension
        filename = str(uuid.uuid4()) + file_extension

        file_path = os.path.join(file_directory, uid, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        return f'{files_base_url}{uid}/{filename}'
    except Exception as e:
        raise e

#-------------- Supporting Functions Start ----------------



#-------------- Supporting Functions End ----------------



#------------------------------------------------------------------------------------------

def sendSMS(msg,phn):
    notifyFlag = getNotfStat()
    if notifyFlag == "off":
        phn=''
    # phn="8793015610"
    if msg and phn:
        url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
        msg_text = msg
        phn_no = phn
        querystring = {"AUTH_KEY":"2b4186d8fc21f47949e7f5e92b56390","message":msg_text,"senderId":"MCFCMP","routeId":"1","mobileNos":phn_no,"smsContentType":"english"}
        headers = {'Cache-Control': "no-cache"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        return 0
    else:
        return 1
    

def send_wp(sms_content, mobile_numbers, file_paths=[]):
    notifyFlag = getNotfStat()
    if notifyFlag == "off":
        mobile_numbers=''
    # mobile_numbers="8793015610"
    if len(file_paths)>1:
            file_paths.append("THINGS_TO_BRING.pdf")
    api_url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
    auth_key = "2b4186d8fc21f47949e7f5e92b56390"
    route_id = "21"
    sender_id = "9604992000"
    sms_content_type = "english"
    payload = {
        "smsContent": sms_content,
        "routeId": route_id,
        "mobileNumbers": mobile_numbers,
        "senderId": sender_id,
        "smsContentType": sms_content_type
    }
    headers = {
        "AUTH_KEY": auth_key,
        "Content-Type": "application/json"
    }

    payload2 = {
        "smsContent": "",
        "routeId": route_id,
        "mobileNumbers": mobile_numbers,
        "senderId": sender_id,
        "smsContentType": sms_content_type
    }

    # Add file data if file_path is provided
    if file_paths:
        if len(file_paths) == 1:
            filedata_encoded = encode_file_to_base64(file_paths[0])
            if filedata_encoded:
                payload["filename"] = file_paths[0].split('/')[-1]  # Extract filename from path
                payload["filedata"] = filedata_encoded
            else:
                print(f"Error: Unable to encode {file_path} to Base64")
                return 1
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                response_json = response.json()
                if 'response' in response_json:
                    print("Send WP")
                    return 0
                else:
                    return 1
            else:
                return 1
        elif len(file_paths) > 1:
            for file_path in file_paths:
                filedata_encoded = encode_file_to_base64(file_path)
                if filedata_encoded:
                    payload2["filename"] = file_path.split('/')[-1]  # Extract filename from path
                    payload2["filedata"] = filedata_encoded
                else:
                    print(f"Error: Unable to encode {file_path} to Base64")
                response = requests.post(api_url, json=payload2, headers=headers)
                if response.status_code == 200:
                    response_json = response.json()
                    if 'response' in response_json:
                        print("Send WP")
                    else:
                        print("Error")
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if 'response' in response_json:
            print("Send WP")
            return 0
        else:
            return 1
    else:
        return 1

def encode_file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            filedata = file.read()
            filedata_encoded = base64.b64encode(filedata).decode('utf-8')
            return filedata_encoded
    except Exception as e:
        print(f"Error encoding file to Base64: {str(e)}")
        return None
    

def send_email(msg, sub, mailToSend):
    notifyFlag = getNotfStat()
    if notifyFlag == "off":
        mailToSend=''
    # mailToSend = "parthbarse72@gmail.com"
    try:
        # Send the password reset link via email
        sender_email = "mcfcamp@gmail.com"
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login("mcfcamp@gmail.com", "meyv ghup onbl fqhu")

        message_text = msg
        message = MIMEText(message_text)
        message["Subject"] = sub
        message["From"] = sender_email
        message["To"] = mailToSend

        smtp_server.sendmail(sender_email, mailToSend, message.as_string())
        print(mailToSend)
        print("Send Mail")
        smtp_server.quit()
        return 0
    except Exception as e:
        print(str(e))
        return 1
    


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_attachments(msg, sub, mailToSend, files=[]):
    notifyFlag = getNotfStat()
    if notifyFlag == "off":
        mailToSend=''
    # mailToSend = "parthbarse72@gmail.com"
    try:
        if len(files)>1:
            files.append("THINGS_TO_BRING.pdf")
        sender_email = "mcfcamp@gmail.com"
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login("mcfcamp@gmail.com", "meyv ghup onbl fqhu")

        # Create a multipart message
        message = MIMEMultipart()
        message["Subject"] = sub
        message["From"] = sender_email
        message["To"] = mailToSend

        # Attach message body
        message.attach(MIMEText(msg, "plain"))

        # Attach files
        for file_path in files:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file_path}",
            )

            # Attach the attachment to the message
            message.attach(part)

        smtp_server.sendmail(sender_email, mailToSend, message.as_string())
        print(mailToSend)
        print("Send Mail")
        smtp_server.quit()
        return 0
    except Exception as e:
        print(str(e))
        return 1

# ------------------------------------------------------------------------------------------------------------

@app.route('/addExam', methods=['POST'])
def add_exam():
    try:
        data = request.form
        print("Data Recieved : ",data)
        print(data.get("exam_name"))

        # Generate a unique ID for the camp using UUID
        exam_id = str(uuid.uuid4().hex)

        exam = {
            "exam_id": exam_id,
            "exam_name": data["exam_name"].strip(),
            "exam_duration": data["exam_duration"],
            "exam_date": data["exam_date"],
            "exam_description": data["exam_description"],
            "exam_status" : data["exam_status"],
        }

        # Store the camp information in the MongoDB collection
        exams_db = db["exams_db"]
        exams_db.insert_one(exam)

        return jsonify({"message": "Exam added successfully", "exam_id": exam_id})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/updateExam', methods=['PUT'])
def update_exam():
    try:
        data = request.form

        # Check if exam_id is provided
        if 'exam_id' not in data:
            raise ValueError("Missing 'exam_id' in the request.")

        # Find the exam based on exam_id
        exams_db = db["exams_db"]
        exam = exams_db.find_one({"exam_id": data['exam_id']})

        if not exam:
            return jsonify({"error": f"No exam found with exam_id: {data['exam_id']}"}), 404  # Not Found

        # Update the exam information with the received data
        for key, value in data.items():
            if key != 'exam_id':
                # If the value is provided, update the field; otherwise, keep the existing value
                if value:
                    exam[key] = value
                    if exam['exam_status'] == "on":
                        exam["exam_status"] = "Active"
                    else:
                        exam['exam_status'] = "Inactive"

        # Update the exam in the database
        exams_db.update_one({"exam_id": data['exam_id']}, {"$set": exam})

        return jsonify({"message": f"Exam with exam_id {data['exam_id']} updated successfully"})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getAllExams', methods=['GET'])
def get_all_exams():
    try:
        exams_db = db["exams_db"]
        exams = exams_db.find({}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        exam_list = list(exams)

        return jsonify({"exams": exam_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getAllExamsActive', methods=['GET'])
def get_all_exams_active():
    try:
        exams_db = db["exams_db"]
        exams = exams_db.find({"exam_status":"Active"}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        exam_list = list(exams)

        return jsonify({"exams": exam_list})

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
    
@app.route('/getExam', methods=['GET'])
def get_exam():
    try:
        # Get the exam_id from request parameters
        exam_id = request.args.get('exam_id')

        if not exam_id:
            return jsonify({"error": "Missing 'exam_id' parameter in the request."}), 400  # Bad Request

        # Find the exam based on exam_id
        exams_db = db["exams_db"]
        exam = exams_db.find_one({"exam_id": exam_id}, {"_id": 0})  # Exclude the _id field from the response

        if not exam:
            return jsonify({"error": f"No exam found with exam_id: {exam_id}"}), 404  # Not Found

        return jsonify({"exam": exam})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/deleteExam', methods=['DELETE'])
def delete_exam():
    try:
        # Get the exam_id from request parameters
        exam_id = request.args.get('exam_id')

        if not exam_id:
            return jsonify({"error": "Missing 'exam_id' parameter in the request."}), 400  # Bad Request

        # Find the exam based on exam_id
        exams_db = db["exams_db"]
        exam = exams_db.find_one({"exam_id": exam_id})

        if not exam:
            return jsonify({"error": f"No exam found with exam_id: {exam_id}"}), 404  # Not Found

        # Delete the exam from the database
        exams_db.delete_one({"exam_id": exam_id})

        return jsonify({"message": f"Exam with exam_id {exam_id} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/addQuestion', methods=['POST'])
def add_question():
    try:
        data = request.form
        data = dict(data)
        print(data)

        # Generate a unique ID for the batch using UUID
        question_id = str(uuid.uuid4().hex)

        data['question_id'] = question_id

        # Store the batch information in the MongoDB collection
        question_db = db["questions_db"]
        question_db.insert_one(data)

        return jsonify({"message": "Question added successfully", "question_id": question_id})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@app.route('/updateQuestion', methods=['POST'])
def update_question():
    try:
        data = request.form

        # Check if question_id is provided
        if 'question_id' not in data:
            raise ValueError("Missing 'question_id' in the request.")

        # Find the question based on question_id
        questions_db = db["questions_db"]
        question = questions_db.find_one({"question_id": data['question_id']})

        if not question:
            return jsonify({"error": f"No question found with question_id: {data['question_id']}"}), 404  # Not Found

        # Update the question information with the received data
        for key, value in data.items():
            if key != 'question_id':
                # If the value is provided, update the field; otherwise, keep the existing value
                if value:
                    question[key] = int(value) if key == 'question_intake' else value

        # Update the question in the database
        questions_db.update_one({"question_id": data['question_id']}, {"$set": question})

        return jsonify({"message": f"question with question_id {data['question_id']} updated successfully", "camp_id":question['camp_id']})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getQuestions', methods=['GET'])
def get_questions():
    try:
        # Get the exam_id from request parameters
        exam_id = request.args.get('exam_id')

        if not exam_id:
            return jsonify({"error": "Missing 'exam_id' parameter in the request."}), 400  # Bad Request

        # Find Question based on exam_id
        question_db = db["questions_db"]
        question = question_db.find({"exam_id": exam_id}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        question_list = list(question)

        return jsonify({"question": question_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error


@app.route('/getQuestion', methods=['GET'])
def get_question():
    try:
        # Get the question_id from request parameters
        question_id = request.args.get('question_id')

        if not question_id:
            return jsonify({"error": "Missing 'question_id' parameter in the request."}), 400  # Bad Request

        # Find the question based on question_id
        questions_db = db["questions_db"]
        question = questions_db.find_one({"question_id": question_id}, {"_id": 0})  # Exclude the _id field from the response

        if not question:
            return jsonify({"error": f"No question found with question_id: {question_id}"}), 404  # Not Found

        return jsonify({"question": question})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/deleteQuestion', methods=['DELETE'])
def delete_question():
    try:
        # Get the question_id from request parameters
        question_id = request.args.get('question_id')

        if not question_id:
            return jsonify({"error": "Missing 'question_id' parameter in the request."}), 400  # Bad Request

        # Find the question based on question_id
        questions_db = db["questions_db"]
        question = questions_db.find_one({"question_id": question_id})

        if not question:
            return jsonify({"error": f"No question found with question_id: {question_id}"}), 404  # Not Found

        # Delete the question from the database
        questions_db.delete_one({"question_id": question_id})

        return jsonify({"message": f"question with question_id {question_id} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/uploadFile', methods=['POST'])
def upload_file():
    try:
        # Check if 'file' and 'sid' parameters are present in the form data
        if 'file' not in request.files:
            return jsonify({'error': 'Missing parameters: file',"success":False}), 400

        uploaded_file = request.files['file']
        sid = "All_Files"

        # Check if the file is an allowed type (e.g., image or pdf)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
        if (
            '.' in uploaded_file.filename
            and uploaded_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions
        ):
            return jsonify({'error': 'Invalid file type. Only allowed: png, jpg, jpeg, gif, pdf.',"success":False}), 400

        # Save the file and get the URL
        file_url = save_file(uploaded_file, sid)

        return jsonify({'message': 'File stored successfully.', 'file_url': file_url,"success":True}), 200

    except Exception as e:
        return jsonify({'error': str(e),"success":False}), 500
    

@app.route('/registerStudentExam', methods=['POST'])
def register_student_exam():
    try:
        data = request.form
        data = dict(data)
        # Generate a unique ID for the student using UUID
        seid = str(uuid.uuid4().hex)
        data["seid"] = seid
        exam_students_db = db["exam_students_db"]
        exam_students_db.insert_one(data)
        return jsonify({"message": "Student registered successfully", "seid": seid})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getAllExamStudents', methods=['GET'])
def get_all_exam_students():
    try:
        students_db = db["exam_students_db"]
        students = students_db.find({}, {"_id": 0})  # Exclude the _id field from the response

        # Convert the cursor to a list of dictionaries for easier serialization
        exam_list = list(students)

        return jsonify({"students": exam_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    

@app.route('/deleteExamStudent', methods=['DELETE'])
def delete_exam_student():
    try:
        # Get the seid from request parameters
        seid = request.args.get('seid')

        if not seid:
            return jsonify({"error": "Missing 'seid' parameter in the request."}), 400  # Bad Request

        # Find the seis based on seid
        exam_students_db = db["exam_students_db"]
        student = exam_students_db.find_one({"seid":  seid})

        if not student:
            return jsonify({"error": f"No student found with  seid: { seid}"}), 404  # Not Found

        # Delete the exam from the database
        exam_students_db.delete_one({"seid": seid})

        return jsonify({"message": f"Student with seid {seid} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    

@app.route('/submitAnswers', methods=['POST'])
def submit_answers():
    try:
        data = request.data
        # data = dict(data)
        students_exam_answers_db = db2[data['ueid']]

        if (students_exam_answers_db.find_one({"question_id":data['question_id']})):
            students_exam_answers_db.update_one({"question_id":data['question_id']}, {"$set": {"answers":data['answers']}})
            return jsonify({"message": "Answer submitted successfully", "question_id": data['question_id']})
        else:
            students_exam_answers_db.insert_one(data)
            return jsonify({"message": "Answer submitted successfully", "question_id": data['question_id']})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    

    



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8088)





