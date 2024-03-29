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

def generate_hash_get2(data, salt):
    concat_string = f"{data[0]}|{data[1]}|{salt}"
    hashed = hashlib.sha512(concat_string.encode()).hexdigest()
    return hashed

def get_easycollect_link(key, merchant_txn, hash_value):
    url = f"https://dashboard.easebuzz.in/easycollect/v1/get?key={key}&merchant_txn={merchant_txn}&hash={hash_value}"
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

def get2_easycollect_link(merchant_txn):
    url = f"https://dashboard.easebuzz.in/transaction/v2/retrieve"
    key = "1YUG4UBN1Q"
    data_sequence = [
            key,
            merchant_txn
        ]
    salt = "KPRYL60DC1"
    hash = generate_hash_get2(data_sequence, salt)

    payload = {
        "key": key,
        "txnid":merchant_txn,
        "hash": hash,
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
        resp = json.dumps(response_data, indent=4)
        # print(response_data['msg']['status'])
    except Exception as e:
        print("Error:", e)


def get_easycollect_list(s_date, e_date):
    url = "https://dashboard.easebuzz.in/easycollect/v1/list"

    key = "1YUG4UBN1Q"
    data_sequence = [
            key,
            s_date,
            e_date
        ]
    salt = "KPRYL60DC1"
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
        url = "https://dashboard.easebuzz.in/easycollect/v1/create"
        name = "Parth"
        email = "parthbarse72@gmail.com"
        phn = "8793015610"
        msg = "Demo Payment"
        amt = "1.00"
        sid = "ADFSD0930220FVS9012"
        transaction_id = uuid.uuid4().hex
        key = "1YUG4UBN1Q"

        # Define the data in the specified sequence for hashing
        data_sequence = [
            key,
            transaction_id,
            name,
            email,
            phn,
            amt,
            sid,
            "",
            "",
            "",
            "",
            msg,
        ]
        salt = "KPRYL60DC1"

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
            "udf1": sid,
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
        key = "1YUG4UBN1Q"
        salt = "KPRYL60DC1"
        merchant_txn = "f1f3933ceb1d445a8f85bb605f3d2de3"
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

    elif mode == "get2":
        merchant_txn = "7ac648b629604a5393c3054f4870100d"
        get2_easycollect_link(merchant_txn)

if __name__ == "__main__":
    # create_easycollect_link("post")
    create_easycollect_link("get2")



'''
{
    "status": true,
    "data": {
        "id": 22872490,
        "name": "Parth",
        "email": "parthbarse72@gmail.com",
        "amount": "1.00",
        "merchant_txn": "f1f3933ceb1d445a8f85bb605f3d2de3",
        "phone": "8793015610",
        "payment_made": 0,
        "state": "active",
        "sms_count": 0,
        "email_count": 0,
        "message": "Demo Payment",
        "udf1": "",
        "udf2": "",
        "udf3": "",
        "udf4": "",
        "udf5": "",
        "expiry_date": "02-04-2024",
        "quick_pay_transaction_date": null,
        "offline_payment_id": null,
        "offline_payment_desc": null,
        "offline_payment_mode": null,
        "created_date": "2024-03-28T18:08:19.155792+05:30",
        "updated_date": "2024-03-28T18:08:19.155811+05:30",
        "min_amount": "0.00",
        "max_amount": "0.00",
        "sms_channel_count": 0,
        "email_channel_count": 0,
        "sms_credit": 0,
        "email_credit": 0,
        "transaction_id": "NA",
        "submerchant_id": null,
        "whatsapp_count": 0,
        "whatsapp_channel_count": 0,
        "whatsapp_credit": 0,
        "split_payments": null,
        "split_percentage": null,
        "obd_count": 0,
        "obd_credit": 0,
        "payment_type": "SP",
        "is_auto_debit_link": false,
        "auth_details": null,
        "is_auto_debit_seamless": false,
        "entity_type": "Root",
        "partial_payment_due_amount": 1.0,
        "amount_collected_so_far": 0.0,
        "payment_url": "https://pay.easebuzz.in/easy_collect/956b5c36d4074273963e4891a29e8b65",
        "accept_partial_payment": false,
        "short_url": "https://ec.ease.buzz/a/ecHFQ0MK"
    },
    "message": "Link Created Successfully"
}
'''


"""
{
    "msg": {
        "txnid": "f1f3933ceb1d445a8f85bb605f3d2de3",
        "firstname": "Parth",
        "email": "parthbarse72@gmail.com",
        "phone": "8793015610",
        "key": "1YUG4UBN1Q",
        "mode": "UPI",
        "unmappedstatus": "NA",
        "cardCategory": "NA",
        "addedon": "2024-03-28 12:38:27",
        "payment_source": "Easebuzz",
        "PG_TYPE": "NA",
        "bank_ref_num": "408859351991",
        "bankcode": "NA",
        "error": "APPROVED OR COMPLETED SUCCESSFULLY",
        "error_Message": "APPROVED OR COMPLETED SUCCESSFULLY",
        "name_on_card": "NA",
        "upi_va": "parxxxxx@ybl",
        "cardnum": "NA",
        "issuing_bank": "NA",
        "easepayid": "E240328JGFEI1F",
        "amount": "1.0",
        "net_amount_debit": "1.0",
        "cash_back_percentage": "50.0",
        "deduction_percentage": "0.0",
        "merchant_logo": "NA",
        "surl": "https://pay.easebuzz.in/webservice/success_url",
        "furl": "https://pay.easebuzz.in/webservice/success_url",
        "productinfo": "EasyCollect Payment",
        "udf10": "",
        "udf9": "",
        "udf8": "",
        "udf7": "",
        "udf6": "",
        "udf5": "",
        "udf4": "",
        "udf3": "",
        "udf2": "",
        "udf1": "",
        "card_type": "UPI",
        "hash": "aaff6a9f4f4afec6e314d5179a85f479c16a66b7935c275e5e8588253f512e86d5df5314dce448d2b374e31c3362785128e69ef5aa45909a65d1b2ba105055c0",
        "status": "success",
        "bank_name": "NA",
        "auth_code": ""
    },
    "status": true
}
"""