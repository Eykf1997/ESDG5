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

inventory_CMS = "http://localhost:5100/inventory_management"
order_URL = "http://localhost:5001/order"
# shipping_record_URL = "http://localhost:5002/shipping_record"
# activity_log_URL = "http://localhost:5003/activity_log"
# error_URL = "http://localhost:5004/error"


@app.route("/place_order", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            print(order)
            result = processPlaceOrder(order)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400






                


def processPlaceOrder(order):

    # 1. Send the order info {cart items}
#################################################################### Invoke the order microservice ######################################################################################################
    print('\n-----Invoking order microservice-----')
    order_result = invoke_http(order_URL, method='POST', json=order)
    print('order_result:', order_result)
    code = order_result["code"]##################################### place this at the last 
    message = json.dumps(order_result)
    
############################################## Error Handling #############################################################
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
            code), order_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure sent for error handling."
        }


############################################################# No error Proceed to Inventory Check & send telegram if stock low ################################################
    else:
        print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')               
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
            body=message)  
    # print('\n\n-----Invoking telegram bot microservice-----')
    # print(inventory_result)
    # bouquetDetail=inventory_result['data']['Details']
    # bouquetQuantity=  abs(inventory_result['data']["Quantity"])

    # #if else check to see whether bouquetQuantity remaining is less than 50
    # if bouquetQuantity<50:
    #     telegram_bot_sendtext(bouquetDetail,bouquetQuantity)
    # # - reply from the invocation is not used;
    # # continue even if this invocation fails



################################################################ 2. Send order to inventory management CMS ##################################################################
    print('\n\n-----Invoking inventory_URL microservice-----')
    inventory_result = invoke_http(inventory_CMS, method="POST", json=order)
    print("\nOrder sent to inventory_URL log.\n")
    print('inventory_result:', inventory_result)
    code = order_result["code"]##################################### place this at the last 
    message = json.dumps(order_result)

############################################## Error Handling #############################################################
    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), order_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"inventory_result": inventory_result},
            "message": "inventory_result failure sent for error handling."
        }







############################################### success return ############################################
    return {
            "code": 201,
        "data": {
            "order_result": order_result,
            "inventory_result": inventory_result
        }

    }


# Execute this program if it is run as a main script (not by 'import')
# if __name__ == "__main__":
#     print("This is flask " + os.path.basename(__file__) +
#           " for placing an order...")
#     app.run(host="0.0.0.0", port=5100, debug=True)

if __name__ == '__main__':

    app.run(port=5000, debug=True)

    
 # 4. Record new order
    # record the activity log anyway
    # print('\n\n-----Invoking activity_log microservice-----')
    # invoke_http(activity_log_URL, method="POST", json=order_result)
    # print("\nOrder sent to activity log.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails


    # Check the order result; if a failure, send it to the error microservice.
    # code = order_result["code"]
    # if code not in range(200, 300):


    # # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as order fails-----')
    # invoke_http(error_URL, method="POST", json=order_result)
    #     # - reply from the invocation is not used; 
    #     # continue even if this invocation fails
    # print("Order status ({:d}) sent to the error microservice:".format(
    # code), order_result)


    # 7. Return error
    # return {
    #     "code": 500,
    #     "data": {"order_result": order_result},
    #     "message": "Order creation failure sent for error handling."
    #     }


    # # 5. Send new order to shipping
    # # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')
    # shipping_result = invoke_http(
    # shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')


    # # Check the shipping result;
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):


    #     # Inform the error microservice
    #     print('\n\n-----Invoking error microservice as shipping fails-----')
    #     invoke_http(error_URL, method="POST", json=shipping_result)
    #     print("Shipping status ({:d}) sent to the error microservice:".format(
    #     code), shipping_result)


    # # 7. Return error
    # return {
    #         "code": 400,
    #         "data": {
    #             "order_result": order_result,
    #             "shipping_result": shipping_result
    #         },
    #         "message": "Simulated shipping record error sent for error handling."
    #     }


    # 7. Return created order, shipping record
