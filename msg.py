import requests

url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"

querystring = {"AUTH_KEY":"39e2807589f775338be0e2e6611d1f7d","message":"message","senderId":"DEMOOS","routeId":"1","mobileNos":"8793015610","smsContentType":"english"}

headers = {
    'Cache-Control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)