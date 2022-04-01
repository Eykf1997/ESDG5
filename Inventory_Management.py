from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from telebotEmail import telegram_bot_sendtext
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

inventory_URL = "http://localhost:5002/update_inventory"
#admin_notification = "http://localhost:5001/order"
# shipping_record_URL = "http://localhost:5002/shipping_record"
# activity_log_URL = "http://localhost:5003/activity_log"
# error_URL = "http://localhost:5004/error"


@app.route("/inventory_management", methods=['POST'])
def inventory_management():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            print(order)
            result = processInventoryManagement(order)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "inventory_management.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400






                


def processInventoryManagement(order):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
        # 4. Record new order
    # record the activity log anyway
    print('\n\n-----Invoking inventory_URL microservice-----')
    inventory_result = invoke_http(inventory_URL, method="POST", json=order)
    print("\nOrder sent to inventory_URL log.\n")
    print('order_result:', inventory_result)
    code = inventory_result["code"]
    message = json.dumps(inventory_result)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), inventory_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"inventory_result": inventory_result},
            "message": "inventory_result failure sent for error handling."
        }

    else:

        # print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')               
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
        #     body=message)  
############################################################# No error Proceed to Inventory Check & send telegram if stock low ################################################

        print('\n\n-----Invoking telegram bot microservice-----')
        print(inventory_result)
        bouquetDetail=inventory_result['data']['Details']
        bouquetQuantity=  abs(inventory_result['data']["Quantity"])

    #if else check to see whether bouquetQuantity remaining is less than 50
    if bouquetQuantity<50:
        telegram_bot_sendtext(bouquetDetail,bouquetQuantity)
    # - reply from the invocation is not used;
    # continue even if this invocation fails


   

    return {
            "code": 201,
        "data": {
            "inventory_result": inventory_result,
            # "shipping_result": shipping_result
        }

    }


# Execute this program if it is run as a main script (not by 'import')
# if __name__ == "__main__":
#     print("This is flask " + os.path.basename(__file__) +
#           " for placing an order...")
#     app.run(host="0.0.0.0", port=5100, debug=True)

if __name__ == '__main__':

    app.run(port=5100, debug=True)

    
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
