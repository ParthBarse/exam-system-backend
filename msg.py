import requests

def send_wp(api_url, auth_key, sms_content, route_id, mobile_numbers, sender_id, sms_content_type):
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
            return response_json['response']
        else:
            return "Response does not contain 'response' key."
    else:
        return "Error: " + str(response.status_code)
    
api_url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
auth_key = "2b4186d8fc21f47949e7f5e92b56390"
sms_content = "Hello, This is Test Message"
route_id = "21"
mobile_numbers = "8793015610"
sender_id = "8793015610"
sms_content_type = "english"

response = send_wp(api_url, auth_key, sms_content, route_id, mobile_numbers, sender_id, sms_content_type)
