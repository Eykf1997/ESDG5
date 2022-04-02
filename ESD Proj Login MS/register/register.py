from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# to dockerise the files, change the urls to environ.get("url") then, in the YAML, specify the URLS using like in the lab 
login_URL = os.environ.get("login_URL") 
admin_URL = os.environ.get("admin_URL")
customer_URL = os.environ.get("customer_URL")

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
    result = invoke_http(login_URL + '/' + username, method='GET')
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
            result = invoke_http(admin_URL + "/" + email, method='POST', json = account_details)

        else:
            result = invoke_http(customer_URL + "/" + email, method='POST', json = account_details)

        # check if result returned has error, return error if have
        # print(result)
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
            result = invoke_http(login_URL + "/" + username, method='POST', json = login_details)
            code = result["code"]
            if code != 201:
                return {
                        "code" : result["code"],
                        "message" : result["message"]
                    }
                
            else:
                return {
                        "code" : result["code"],
                        "data" : result["data"],
                        "account_details" : account_details_results
                    }

@app.route("/register/verify_grecaptcha", methods=["POST"])
def verify_grecaptcha():
    try:
        headers = request.headers
        params = {}
        if request.method == "POST":
            if request.is_json:
                params = request.json
            else:
                params = request.args

            method = 'verify_grecaptcha'
            # print(params)
            token = params["response"]
            # print(token)
            key = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
            url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_params = {'secret': key, 'response': token}
            print(recaptcha_params)
            response = requests.post(url, data=recaptcha_params)
            print(response)
            if response.status_code != 200:
                return response.content

            msg = 'success '
            results = response.json()
            print(results)
            return jsonify(results), 200

    except Exception as error:
        return {"error": 'Bad request. ' + str(error)}, 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5003, debug=True)              