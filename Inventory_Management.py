from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

from datetime import date,datetime

app = Flask(__name__)
CORS(app)

# inventory_URL = "http://localhost:5002/update_inventory"
inventory_URL = os.environ.get("inventory_URL")
# telegram_URL = "http://localhost:5101/telegramNotificationDate"
telegram_URL = os.environ.get("telegram_URL")
# bouquet_URL = "http://localhost:5002/backendInventoryManagement"
bouquet_URL = os.environ.get("bouquet_URL")
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
    print('inventory_result:', inventory_result)
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
        data = []
        for item in inventory_result['data']:
            
            bouquetQuantity =  abs(item["Quantity"])

            if bouquetQuantity<50:
                print('\n\n-----Invoking Telegram microservice-----')
                telegram_result =  invoke_http(telegram_URL, method="POST", json=item)
                
                code = telegram_result["code"]##################################### place this at the last 
                data.append(json.dumps(telegram_result))
                # data.append(telegram_result)
                # print(data) 

                #message = json.dumps(telegram_result)
                
        
            ############################################## Error Handling #############################################################
                if code not in range(200, 300):
                    # Inform the error microservice
                    #print('\n\n-----Invoking error microservice as order fails-----')
                    print('\n\n-----Publishing the (order error) message with routing_key=telegram.error-----')
                    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="telegram.error", 
                        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

                    # - reply from the invocation is not used;
                    # continue even if this invocation fails        
                    print("\nTelegram Error({:d}) published to the RabbitMQ Exchange:".format(
                        code), telegram_result)

                    # 7. Return error
                    return {
                        "code": 500,
                        "data": {"telegram_result": telegram_result},
                        "message": "telegram_result failure sent for error handling."
                    }
            else:
                print('\n\n-----Publishing the (telegram) message with routing_key=success.telegram-----')
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="success.telegram", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))               



    return {
            "code": 201,
        "data": {
            "inventory_result": inventory_result,
            "telegram_result": telegram_result
        }

    }





# invoke inventory.py when admin performs delete function, when there is error, it sends to error ms, send to activity log

@app.route("/bouquet", methods=['DELETE'])
def backendInventoryManagementDelete():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            print(order)
            result = processBackendInventoryManagementDelete(order)
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



def processBackendInventoryManagementDelete(order):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
        # 4. Record new order
    # record the activity log anyway
    item_id = str(order['Item_Id'])
    print(item_id)
    print('2')
    flower_URL = bouquet_URL + '/' + item_id
    print('\n\n-----Invoking inventory_URL microservice-----')
    bouquet_del = invoke_http(flower_URL, method="DELETE", json=order)
    print("\nOrder sent to bouquet_URL log.\n")
    print('order_result:', bouquet_del)
    code = bouquet_del["code"]
    message = json.dumps(bouquet_del)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (backend deleting error) message with routing_key=backend.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="backend.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), bouquet_del)

        # 7. Return error
        return {
            "code": 500,
            "data": {"inventory_result": bouquet_del},
            "message": "inventory_result failure sent for error handling."
        }

    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="backend.delete", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')               
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
        #     body=message)  
############################################################# No error Proceed to Inventory Check & send telegram if stock low ################################################

        return {
                "code": 201,
            "data": {
                "inventory_result": bouquet_del,
                # "shipping_result": shipping_result
            }

        }


# invoke inventory.py when admin performs UPDATE function, when there is error, it sends to error ms, send to activity log


@app.route("/bouquet", methods=['PUT'])
def backendInventoryManagementUpdate():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            backendInfo = request.get_json()
            print("\nReceived an order in JSON:", backendInfo)

            # do the actual work
            # 1. Send order info {cart items}
            print(backendInfo)
            result = processBackendInventoryManagementUpdate(backendInfo)
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



def processBackendInventoryManagementUpdate(backendInfo):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
        # 4. Record new order
    # record the activity log anyway
    item_id = str(backendInfo['Item_Id'])
    print(item_id)
    flower_URL = bouquet_URL + '/' + item_id
    print('\n\n-----Invoking inventory_URL microservice-----')
    bouquet_update = invoke_http(flower_URL, method="PUT", json=backendInfo)
    print("\nOrder sent to bouquet_URL log.\n")
    print('order_result:', bouquet_update)
    code = bouquet_update["code"]
    message = json.dumps(bouquet_update)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (backend update error) message with routing_key=backend.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="backend.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), bouquet_update)

        # 7. Return error
        return {
            "code": 500,
            "data": {"inventory_result": bouquet_update},
            "message": "inventory_result failure sent for error handling."
        }

    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="backend.update", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')               
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
        #     body=message)  
############################################################# No error Proceed to Inventory Check & send telegram if stock low ################################################

        return {
                "code": 201,
            "data": {
                "inventory_result": bouquet_update,
                # "shipping_result": shipping_result
            }

        }



# invoke inventory.py when admin performs CREATE function, when there is error, it sends to error ms, send to activity log

@app.route("/bouquet", methods=['POST'])
def backendInventoryManagementCreate():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            backendInfo = request.get_json()
            print("\nReceived an order in JSON:", backendInfo)

            # do the actual work
            # 1. Send order info {cart items}
            print(backendInfo)
            result = processBackendInventoryManagementCreate(backendInfo)
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



def processBackendInventoryManagementCreate(backendInfo):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
        # 4. Record new order
    # record the activity log anyway
    item_id = str(backendInfo['Item_Id'])
    print(item_id)
    print('2')
    flower_URL = bouquet_URL + '/' + item_id
    #flower_URL = bouquet_URL 
    backendInfo = {'Item_Name': backendInfo['Item_Name'],'Price': backendInfo['Price'], 'Details': backendInfo['Details'], 'Expiry_Date': backendInfo['Expiry_Date'], 'Quantity': backendInfo['Quantity'] }

    print('\n\n-----Invoking inventory_URL microservice-----')
    bouquet_update = invoke_http(flower_URL, method="POST", json=backendInfo)
    print("\nOrder sent to bouquet_URL log.\n")
    print('order_result:', bouquet_update)
    code = bouquet_update["code"]
    message = json.dumps(bouquet_update)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (backend update error) message with routing_key=backend.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="backend.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), bouquet_update)

        # 7. Return error
        return {
            "code": 500,
            "data": {"inventory_result": bouquet_update},
            "message": "inventory_result failure sent for error handling."
        }

    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="backend.update", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')               
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
        #     body=message)  
############################################################# No error Proceed to Inventory Check & send telegram if stock low ################################################

        return {
                "code": 201,
            "data": {
                "inventory_result": bouquet_update,
                # "shipping_result": shipping_result
            }

        }


## Check if any inventory is close to expiry date  ################################################
print('\n\n-----Invoking Expiry Date CHeck-----')
currentInventoryDetails = invoke_http(bouquet_URL, method="GET")
for x in currentInventoryDetails["data"]["inventory"]:
    seperatedDate= x["Expiry_Date"].split("-")
    seperatedCurrentDate= (datetime.today().strftime('%Y-%m-%d')).split("-")
    f_date = date(int(seperatedDate[0]), int(seperatedDate[1]), int(seperatedDate[2]))
    l_date = date(int(seperatedCurrentDate[0]), int(seperatedCurrentDate[1]), int(seperatedCurrentDate[2]))
    remainingDays= f_date - l_date
    if(int(remainingDays.days)<=7):
            telegramDateNotification = invoke_http(telegram_URL, method="POST",json=x)
            code = telegramDateNotification["code"]
            if code not in range(200,300):
                print('\n\n-----Publishing the (Telegram error) message with routing_key=telegram.error-----')
                message = json.dumps(telegramDateNotification)

                # invoke_http(error_URL, method="POST", json=order_result)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="telegram.error", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))         
            else:
                print('\n\n-----Publishing the (Telegram success) message with routing_key=update.telegram-----')
                message = json.dumps(telegramDateNotification)

                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="update.telegram", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))


# if __name__ == '__main__':

#     app.run(port=5100, debug=True)
if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) +
        " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
