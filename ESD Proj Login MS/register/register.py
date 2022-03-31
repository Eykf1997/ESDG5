from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# book_URL = "http://localhost:5000/book"
# order_URL = "http://localhost:5001/order"
# shipping_record_URL = "http://localhost:5002/shipping_record"
# activity_log_URL = "http://localhost:5003/activity_log"
# error_URL = "http://localhost:5004/error"

login_URL = "http://localhost:5000/login/"
admin_URL = "http://localhost:5002/admin/"
customer_URL = "http://localhost:5001/customer/"

# register_details should contain details for admin/customer(email, name), password, username and creating admin or customer
# for now, just take it that it is an input
# {"email", "name", "password", "username", "account_type"}
# this means that the UI must contain fields for these details
# then when get back the results from admin/customer
# use the id to create login with the password 


@app.route("/register", methods=['POST'])
def register():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            register_details = request.get_json()
            print("\nReceived registration details in JSON:", register_details)

            # do the actual work
            # 1. Send order info {cart items}
            result = processRegister(register_details)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "register.py internal error: " + ex_str
            }), 500

def processRegister(register_details):
    # possible to check admin/customer first then check existence of username

    # invoke login to check whether username exists
    # then invoke admin/customer to check email exists
    print('\n-----Invoking login microservice-----')
    username = register_details["username"]
    result = invoke_http(login_URL + username, method='GET')
    code = result["code"]

    if code == 200:
        return {
                "code": 409,
                "message": "Username already taken."
            }
  

    # invoke admin/customer to create new entry
    else:
        email = register_details["email"]
        account_type = register_details["account_type"]
        account_details = {"name" : register_details["name"]}

        if account_type == "admin":
            result = invoke_http(admin_URL + email, method='POST', json = account_details)

        else:
            result = invoke_http(customer_URL + email, method='POST', json = account_details)

        # check if result returned has error, return error if have
        print(result)
        code = result["code"]
        if code != 201:
            return {
                    "code" : code,
                    "message" : result["message"]
                }
            

    # then from json returned from creating new admin/customer, create login
        else:
            account_details_results = result
            data = result["data"]
            account_id = account_type + "_id"
            login_details = {"password" : register_details["password"], account_id : data[account_id]}
            result = invoke_http(login_URL + username, method='POST', json = login_details)
            code = result["code"]
            if code != 201:
                return {
                        "code" : result["code"],
                        "message" : result["message"]
                    }
                
            else:
                return {
                        "code" : result["code"],
                        "data" : result["data"]
                    }



if __name__ == '__main__':
    app.run(port=5003, debug=True)              