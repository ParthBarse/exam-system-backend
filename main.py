# # # # # import pygsheets
# # # # # import pandas as pd

# # # # # gc = pygsheets.authorize(service_file='creds.json')

# # # # # # Define the data
# # # # # data = [
# # # # #     {
# # # # #       "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
# # # # #       "productName": "Masala Dosa",
# # # # #       "productPrice": "120",
# # # # #       "productTotalPrice": 240,
# # # # #       "quantity": 2,
# # # # #       "username": "testUser"
# # # # #     },
# # # # #     {
# # # # #       "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
# # # # #       "productName": "Soda",
# # # # #       "productPrice": "40",
# # # # #       "productTotalPrice": 80,
# # # # #       "quantity": 2,
# # # # #       "username": "testUser"
# # # # #     },
# # # # #     {
# # # # #       "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
# # # # #       "productName": "Pizza",
# # # # #       "productPrice": "200",
# # # # #       "productTotalPrice": 600,
# # # # #       "quantity": 3,
# # # # #       "username": "testUser"
# # # # #     }
# # # # # ]

# # # # # df = pd.DataFrame(data)
# # # # # sh = gc.open('Stall-management-data')
# # # # # wks = sh[0]
# # # # # existing_data = wks.get_all_records()
# # # # # combined_data = existing_data + data
# # # # # df_combined = pd.DataFrame(combined_data)
# # # # # wks.set_dataframe(df_combined, start='A1')



# # # # import requests
# # # # import base64

# # # # def send_wp(sms_content, mobile_numbers, file_paths=None):
# # # #     api_url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
# # # #     auth_key = "2b4186d8fc21f47949e7f5e92b56390"
# # # #     route_id = "21"
# # # #     sender_id = "8793015610"
# # # #     sms_content_type = "english"
# # # #     payload = {
# # # #         "smsContent": sms_content,
# # # #         "routeId": route_id,
# # # #         "mobileNumbers": mobile_numbers,
# # # #         "senderId": sender_id,
# # # #         "smsContentType": sms_content_type
# # # #     }
# # # #     headers = {
# # # #         "AUTH_KEY": auth_key,
# # # #         "Content-Type": "application/json"
# # # #     }

# # # #     payload2 = {
# # # #         "smsContent": "",
# # # #         "routeId": route_id,
# # # #         "mobileNumbers": mobile_numbers,
# # # #         "senderId": sender_id,
# # # #         "smsContentType": sms_content_type
# # # #     }

# # # #     # Add file data if file_path is provided
# # # #     if file_paths:
# # # #         if len(file_paths) == 1:
# # # #             filedata_encoded = encode_file_to_base64(file_paths[0])
# # # #             if filedata_encoded:
# # # #                 payload["filename"] = file_paths[0].split('/')[-1]  # Extract filename from path
# # # #                 payload["filedata"] = filedata_encoded
# # # #             else:
# # # #                 print(f"Error: Unable to encode {file_path} to Base64")
# # # #                 return 1
# # # #             response = requests.post(api_url, json=payload, headers=headers)
# # # #             if response.status_code == 200:
# # # #                 response_json = response.json()
# # # #                 if 'response' in response_json:
# # # #                     print("Send WP")
# # # #                     return 0
# # # #                 else:
# # # #                     return 1
# # # #             else:
# # # #                 return 1
# # # #         elif len(file_paths) > 1:
# # # #             for file_path in file_paths:
# # # #                 filedata_encoded = encode_file_to_base64(file_path)
# # # #                 if filedata_encoded:
# # # #                     payload2["filename"] = file_path.split('/')[-1]  # Extract filename from path
# # # #                     payload2["filedata"] = filedata_encoded
# # # #                 else:
# # # #                     print(f"Error: Unable to encode {file_path} to Base64")
# # # #                 response = requests.post(api_url, json=payload2, headers=headers)
# # # #                 if response.status_code == 200:
# # # #                     response_json = response.json()
# # # #                     if 'response' in response_json:
# # # #                         print("Send WP")
# # # #                     else:
# # # #                         print("Error")
# # # #     response = requests.post(api_url, json=payload, headers=headers)
# # # #     if response.status_code == 200:
# # # #         response_json = response.json()
# # # #         if 'response' in response_json:
# # # #             print("Send WP")
# # # #             return 0
# # # #         else:
# # # #             return 1
# # # #     else:
# # # #         return 1



# # # # def encode_file_to_base64(file_path):
# # # #     try:
# # # #         with open(file_path, "rb") as file:
# # # #             filedata = file.read()
# # # #             filedata_encoded = base64.b64encode(filedata).decode('utf-8')
# # # #             return filedata_encoded
# # # #     except Exception as e:
# # # #         print(f"Error encoding file to Base64: {str(e)}")
# # # #         return None

# # # # # Example usage:
# # # # sms_content = "Medical Certificate Template"
# # # # mobile_numbers = "8793015610"
# # # # file_paths = ["medical_certificate.docx", "mcf_entrance_card.docx"]  # Replace with the actual file path

# # # # send_wp(sms_content, mobile_numbers, file_paths)




# # # def generate_3_digit_number(num):
# # #     num_str = str(num)
# # #     padded_num = num_str.zfill(3)
# # #     return padded_num

# # # print(generate_3_digit_number(100))


# # # def sac_table_generator(batch_id, camp_id, intake):
# # #     data = {
# # #         "batch_id":batch_id,
# # #         "camp_id":camp_id,
# # #     }
# # #     for i in range(1, intake):
# # #         num = generate_3_digit_number(i)
# # #         data[num] = "-"
# # #     print(data)

# # # sac_table_generator("00001", "010101", 30)

# # new_data = {
# #     "details": {
# #         "name": "VIRAJ TODKAR",
# #         "email": "ajit.todkar@gmail.com",
# #         "phone": "9323047766",
# #         "address": "C1005 SRUSHTI RESIDENCY KHAMBALAPADA ROAD DOMBIVALI EAST , NEAR MATOSHREE HOTEL C1005 SRUSHTI RESIDENCY KHAMBALAPADA ROAD DOMBIVALI EAST , NEAR MATOSHREE HOTEL 421201",
# #         "camp_name": "COMMANDO TRAINING CAMP -2024 (CTC)",
# #         "pickup_point": "KOPARKHAIRANE"
# #     },
# #     "activities": {
# #         "skill_activities": [
# #             {
# #                 "SR.NO.": 1,
# #                 "SKILL": "Archery",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 2,
# #                 "SKILL": "Lathi-Kathi",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 3,
# #                 "SKILL": "Rifle Shooting",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 4,
# #                 "SKILL": "Martial Arts",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 5,
# #                 "SKILL": "Horse Riding",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 6,
# #                 "SKILL": "Pistol Shooting",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "physical_activities": [
# #             {
# #                 "SR.NO.": 7,
# #                 "SKILL": "Trekking",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 8,
# #                 "SKILL": "Aerobics/Yoga",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 9,
# #                 "SKILL": "P.T. and Mass P.T.Execise",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 10,
# #                 "SKILL": "March Past/Drill",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 11,
# #                 "SKILL": "Commando Activities",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "water_activities": [
# #             {
# #                 "SR.NO.": 12,
# #                 "SKILL": "Rain Dance",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 13,
# #                 "SKILL": "Swimming",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "adventure_activities": [
# #             {
# #                 "SR.NO.": 15,
# #                 "SKILL": "Rock Climbing",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 16,
# #                 "SKILL": "Zip Line",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 17,
# #                 "SKILL": "Rappelling",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "mcf_rope_course_activities": [
# #             {
# #                 "SR.NO.": 18,
# #                 "SKILL": "Rope Bridge",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 19,
# #                 "SKILL": "Ladder Walking",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 20,
# #                 "SKILL": "Single Rope Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 21,
# #                 "SKILL": "Zig Zag Ladder Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 22,
# #                 "SKILL": "One Feet Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 23,
# #                 "SKILL": "Straight Line Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "cultural_activities": [
# #             {
# #                 "SR.NO.": 24,
# #                 "SKILL": "Camp Fire",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 25,
# #                 "SKILL": "Karaoke",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "Obstacle_course_activities": [
# #             {
# #                 "SR.NO.": 26,
# #                 "SKILL": "Straight Balance",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 27,
# #                 "SKILL": "Clear Jump",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 28,
# #                 "SKILL": "Double Walt ",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 29,
# #                 "SKILL": "Zig Zag",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 30,
# #                 "SKILL": "Double Jump",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 31,
# #                 "SKILL": "Wall Climbing",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 32,
# #                 "SKILL": "Tire Jump",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 33,
# #                 "SKILL": "Tarzan Swing",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "disaster_management_activities": [
# #             {
# #                 "SR.NO.": 34,
# #                 "SKILL": "First Aid",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 35,
# #                 "SKILL": "Bandage",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 36,
# #                 "SKILL": "Knots",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "military_obstacle_activities": [
# #             {
# #                 "SR.NO.": 37,
# #                 "SKILL": "Commando Net",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 38,
# #                 "SKILL": "Spider Net",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 39,
# #                 "SKILL": "Verticle Net",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "Team_building_activities": [
# #             {
# #                 "SR.NO.": 40,
# #                 "SKILL": "Group Activities",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 41,
# #                 "SKILL": "Sports Activities",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ]
# #     },
# #     "dates": {
# #         "checkin_Date": "",
# #         "pickup_Date": "",
# #         "checkout_Date": "",
# #         "drop_Date": "",
# #         "last_closing_ceremony": ""
# #     },
# #     "individual_remarks_form": {
# #         "time_management": "",
# #         "accommodation": "",
# #         "facilities": "",
# #         "ins_training": "",
# #         "atmosphere": "",
# #         "activity": "",
# #         "uniform": "",
# #         "certification": "",
# #         "suggestion": "",
# #         "best_achievement": "",
# #         "achievement": "",
# #         "personality_dimensions": ""
# #     },
# #     "individual_remarks_table": {
# #         "LEADERSHIP POTENTIAL": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "COMMUNICATION SKILLS": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "TEAMWORK AND COOPERATION": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "ADAPTABILITY AND FLEXIBILITY": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "PROBLEM-SOLVING ABILITY": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         }
# #     },
# #     "final_remarks": {
# #         "Parents presence": "",
# #         "best activity": "",
# #         "remarks": "",
# #         "checked by name": "",
# #         "rank": "",
# #         "overall assessment": ""
# #     }
# # }

# # student_data1 = {
# #             'REG_NO': "",
# #             'CADET_NAME': new_data['details']['name'],
# #             'START_DATE': "",
# #             'END_DATE':"",
# #             'CQY': ''
# #         }

# # print(new_data['details']['name'])
# # print(new_data['activities']['skill_activities'][0]['TIMES TO REPEAT'])


# # {
# #     "details": {
# #         "name": "VIRAJ TODKAR",
# #         "email": "ajit.todkar@gmail.com",
# #         "phone": "9323047766",
# #         "address": "C1005 SRUSHTI RESIDENCY KHAMBALAPADA ROAD DOMBIVALI EAST , NEAR MATOSHREE HOTEL C1005 SRUSHTI RESIDENCY KHAMBALAPADA ROAD DOMBIVALI EAST , NEAR MATOSHREE HOTEL 421201",
# #         "camp_name": "COMMANDO TRAINING CAMP -2024 (CTC)",
# #         "pickup_point": "KOPARKHAIRANE",
# #         "cqy_name": "jk",
# #         "incharge_name": "ll"
# #     },
# #     "activities": {
# #         "skill_activities": [
# #             {
# #                 "SR.NO.": 1,
# #                 "SKILL": "Archery",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 2,
# #                 "SKILL": "Lathi-Kathi",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 3,
# #                 "SKILL": "Rifle Shooting",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 4,
# #                 "SKILL": "Martial Arts",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 5,
# #                 "SKILL": "Horse Riding",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 6,
# #                 "SKILL": "Pistol Shooting",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "physical_activities": [
# #             {
# #                 "SR.NO.": 7,
# #                 "SKILL": "Trekking",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 8,
# #                 "SKILL": "Aerobics/Yoga",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 9,
# #                 "SKILL": "P.T. and Mass P.T.Execise",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 10,
# #                 "SKILL": "March Past/Drill",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 11,
# #                 "SKILL": "Commando Activities",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "water_activities": [
# #             {
# #                 "SR.NO.": 12,
# #                 "SKILL": "Rain Dance",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 13,
# #                 "SKILL": "Swimming",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "adventure_activities": [
# #             {
# #                 "SR.NO.": 15,
# #                 "SKILL": "Rock Climbing",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 16,
# #                 "SKILL": "Zip Line",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 17,
# #                 "SKILL": "Rappelling",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "mcf_rope_course_activities": [
# #             {
# #                 "SR.NO.": 18,
# #                 "SKILL": "Rope Bridge",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 19,
# #                 "SKILL": "Ladder Walking",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 20,
# #                 "SKILL": "Single Rope Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 21,
# #                 "SKILL": "Zig Zag Ladder Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 22,
# #                 "SKILL": "One Feet Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 23,
# #                 "SKILL": "Straight Line Walk",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "cultural_activities": [
# #             {
# #                 "SR.NO.": 24,
# #                 "SKILL": "Camp Fire",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 25,
# #                 "SKILL": "Karaoke",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "Obstacle_course_activities": [
# #             {
# #                 "SR.NO.": 26,
# #                 "SKILL": "Straight Balance",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 27,
# #                 "SKILL": "Clear Jump",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 28,
# #                 "SKILL": "Double Walt ",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 29,
# #                 "SKILL": "Zig Zag",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 30,
# #                 "SKILL": "Double Jump",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 31,
# #                 "SKILL": "Wall Climbing",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 32,
# #                 "SKILL": "Tire Jump",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 33,
# #                 "SKILL": "Tarzan Swing",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "disaster_management_activities": [
# #             {
# #                 "SR.NO.": 34,
# #                 "SKILL": "First Aid",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 35,
# #                 "SKILL": "Bandage",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 36,
# #                 "SKILL": "Knots",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "military_obstacle_activities": [
# #             {
# #                 "SR.NO.": 37,
# #                 "SKILL": "Commando Net",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 38,
# #                 "SKILL": "Spider Net",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 39,
# #                 "SKILL": "Verticle Net",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ],
# #         "Team_building_activities": [
# #             {
# #                 "SR.NO.": 40,
# #                 "SKILL": "Group Activities",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             },
# #             {
# #                 "SR.NO.": 41,
# #                 "SKILL": "Sports Activities",
# #                 "TIMES TO REPEAT": 0,
# #                 "TRAINED BY INS": ""
# #             }
# #         ]
# #     },
# #     "dates": {
# #         "checkin_Date": "",
# #         "pickup_Date": "",
# #         "checkout_Date": "",
# #         "drop_Date": "",
# #         "last_closing_ceremony": ""
# #     },
# #     "individual_remarks_form": {
# #         "time_management": "",
# #         "accommodation": "",
# #         "facilities": "",
# #         "ins_training": "",
# #         "atmosphere": "",
# #         "activity": "",
# #         "uniform": "",
# #         "certification": "",
# #         "suggestion": "",
# #         "best_achievement": "",
# #         "achievement": "",
# #         "personality_dimensions": ""
# #     },
# #     "individual_remarks_table": {
# #         "LEADERSHIP POTENTIAL": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "COMMUNICATION SKILLS": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "TEAMWORK AND COOPERATION": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "ADAPTABILITY AND FLEXIBILITY": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         },
# #         "PROBLEM-SOLVING ABILITY": {
# #             "SCORE": "",
# #             "INTERPRETATION": ""
# #         }
# #     },
# #     "final_remarks": {
# #         "Parents presence": "",
# #         "best activity": "",
# #         "remarks": "",
# #         "checked by name": "",
# #         "rank": "",
# #         "overall assessment": ""
# #     }
# # }


# def number_to_words(num):
#     # Define lists of words for numbers
#     units = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
#     teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
#     tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
#     thousands = ['', 'Thousand', 'Million', 'Billion', 'Trillion']

#     # Function to convert numbers less than 1000 to words
#     def helper(num):
#         if num == 0:
#             return ''
#         elif num < 10:
#             return units[num]
#         elif num < 20:
#             return teens[num - 10]
#         elif num < 100:
#             return tens[num // 10 - 2] + ' ' + helper(num % 10)
#         else:
#             return units[num // 100] + ' Hundred ' + helper(num % 100)

#     if num == 0:
#         return 'Zero'

#     # Separate integer and fractional parts
#     integer_part = int(num)
#     fractional_part = int((num - integer_part) * 100)

#     integer_words = ''
#     for i in range(len(thousands)):
#         if integer_part % 1000 != 0:
#             integer_words = helper(integer_part % 1000) + thousands[i] + ' ' + integer_words
#         integer_part //= 1000

#     fractional_words = ''
#     if fractional_part > 0:
#         fractional_words = 'Point ' + helper(fractional_part)

#     words = integer_words.strip()
#     if fractional_words:
#         words += ' ' + fractional_words

#     return words.strip()


# # Example usage
# print(number_to_words(1234.89))  # Output: One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven Point Eight Nine


import jwt

def create_jwt_token(admin_id):
    import datetime
    payload = {
        'admin_id': admin_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
    }
    token = jwt.encode(payload, "a6d217d048fdcd227661b755", algorithm='HS256')
    return token

print(create_jwt_token("admin123123"))

def decode_jwt_token(token, secret_key):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."

# Assuming you have a secret key
SECRET_KEY = "a6d217d048fdcd227661b755"

# Example usage
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbl9pZCI6ImFkbWluMTIzMTIzIiwiZXhwIjoxNzEyNjY2NDYwfQ.gWghoR0RGhsx8kN-O96eu2nBS2tGoAjJ7YWb7FF9Rz4"
decoded_message = decode_jwt_token(token, SECRET_KEY)

print(decoded_message['admin_id'])
