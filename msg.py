import requests

url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"

querystring = {"AUTH_KEY":"YourAuthKey"}

payload = "{\"smsContent\":\"Hello Test SMS\",\"groupId\":\"0\",\"routeId\":\"1\",\"mobileNumbers\":\"9999999999\",\"senderId\":\"DEMOOS\",\"signature\":\"signature\",\"smsContentType\":\"english\"}"
headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)