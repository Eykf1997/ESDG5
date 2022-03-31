#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os


import requests
import amqp_setup

monitorBindingKey='*.Notification'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Order_Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    CustomerNotification(json.loads(body))
    print() # print a new line feed

def CustomerNotification(order):
    print("Show customer order:")
    telegram_bot_sendtext(order)
    print(order)

    print("Name:" + order["data"]["customer_id"] + "order:" + order["data"]["customer_id"])


def telegram_bot_sendtext(textMessage):
    print(textMessage)
    bot_token='5148498973:AAGd2BFVjJEH3dc4WJmtFyOCWfX3MxRPhEk'
    bot_chatID = '179825290'
    numberOfFlowers = ""
    for i in textMessage["data"]["order_item"]: 
        numberOfFlowers += str(i["quantity"]) 
        print(numberOfFlowers)
    

    send_text= 'https://api.telegram.org/bot' + bot_token +'/sendMessage?chat_id=' +bot_chatID +\
                '&parse_mode=MarkdownV2&text=' + "Name:" + textMessage["data"]["customer_id"] + "\n order:" + str(numberOfFlowers)

    response=requests.get(send_text)
    return response.json()

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
