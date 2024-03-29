# # import pygsheets
# # import pandas as pd

# # gc = pygsheets.authorize(service_file='creds.json')

# # # Define the data
# # data = [
# #     {
# #       "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
# #       "productName": "Masala Dosa",
# #       "productPrice": "120",
# #       "productTotalPrice": 240,
# #       "quantity": 2,
# #       "username": "testUser"
# #     },
# #     {
# #       "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
# #       "productName": "Soda",
# #       "productPrice": "40",
# #       "productTotalPrice": 80,
# #       "quantity": 2,
# #       "username": "testUser"
# #     },
# #     {
# #       "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
# #       "productName": "Pizza",
# #       "productPrice": "200",
# #       "productTotalPrice": 600,
# #       "quantity": 3,
# #       "username": "testUser"
# #     }
# # ]

# # df = pd.DataFrame(data)
# # sh = gc.open('Stall-management-data')
# # wks = sh[0]
# # existing_data = wks.get_all_records()
# # combined_data = existing_data + data
# # df_combined = pd.DataFrame(combined_data)
# # wks.set_dataframe(df_combined, start='A1')



# import requests
# import base64

# def send_wp(sms_content, mobile_numbers, file_paths=None):
#     api_url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
#     auth_key = "2b4186d8fc21f47949e7f5e92b56390"
#     route_id = "21"
#     sender_id = "8793015610"
#     sms_content_type = "english"
#     payload = {
#         "smsContent": sms_content,
#         "routeId": route_id,
#         "mobileNumbers": mobile_numbers,
#         "senderId": sender_id,
#         "smsContentType": sms_content_type
#     }
#     headers = {
#         "AUTH_KEY": auth_key,
#         "Content-Type": "application/json"
#     }

#     payload2 = {
#         "smsContent": "",
#         "routeId": route_id,
#         "mobileNumbers": mobile_numbers,
#         "senderId": sender_id,
#         "smsContentType": sms_content_type
#     }

#     # Add file data if file_path is provided
#     if file_paths:
#         if len(file_paths) == 1:
#             filedata_encoded = encode_file_to_base64(file_paths[0])
#             if filedata_encoded:
#                 payload["filename"] = file_paths[0].split('/')[-1]  # Extract filename from path
#                 payload["filedata"] = filedata_encoded
#             else:
#                 print(f"Error: Unable to encode {file_path} to Base64")
#                 return 1
#             response = requests.post(api_url, json=payload, headers=headers)
#             if response.status_code == 200:
#                 response_json = response.json()
#                 if 'response' in response_json:
#                     print("Send WP")
#                     return 0
#                 else:
#                     return 1
#             else:
#                 return 1
#         elif len(file_paths) > 1:
#             for file_path in file_paths:
#                 filedata_encoded = encode_file_to_base64(file_path)
#                 if filedata_encoded:
#                     payload2["filename"] = file_path.split('/')[-1]  # Extract filename from path
#                     payload2["filedata"] = filedata_encoded
#                 else:
#                     print(f"Error: Unable to encode {file_path} to Base64")
#                 response = requests.post(api_url, json=payload2, headers=headers)
#                 if response.status_code == 200:
#                     response_json = response.json()
#                     if 'response' in response_json:
#                         print("Send WP")
#                     else:
#                         print("Error")
#     response = requests.post(api_url, json=payload, headers=headers)
#     if response.status_code == 200:
#         response_json = response.json()
#         if 'response' in response_json:
#             print("Send WP")
#             return 0
#         else:
#             return 1
#     else:
#         return 1



# def encode_file_to_base64(file_path):
#     try:
#         with open(file_path, "rb") as file:
#             filedata = file.read()
#             filedata_encoded = base64.b64encode(filedata).decode('utf-8')
#             return filedata_encoded
#     except Exception as e:
#         print(f"Error encoding file to Base64: {str(e)}")
#         return None

# # Example usage:
# sms_content = "Medical Certificate Template"
# mobile_numbers = "8793015610"
# file_paths = ["medical_certificate.docx", "mcf_entrance_card.docx"]  # Replace with the actual file path

# send_wp(sms_content, mobile_numbers, file_paths)




def generate_3_digit_number(num):
    num_str = str(num)
    padded_num = num_str.zfill(3)
    return padded_num

print(generate_3_digit_number(100))


def sac_table_generator(batch_id, camp_id, intake):
    data = {
        "batch_id":batch_id,
        "camp_id":camp_id,
    }
    for i in range(1, intake):
        num = generate_3_digit_number(i)
        data[num] = "-"
    print(data)

sac_table_generator("00001", "010101", 30)