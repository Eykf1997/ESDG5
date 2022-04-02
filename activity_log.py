#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
import amqp_setup

monitorBindingKey='#'

@app.route("/activity_log", methods=['POST'])
def receiveLog():
    # Check if the request contains valid JSON
    log = None
    if request.is_json:
        log = request.get_json()
        processLog(log)
        # reply to the HTTP request
        return jsonify({"code": 200, "data": 'OK. Activity log printed.'}), 200 # return message; can be customized
    else:
        log = request.get_data()
        print("Received an invalid log:")
        print(log)
        print()
        return jsonify({"code": 400, "message": "Activity log input should be in JSON."}), 400 # Bad Request



def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Inventory_Log'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an order log:")
    print(order)


def processLog(order):
    print("Recording a log:")
    print(order)
    print() # print a new line feed as a separator

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
