from flask import Flask
from flask_login import login_user
from flask import request, session
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
# from datetime import datetime
# from datetime import datetime, timedelta
import datetime
from datetime import datetime
import random
import json
from email.mime.text import MIMEText
import smtplib
import uuid
import re
import os

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

host = ""


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return 'home page'

def sendSMS(msg,phn):
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
    
def send_wp(sms_content, mobile_numbers):
    api_url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
    auth_key = "2b4186d8fc21f47949e7f5e92b56390"
    route_id = "21"
    sender_id = "8793015610"
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
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if 'response' in response_json:
            return 0
        else:
            return 1
    else:
        return 1


# ------------------------------------------------------------------------------------------------------------


@app.route("/getAllStudents", methods=["GET"])
def getAllStudents():
    users = db["students_db"]
    ans = []
    ans = list(users.find({},{'_id':0}))
    return jsonify({"students":ans[::-1]})

@app.route("/getInactiveStudents", methods=["GET"])
def getInactiveStudents():
    users = db["students_db"]
    ans = []
    ans = list(users.find({"status": {"$ne": "Active"}}, {"_id": 0}))
    return jsonify({"students":ans[::-1]})

def calculate_age(dob):
    try:
        birth_date = datetime.strptime(dob, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        raise ValueError("Invalid date of birth format. Please use 'dd-mm-yyyy'.")
    
from reportlab.pdfgen import canvas
    
# def convert_docx_to_pdf(docx_path, pdf_path):
#     # Load the DOCX file
#     doc = Document(docx_path)

#     # Create a PDF file
#     pdf = canvas.Canvas(pdf_path)

#     # Loop through paragraphs in the DOCX file and write them to the PDF
#     for paragraph in doc.paragraphs:
#         pdf.drawString(10, 800, paragraph.text)
#         pdf.showPage()

#     # Save the PDF file
#     pdf.save()
    

from docx import Document
from docx.shared import Pt
# from docx2pdf import convert

import subprocess

def convert_to_pdf(docx_file, pdf_file):
    try:
        subprocess.run(['unoconv', '--output', pdf_file, '--format', 'pdf', docx_file], check=True)
        print(f"Conversion successful: {docx_file} -> {pdf_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def set_font(run, font_name, font_size):
    font = run.font
    font.name = font_name
    font.size = Pt(font_size)
    font.bold = True

def find_and_replace_paragraph_med(paragraph, field_values):
    for run in paragraph.runs:
        print(run.text)
        for field, value in field_values.items():
            run.text = run.text.replace(f"{field}", value)
            set_font(run, 'Montserrat', 14)

def replace_fields_in_document_med(doc_path, field_values):
    doc = Document(doc_path)
    for paragraph in doc.paragraphs:
        find_and_replace_paragraph_med(paragraph, field_values)
    doc.save(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.docx")))

    # import aspose.words as aw
    # doc = aw.Document(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.docx")))
    # doc.save(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.pdf")))

    convert_to_pdf(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.docx")),str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.pdf")))

    # convert_docx_to_pdf(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.docx")), str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.pdf")))

    # convert(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.docx")), str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+str(f"{field_values['sid']}_MEDICAL_CER.pdf")))


from docx import Document
from docx.shared import Inches, Pt
import requests
from io import BytesIO

def set_paragraph_font_entrace_card(paragraph, font_name, font_size, bold=False):
    for run in paragraph.runs:
        font = run.font
        font.name = font_name
        font.size = Pt(font_size)
        font.bold = bold

def find_and_replace_paragraphs_entrance_card(paragraphs, field, replacement):
    for paragraph in paragraphs:
        if field in paragraph.text:
            paragraph.text = paragraph.text.replace(field, replacement)
            set_paragraph_font_entrace_card(paragraph, 'Arial', 9, False)

def find_and_replace_tables_entrance_card(tables, field, replacement):
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    find_and_replace_paragraphs_entrance_card([paragraph], field, replacement)

from docx import Document
from docx.shared import Inches, Pt
import requests
from io import BytesIO

def set_paragraph_font_visiting_card(paragraph, font_name, font_size, bold=False):
    for run in paragraph.runs:
        font = run.font
        font.name = font_name
        font.size = Pt(font_size)
        font.bold = bold                    

def find_and_replace_paragraphs_visiting_card(paragraphs, field, replacement):
    for paragraph in paragraphs:
        if field in paragraph.text:
            paragraph.text = paragraph.text.replace(field, replacement)
            set_paragraph_font_visiting_card(paragraph, 'Times New Roman', 16, False)

def find_and_replace_tables_visiting_card(tables, field, replacement):
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    find_and_replace_paragraphs_visiting_card([paragraph], field, replacement)

from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def replace_image_in_cell(doc, table_index, row_index, column_index, image_path):
    # Get the specified table
    table = doc.tables[table_index]

    # Get the specified cell
    cell = table.cell(row_index, column_index)

    # Clear the content of the cell by removing its paragraphs
    for paragraph in cell.paragraphs:
        paragraph.clear()

    # Add a new paragraph and insert the image
    paragraph = cell.add_paragraph()
    run = paragraph.add_run()
    run.add_picture(image_path, width=Inches(1.4))

    # Align the paragraph to the center
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

# image_path_father = 'img_rap.png'
# image_path_mother = 'rutu.png'
# image_path_cadet = 'aditi_pic.png'
# image_path_guardian = 'sai_photo.jpeg'

# replace_image_in_cell(doc, table_index=0, row_index=4, column_index=0, image_path=image_path_father)

# replace_image_in_cell(doc, table_index=0, row_index=4, column_index=2, image_path=image_path_mother)
# replace_image_in_cell(doc, table_index=0, row_index=4, column_index=6, image_path=image_path_cadet)
# replace_image_in_cell(doc, table_index=0, row_index=4, column_index=8, image_path=image_path_guardian)
        


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

        company = ""
        # Calculate age based on the provided date of birth
        age = calculate_age(data["dob"])
        if age>=7 and age<=11 and data.get("gender") == "male":
            company = "ALPHA"
        elif age>=12 and age<=16 and data.get("gender") == "male":
            company = "BRAVO"
        elif age>=17 and age<=21 and data.get("gender") == "male":
            company = "DELTA"
        elif age>=7 and age<=11 and data.get("gender") == "female":
            company = "CHARLEY"
        elif age>=12 and age<=16 and data.get("gender") == "female":
            company = "ECO"
        elif age>=17 and age<=21 and data.get("gender") == "female":
            company = "FOXFORD"

        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id":data.get("batch_id")}, {"_id":0})
        camps_db = db["camps_db"]
        camp = camps_db.find_one({"camp_id":data.get("camp_id")}, {"_id":0})
        camp_name = camp["camp_name"]
        camp_short = camp_name.split(" ")[-1].replace("(", "").replace(")", "")
        sid=""
        medical_cert_url = ""
        if batch:
            if int(batch["students_registered"]) <= int(batch["batch_intake"]):
                sr_no = int(int(batch["students_registered"])+1)
                start_date = batch["start_date"]
                year = start_date[-2:]
                day = start_date[0:2]
                batch_name = batch["batch_name"].replace(" ", "")

                sid = str(camp_short)+str(year)+str(day)+str(batch_name)+str(company)+str(sr_no)

                document_med_path = 'medical_certificate.docx'

                field_values = {
                    'CADET_NAME': str(data["first_name"].upper()+" "+data["last_name"].upper()),
                    'LOC':  str(data["district"]+", "+data["state"]),
                    'DOB':  str(data["dob"]),
                    '121212':  str("__________"),
                    'C_NAME':  str(camp_name),
                    'DATE':  str(start_date),
                    'BATCH':  str(batch_name),
                    'sid': sid
                }

                student_data = {
                    'CADET_NAME': str(data["first_name"].upper()+" "+data["last_name"].upper()),
                    'REGNO': sid,
                    'RANK': '',
                    'C_NAME': camp_name,
                    'C_BATCH': batch_name,
                    'C_DAYS': batch["duration"],
                    'COMP_N': company,
                    'C_DATE': start_date,
                    'PICKPT': data["pick_up_point"],
                    'PICK_TIME': '',
                    'EMP_NAME':  data["employee_who_reached_out_to_you"],
                    'GAR_NAME': "",
                    'ADDRESS': data["address"],
                    'CITY': data["pick_up_city"],
                    'DISTRICT': data["district"],
                    'STATE': data['state'],
                    'PINCODE': data["pincode"],
                    'EMAIL': data["email"],
                    'C_NUM': str(data["phn"]),
                    'WP_NUM': data.get("wp_no", ""),
                    'FATHER_NUM': '',
                    'MOTHER_NUM': '',
                    'DOB': data["dob"],
                    'BLOOD_GROUP':  data.get("blood_group", ""),
                    'STD': data.get("standard", ""),
                    'SCHOOL': data.get("school_name", ""),
                    'FEE_PAID': '',
                    'BALANCE': '',
                    'RECEIPT_NUM': '',
                    'DATE': '',
                    'TIME': ''
                }
                doc = Document('mcf_entrance_card.docx')

                replace_fields_in_document_med(document_med_path, field_values)

                # Replace text fields in paragraphs
                find_and_replace_paragraphs_entrance_card(doc.paragraphs, '{MERGEFIELD CADET_NAME}', student_data['CADET_NAME'])
                find_and_replace_paragraphs_entrance_card(doc.paragraphs, '{MERGEFIELD DATE}', student_data['DATE'])
                find_and_replace_paragraphs_entrance_card(doc.paragraphs, '{MERGEFIELD TIME}', student_data['TIME'])

                for key, value in student_data.items():
                        find_and_replace_tables_entrance_card(doc.tables, f'{{MERGEFIELD {key}}}', str(value))

                try:
                    print("replacing image")
                    table = doc.tables[0]  # Assuming the first table
                    cell = table.cell(0, 3)  # Assuming the first cell in the third column

                    # Clear the content of the cell by removing its paragraphs
                    for paragraph in cell.paragraphs:
                        paragraph.clear()

                    # Add a new paragraph and insert the image
                    paragraph = cell.add_paragraph()
                    run = paragraph.add_run()
                    cadet_photo_url = data["cadetPhoto"]
                    cadet_photo_path = cadet_photo_url.replace("https://files.bnbdevelopers.in","/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/")
                    run.add_picture(cadet_photo_path, width=Inches(0.9))
                except Exception as e:
                    print("Error : ",str(e))

                doc.save(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_entrance_card.docx"))

                # import aspose.words as aw
                # doc = aw.Document(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_entrance_card.docx"))
                # doc.save(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_entrance_card.pdf"))

                convert_to_pdf(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_entrance_card.docx"), str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_entrance_card.pdf"))

                # Load the document template
                doc1 = Document('visit_card.docx')

                # Sample student_data
                student_data1 = {
                    'CADET_NAME': str(data["first_name"].upper()+" "+data["last_name"].upper()),
                    'C_NAME': camp_name,
                    'C_BATCH': batch_name,
                    'ADDRESS': data["address"],
                    'C_NUM': data["phn"],
                    'WP_NUM': data["wp_no"]
                }

                for key, value in student_data1.items():
                        find_and_replace_tables_visiting_card(doc1.tables, f'{{MERGEFIELD {key}}}', str(value))
                
                # image_path_father = 'img_rap.png'
                # image_path_mother = 'rutu.png'
                # image_path_cadet = 'aditi_pic.png'
                # image_path_guardian = 'sai_photo.jpeg'

                # replace_image_in_cell(doc1, table_index=0, row_index=4, column_index=0, image_path=image_path_father)

                # replace_image_in_cell(doc1, table_index=0, row_index=4, column_index=2, image_path=image_path_mother)
                try:
                    cadet_photo_url = data["cadetPhoto"]
                    cadet_photo_path = cadet_photo_url.replace("https://files.bnbdevelopers.in","/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/")

                    image_url_guardian = data["parentGurdianPhoto"]
                    image_path_guardian = image_url_guardian.replace("https://files.bnbdevelopers.in","/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/")
                    
                    replace_image_in_cell(doc1, table_index=0, row_index=4, column_index=6, image_path=cadet_photo_path)
                    replace_image_in_cell(doc1, table_index=0, row_index=4, column_index=8, image_path=image_path_guardian)

                    doc1.save(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_visit_card.docx"))

                    convert_to_pdf(str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_visit_card.docx"), str(str("/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/")+f"{sid}_visit_card.pdf"))
                except Exception as e:
                    print("Error : ", str(e))

                entrance_cert_url = f"https://files.bnbdevelopers.in/mcf_files/{sid}_entrance_card.pdf"
                medical_cert_url = f"https://files.bnbdevelopers.in/mcf_files/{sid}_MEDICAL_CER.pdf"
                visiting_card_url = f"https://files.bnbdevelopers.in/mcf_files/{sid}_visit_card.pdf"

            else:
                return jsonify({"message": "Batch is Already Full !"})
        

        student = {
            "sid": sid,
            "first_name": data["first_name"].upper(),
            "middle_name": data.get("middle_name", "").upper(),
            "last_name": data["last_name"].upper(),
            "email": data["email"],
            "phn": str(data["phn"]),
            "dob": data["dob"],
            "age": str(age),
            "company":company,
            "address": data["address"].upper(),
            "fathers_occupation": data["fathers_occupation"].upper(),
            "mothers_occupation": data["mothers_occupation"].upper(),
            "how_you_got_to_know": data["how_you_got_to_know"].upper(),
            "employee_who_reached_out_to_you": data["employee_who_reached_out_to_you"].upper(),
            "district": data["district"].upper(),
            "state": data["state"].upper(),
            "pincode": str(data["pincode"]),
            "status": "Active",
            "camp_id": data.get("camp_id", ""),
            "camp_category": data.get("camp_category", "").upper(),
            "batch_id": data.get("batch_id", ""),
            "food_option": data.get("food_option", "").upper(),
            # "dress_code": data.get("dress_code", ""),
            "pick_up_city": data.get("pick_up_city", "").upper(),
            "pick_up_point": data.get("pick_up_point", "").upper(),
            "height": data.get("height", ""),
            "weight": data.get("weight", ""),
            "blood_group": data.get("blood_group", ""),
            "payment_option": data.get("payment_option", ""),
            "school_name": data.get("school_name", "").upper(),
            "gender": data.get("gender", "").upper(),
            "standard": data.get("standard", ""),
            "wp_no": data.get("wp_no", ""),
            "medication_physical":data.get("medication_physical"),
            "other_problem":data.get("other_problem"),
            "physical_problem":data.get("physical_problem",""),
            "medication_allergy":data.get("medication_allergy",""),
            "medication_other":data.get("medication_other",""),
            "allergy":data.get("allergy",""),
            "medicalCertificate":medical_cert_url,
            "cadetPhoto":data.get("cadetPhoto",""),
            "cadetSign":data.get("cadetSign",""),
            "parentGurdianPhoto":data.get("parentGurdianPhoto",""),
            "parentGurdianSign":data.get("parentGurdianSign",""),
            "payment_status": data.get("payment_status", "Pending"),
            "entrence_card":entrance_cert_url,
            "visiting_card":visiting_card_url
        }

        # Store the student information in the MongoDB collection
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id":data.get("batch_id")}, {"_id":0})
        if batch:
            if int(batch["students_registered"]) <= int(batch["batch_intake"]):
                students_db.insert_one(student)
                batches_db.update_one({"batch_id": data.get("batch_id")}, {"$set": {"students_registered":int(int(batch["students_registered"])+1)}})
                return jsonify({"message": "Student registered successfully", "sid": sid})
            else:
                return jsonify({"message": "Batch is Already Full !"})
            
        msg = "Dear Parent, Thank you for registering with MCF Camp, for any registration and payment-related query please visit us at www.mcfcamp.in. Or contact us at 9604087000/9604082000, or email us at mcfcamp@gmail.com MARSHAL CADEF"
        sendSMS(msg,str(data["phn"]))

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
        batches_db = db["batches_db"]
        batch = batches_db.find_one({"batch_id":data.get("batch_id")}, {"_id":0})
        if batch:
            if int(batch["students_registered"]) <= int(batch["batch_intake"]):
                students_db.update_one({"sid": data['sid']}, {"$set": student})
                return jsonify({"message": f"Student with sid {data['sid']} updated successfully"})
            else:
                return jsonify({"message": "Batch is Already Full !"}),400
        else:
            return jsonify({"message": "Batch not Found !"}),400
            
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
        print("Data Recieved : ",data)

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
            "camp_place": data["camp_place"],
            "camp_fee": float(data["camp_fee"]),  # assuming camp_fee is a float
            "camp_description": data["camp_description"],
            "fee_discount": float(data["fee_discount"]),  # assuming fee_discount is a float
            # "discount_date": data["discount_date"],
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
    
@app.route('/getAllCampsActive', methods=['GET'])
def get_all_camps_active():
    try:
        camps_db = db["camps_db"]
        camps = camps_db.find({"camp_status":"Active"}, {"_id": 0})  # Exclude the _id field from the response

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
        required_fields = ["batch_name", "start_date", "end_date", "duration", "batch_intake", "camp_id"]
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
        students_db.update_one({"sid": sid}, {"$set": {"status": "Active"}})

        return jsonify({"message": f"Student with sid {sid} is now Active."})

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
        remark = data.get('remark')

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
                "training": training,
                "remark": remark
            }}
        )

        return jsonify({"message": f"Report generated for student with sid {sid}."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/addAdmin', methods=['POST'])
def add_admin():
    try:
        data = request.get_json()

        # Get parameters from the JSON data
        admins_db = db['admins_db']
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        admin_id = str(uuid.uuid4().hex)
        admin = admins_db.find_one({"username": username}, {"_id": 0})
        if admin:
            return jsonify({"success":False,"error":"Username Already Exist"})

        # Check if username and password are provided
        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400  # Bad Request

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Store admin information in the MongoDB collection
        admins_db = db['admins_db']
        admins_db.insert_one({"username": username, "password": hashed_password, "email": email, "admin_id":admin_id})

        return jsonify({"message": "Admin added successfully.","success":True, "admin_id":admin_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

# @app.route('/loginAdmin', methods=['POST'])
# def login_admin():
#     try:
#         data = request.get_json()

#         # Get parameters from the JSON data
#         username = data.get('username')
#         password = data.get('password')

#         # Check if username and password are provided
#         if not username or not password:
#             return jsonify({"error": "Username and password are required.","success":False}), 400  # Bad Request

#         # Find the admin based on username
#         admins_db = db['admins_db']
#         admin = admins_db.find_one({"username": username}, {"_id": 0})

#         if not admin or not check_password_hash(admin.get("password", ""), password):
#             return jsonify({"error": "Invalid username or password."}), 401  # Unauthorized

#         return jsonify({"message": "Login successful.","success":True,"admin_id":admin['admin_id']})

#     except Exception as e:
#         return jsonify({"error": str(e),"success":False}), 500  # Internal Server Error

# Function to create a JWT token
import jwt
def create_jwt_token(admin_id):
    import datetime
    payload = {
        'admin_id': admin_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/loginAdmin', methods=['POST'])
def login_admin():
    try:
        data = request.get_json()

        # Get parameters from the JSON data
        username = data.get('username')
        password = data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return jsonify({"error": "Username and password are required.", "success": False}), 400  # Bad Request

        # Find the admin based on username
        admins_db = db["admins_db"]
        admin = admins_db.find_one({"username": username}, {"_id": 0})

        if not admin or not check_password_hash(admin.get("password", ""), password):
            return jsonify({"error": "Invalid username or password.", "success": False}), 401  # Unauthorized

        # Generate JWT token
        token = create_jwt_token(admin['admin_id'])

        return jsonify({"message": "Login successful.", "success": True, "admin_id": admin['admin_id'], "token": token})

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500  # Internal Server Error

    
@app.route('/getAllAdmin', methods=['GET'])
def get_all_admin():
    try:
        # Retrieve all admin records from the MongoDB collection
        admins_db = db["admins_db"]
        admins = list(admins_db.find({}, {"_id": 0}))

        return jsonify({"admins": admins})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getStudentCounts', methods=['GET'])
def get_student_counts():
    try:
        # Retrieve count of canceled students
        total_students_count = db["students_db"].count_documents({})

        active_students_count = db["students_db"].count_documents({"status": "Active"})

        canceled_students_count = db["students_db"].count_documents({"status": "Cancel"})

        # Retrieve count of refunded students
        refunded_students_count = db["students_db"].count_documents({"status": "Refund"})

        # Retrieve count of extended students
        extended_students_count = db["students_db"].count_documents({"status": "Extend"})

        return jsonify({
            "active_students_count": active_students_count,
            "canceled_students_count": canceled_students_count,
            "refunded_students_count": refunded_students_count,
            "extended_students_count": extended_students_count,
            "total_students_count": total_students_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getCanceledStudents', methods=['GET'])
def get_canceled_students():
    try:
        canceled_students_count = db["students_db"].find({"status": "Cancel"},{"_id":0})

        return jsonify({
            "canceled_students_count": canceled_students_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getRefundStudents', methods=['GET'])
def get_refund_students():
    try:
        # Retrieve count of refunded students
        refunded_students_count = db["students_db"].find({"status": "Refund"},{"_id":0})
        return jsonify({
            "refunded_students_count": refunded_students_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/getExtendedStudents', methods=['GET'])
def get_extended_students():
    try:

        # Retrieve count of extended students
        extended_students_count = db["students_db"].find({"status": "Extend"},{"_id":0})

        return jsonify({
            "extended_students_count": extended_students_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/changeStatus', methods=['PUT'])
def change_student_status():
    try:
        data = request.get_json()

        # Check if sid and new_status are provided
        if 'sid' not in data or 'new_status' not in data or 'reason' not in data:
            return jsonify({"error": "Both 'sid' and 'new_status' are required."}), 400  # Bad Request

        # Find the student based on sid
        students_db = db["students_db"]
        student = students_db.find_one({"sid": data['sid']})

        if not student:
            return jsonify({"error": f"No student found with sid: {data['sid']}"}), 404  # Not Found

        # Update the status of the student
        students_db.update_one({"sid": data['sid']}, {"$set": {"status": data['new_status'],"reason":data['reason']}})

        return jsonify({"message": f"Status for student with sid {data['sid']} updated to {data['new_status']} successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
#-----------------------------------------------------------------------------------

@app.route('/addDiscountCodes', methods=['POST'])
def add_discount_codes():
    try:
        data = request.get_json()

        # Check if discount_code and discount_amount are provided
        if 'discount_code' not in data or 'discount_amount' not in data:
            return jsonify({"error": "Both 'discount_code' and 'discount_amount' are required."}), 400  # Bad Request

        # Generate a unique ID for the discount using UUID
        discount_id = str(uuid.uuid4().hex)

        # Store discount code information in the MongoDB collection
        discount_codes_db = db["discount_codes_db"]
        discount_codes_db.insert_one({
            "discount_id": discount_id,
            "discount_code": data['discount_code'],
            "discount_amount": data['discount_amount']
        })

        return jsonify({"message": f"Discount code '{data['discount_code']}' added successfully.", "discount_id": discount_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@app.route('/getAllDiscounts', methods=['GET'])
def get_all_discounts():
    try:
        discount_codes_db = db["discount_codes_db"]
        discounts = list(discount_codes_db.find({}, {"_id": 0}))

        return jsonify({"discounts": discounts})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@app.route('/getDiscount', methods=['GET'])
def get_discount():
    try:
        discount_id = request.args.get('discount_id')
        if not discount_id:
            return jsonify({"error": "Missing 'discount_id' parameter in the request."}), 400  # Bad Request

        discount_codes_db = db["discount_codes_db"]
        discount = discount_codes_db.find_one({"discount_id": discount_id}, {"_id": 0})

        if not discount:
            return jsonify({"error": f"No discount found with discount_id: {discount_id}"}), 404  # Not Found

        return jsonify({"discount": discount})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error


@app.route('/updateDiscount', methods=['PUT'])
def update_discount():
    try:
        data = request.get_json()

        # Check if discount_id and new_discount_code are provided
        if 'discount_id' not in data or 'new_discount_code' not in data or "discount_amount" not in data:
            return jsonify({"error": "Both 'discount_id' and 'new_discount_code' and 'discount_amount' are required."}), 400  # Bad Request

        discount_codes_db = db["discount_codes_db"]
        discount = discount_codes_db.find_one({"discount_id": data['discount_id']})

        if not discount:
            return jsonify({"error": f"No discount found with discount_id: {data['discount_id']}"}), 404  # Not Found

        # Update the discount_code of the discount
        discount_codes_db.update_one({"discount_id": data['discount_id']}, {"$set": {"discount_code": data['new_discount_code']},"discount_amount":data["discount_amount"]})

        return jsonify({"message": f"Discount with discount_id {data['discount_id']} updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

@app.route('/deleteDiscount', methods=['DELETE'])
def delete_discount():
    try:
        discount_id = request.args.get('discount_id')
        if not discount_id:
            return jsonify({"error": "Missing 'discount_id' parameter in the request."}), 400  # Bad Request

        discount_codes_db = db["discount_codes_db"]
        discount = discount_codes_db.find_one({"discount_id": discount_id})

        if not discount:
            return jsonify({"error": f"No discount found with discount_id: {discount_id}"}), 404  # Not Found

        # Delete the discount from the database
        discount_codes_db.delete_one({"discount_id": discount_id})

        return jsonify({"message": f"Discount with discount_id {discount_id} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
@app.route('/checkDiscountCode', methods=['POST'])
def check_discount_code():
    try:
        data = request.get_json()

        # Check if discount_code is provided
        if 'discount_code' not in data:
            return jsonify({"error": "Missing 'discount_code' parameter in the request."}), 400  # Bad Request

        discount_codes_db = db["discount_codes_db"]
        discount = discount_codes_db.find_one({"discount_code": data['discount_code']}, {"_id": 0, "discount_amount": 1})

        if discount:
            return jsonify({"message": "Valid code", "discount_amount": discount["discount_amount"],"success":True})
        else:
            return jsonify({"message": "Invalid code","success":False})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error
    
file_directory = '/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/mcf_files/'
    
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

        return f'https://files.bnbdevelopers.in/mcf_files/{uid}/{filename}'
    except Exception as e:
        raise e
    
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
    
# Endpoint for requesting password reset (for admin)
@app.route("/sendEntranceCard", methods=["GET"])
def send_entrance_card():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        mailToSend = student_data['email']
        # Send the password reset link via email
        sender_email = "partbarse92@gmail.com"
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login("partbarse92@gmail.com", "xdfrjwaxctwqpzyg")

        message_text = f"Hello {student_data['first_name']}, \n\n You can download your Entrance Card from below Link. \n {student_data['entrence_card']} \n\n You need to print the Entrance Card and Bring to camp in Hardcopy."
        message = MIMEText(message_text)
        message["Subject"] = "MCF Camp Entrance Card"
        message["From"] = sender_email
        message["To"] = mailToSend

        smtp_server.sendmail(sender_email, mailToSend, message.as_string())
        smtp_server.quit()

        return jsonify({'success': True, 'msg': 'Mail Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
    

# Endpoint for requesting password reset (for admin)
@app.route("/sendMedicalCertificate", methods=["GET"])
def send_medical_certificate():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        mailToSend = student_data['email']
        # Send the password reset link via email
        sender_email = "partbarse92@gmail.com"
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login("partbarse92@gmail.com", "xdfrjwaxctwqpzyg")

        message_text = f"Hello {student_data['first_name']}, \n\n You can download your Medical Certificate from below Link. \n {student_data['medicalCertificate']} \n\n You need to print the Medical Certificate and Take a signature from your Doctor and Bring to camp in Hardcopy."
        message = MIMEText(message_text)
        message["Subject"] = "MCF Camp Medical Certificate"
        message["From"] = sender_email
        message["To"] = mailToSend

        smtp_server.sendmail(sender_email, mailToSend, message.as_string())
        smtp_server.quit()

        return jsonify({'success': True, 'msg': 'Mail Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
    
@app.route("/sendVisitingCard", methods=["GET"])
def send_visiting_card():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        mailToSend = student_data['email']
        # Send the password reset link via email
        sender_email = "partbarse92@gmail.com"
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login("partbarse92@gmail.com", "xdfrjwaxctwqpzyg")

        message_text = f"Hello {student_data['first_name']}, \n\n You can download your Visiting Card from below Link. \n {student_data['visiting_card']} \n\n You need to print the Visiting Card and bring to camp for parents to visit Student"
        message = MIMEText(message_text)
        message["Subject"] = "MCF Camp Visiting Card"
        message["From"] = sender_email
        message["To"] = mailToSend

        smtp_server.sendmail(sender_email, mailToSend, message.as_string())
        smtp_server.quit()

        return jsonify({'success': True, 'msg': 'Mail Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
    






# Endpoint for requesting password reset (for admin)
@app.route("/sendEntranceCard_sms", methods=["GET"])
def send_entrance_card_sms():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        entrence_card = student_data["entrence_card"]
        entrence_card_srt = ''
        url = "https://s.mcfcamp.in/shorten"
        data = {
            "url": entrence_card
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            entrence_card_srt = json_data["short_url"]
            print(entrence_card_srt)
        else:
            print("Error:", response.status_code)
        msg = f"Hello, Download Link for your Entrance Card is {entrence_card_srt} \n Team MCF CAMP"
        phn = student_data['phn']
        sendSMS(msg,phn)

        return jsonify({'success': True, 'msg': 'SMS Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500


import requests
# Endpoint for requesting password reset (for admin)
@app.route("/sendMedicalCertificate_sms", methods=["GET"])
def send_medical_certificate_sms():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        medical_cert = student_data["medicalCertificate"]
        medical_cert_srt = ''
        url = "https://s.mcfcamp.in/shorten"
        data = {
            "url": medical_cert
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            medical_cert_srt = json_data["short_url"]
            print(medical_cert_srt)
        else:
            print("Error:", response.status_code)
        msg = f"Hello, Download Link for your Medical Certificate is {medical_cert_srt} \n Team MCF CAMP"
        phn = student_data['phn']
        sendSMS(msg,phn)

        return jsonify({'success': True, 'msg': 'SMS Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
        
    
@app.route("/sendVisitingCard_sms", methods=["GET"])
def send_visiting_card_sms():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        visiting_card = student_data["visiting_card"]
        visiting_card_srt = ''
        url = "https://s.mcfcamp.in/shorten"
        data = {
            "url": visiting_card
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            visiting_card_srt = json_data["short_url"]
            print(visiting_card_srt)
        else:
            print("Error:", response.status_code)
        msg = f"Hello, Download Link for your Visiting Card is {visiting_card_srt} \n Team MCF CAMP"
        phn = student_data['phn']
        sendSMS(msg,phn)

        return jsonify({'success': True, 'msg': 'SMS Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500









@app.route("/sendEntranceCard_wp", methods=["GET"])
def send_entrance_card_wp():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        entrence_card = student_data["entrence_card"]
        entrence_card_srt = ''
        url = "https://s.mcfcamp.in/shorten"
        data = {
            "url": entrence_card
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            entrence_card_srt = json_data["short_url"]
            print(entrence_card_srt)
        else:
            print("Error:", response.status_code)
        msg = f"Hello, Download Link for your Entrance Card is {entrence_card_srt} \n Team MCF CAMP"
        phn = student_data['phn']
        send_wp(msg,phn)

        return jsonify({'success': True, 'msg': 'SMS Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
    

@app.route("/sendMedicalCertificate_wp", methods=["GET"])
def send_medical_certificate_wp():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        medical_cert = student_data["medicalCertificate"]
        medical_cert_srt = ''
        url = "https://s.mcfcamp.in/shorten"
        data = {
            "url": medical_cert
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            medical_cert_srt = json_data["short_url"]
            print(medical_cert_srt)
        else:
            print("Error:", response.status_code)
        msg = f"Hello, Download Link for your Medical Certificate is {medical_cert_srt} \n Team MCF CAMP"
        phn = student_data['phn']
        send_wp(msg,phn)

        return jsonify({'success': True, 'msg': 'SMS Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
    

@app.route("/sendVisitingCard_wp", methods=["GET"])
def send_visiting_card_sms():
    try:
        # collection = db["students_db"]
        sid = request.args.get('sid')
        students_db = db["students_db"]
        student_data = students_db.find_one({"sid":sid}, {"_id":0})
        visiting_card = student_data["visiting_card"]
        visiting_card_srt = ''
        url = "https://s.mcfcamp.in/shorten"
        data = {
            "url": visiting_card
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            json_data = response.json()
            visiting_card_srt = json_data["short_url"]
            print(visiting_card_srt)
        else:
            print("Error:", response.status_code)
        msg = f"Hello, Download Link for your Visiting Card is {visiting_card_srt} \n Team MCF CAMP"
        phn = student_data['phn']
        send_wp(msg,phn)

        return jsonify({'success': True, 'msg': 'SMS Send'}), 200

    except Exception as e:
        return jsonify({'success': False, 'msg': 'Something Went Wrong.', 'reason': str(e)}), 500
    


if __name__ == '__main__':
    app.run(host="0.0.0.0")





