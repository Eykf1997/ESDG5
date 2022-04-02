from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

schedule_URL = "http://localhost:5003/schedule"


@app.route("/process_schedule", methods=['POST'])
def process_schedule():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            schedule = request.get_json()
            print("\nReceived a schedule in JSON:", schedule)

            # do the actual work
            # 1. Send order info {cart items}
            print(schedule)
            result = processScheduleManagement(schedule)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "process_schedule.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400






                


def processScheduleManagement(schedule):
    print('\n\n-----Invoking schedule_URL microservice-----')
    schedule_result = invoke_http(schedule_URL, method="POST", json=schedule)
    print("\nSchedule sent to schedule_URL log.\n")
    print('Schedule_result:', schedule_result)
    code = schedule_result["code"]
    message = json.dumps(schedule_result)

    if code not in range(200, 300):

        return {
            "code": 500,
            "data": {"inventory_result": schedule_result},
            "message": "inventory_result failure sent for error handling."
        }

    else:

        print(schedule_result)
        return {
                "code": 201,
            "data": {
                "inventory_result": schedule_result,
            }

        }


if __name__ == '__main__':

    app.run(port=5100, debug=True)
