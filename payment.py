import requests
import json
import hashlib
import uuid

def generate_hash(data, salt):
    # key|merchant_txn|name|email|phone|amount|udf1|udf2|udf3|udf4|udf5|message|salt
    concat_string = f"{data[0]}|{data[1]}|{data[2]}|{data[3]}|{data[4]}|{data[5]}|{data[6]}|{data[7]}|{data[8]}|{data[9]}|{data[10]}|{data[11]}|{salt}"
    hashed = hashlib.sha512(concat_string.encode()).hexdigest()
    print(hashed)
    return hashed

def generate_hash_get(data, salt):
    concat_string = f"{data[0]}|{data[1]}|{salt}"
    hashed = hashlib.sha512(concat_string.encode()).hexdigest()
    return hashed

def generate_hash_list(data, salt):
    concat_string = f"{data[0]}|{data[1]}|{data[2]}|{salt}"
    hashed = hashlib.sha512(concat_string.encode()).hexdigest()
    return hashed

def get_easycollect_link(key, merchant_txn, hash_value):
    url = f"https://testdashboard.easebuzz.in/easycollect/v1/get?key={key}&merchant_txn={merchant_txn}&hash={hash_value}"

    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        print("Response:")
        print(json.dumps(response_data, indent=4))
    except Exception as e:
        print("Error:", e)

def get_easycollect_list(s_date, e_date):
    url = "https://testdashboard.easebuzz.in/easycollect/v1/list"

    key = "2PBP7IABZ2"
    data_sequence = [
            key,
            s_date,
            e_date
        ]
    salt = "DAH88E3UWQ"
    hash = generate_hash_list(data_sequence, salt)

    payload = {
        "key": key,
        "hash": hash,
        "date_range": {
            "start_date": s_date,
            "end_date": e_date
        },
        "payment_range": {
            "start_date": s_date,
            "end_date": e_date
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        print("Response:")
        print(json.dumps(response_data, indent=4))
    except Exception as e:
        print("Error:", e)


def create_easycollect_link(mode):
    if mode == "post":
        url = "https://testdashboard.easebuzz.in/easycollect/v1/create"
        name = "Parth"
        email = "parthbarse72@gmail.com"
        phn = "8793015610"
        msg = "Demo Payment"
        amt = "1.00"

        transaction_id = uuid.uuid4().hex
        key = "2PBP7IABZ2"

        # Define the data in the specified sequence for hashing
        data_sequence = [
            key,
            transaction_id,
            name,
            email,
            phn,
            amt,
            "",
            "",
            "",
            "",
            "",
            msg,
        ]
        salt = "DAH88E3UWQ"

        # Generate hash using the data sequence and salt
        hash_value = generate_hash(data_sequence, salt)
        # key|merchant_txn|name|email|phone|amount|udf1|udf2|udf3|udf4|udf5|message|salt
        payload = {
            "key": key,
            "merchant_txn": transaction_id,
            "name": name,
            "email": email,
            "phone": phn,
            "amount": amt,
            "udf1": " ",
            "udf2": " ",
            "udf3": " ",
            "udf4": " ",
            "udf5": " ",
            "message": msg,
            "accept_partial_payment": False,
            "hash": hash_value  # Include the generated hash in the payload
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            print("Response:")
            print(json.dumps(response_data, indent=4))  # Print response data in formatted JSON
            print("testing")
        except Exception as e:
            print("Error:", e)

    elif mode == "get":
        key = "2PBP7IABZ2"
        salt = "DAH88E3UWQ"
        merchant_txn = "2ff10c44f15c4977b02a8f5b9dfc7065"
        data_sequence = [
            key,
            merchant_txn
        ]
        hash_value = generate_hash_get(data_sequence, salt)
        get_easycollect_link(key, merchant_txn, hash_value)

    elif mode == "list":
        s_date = "2024-03-25"
        e_date = "2024-03-28"
        get_easycollect_list(s_date, e_date)

if __name__ == "__main__":
    create_easycollect_link("post")
