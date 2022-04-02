#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

from cgitb import text
import json
import os


import requests
import amqp_setup

monitorBindingKey='*.admin'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Admin_Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    Admin_Notification(json.loads(body))
    print() # print a new line feed

def Admin_Notification(order):
    print("Show customer order:")
    telegram_bot_sendtext(order)
    

   # print("Name:" + order["data"]["customer_id"] + "order:" + order["data"]["customer_id"])

#{'order_result': 
# {'code': 201, 'data': 
# {'created': 'Sun, 03 Apr 2022 00:28:16 GMT', 'customer_id': 'gleena', 'modified': 'Sun, 03 Apr 2022 00:28:16 GMT', 'order_id': 312, 'order_item': 
# [{'Item_Id': '1', 'order_id': 312, 'order_item_id': 621, 'quantity': 1}, {'Item_Id': '2', 'order_id': 312, 'order_item_id': 622, 'quantity': 1}], 'status': 'NEW'}},
#  'inventory_result': 
# {'code': 201, 'data': 
# {'inventory_result': {'code': 201, 'data': 
# [{'Details': '99 rose bouquet', 'Expiry_date': '2022-03-20', 'Item_Id': 1, 'Item_Name': 'Willow Series ', 'Price': '500.00', 'Quantity': 49}, {'Details': 'Blue Baby Breath', 'Expiry_date': '2022-03-26', 'Item_Id': 2, 'Item_Name': 'Blue Baby Breath Bouquet', 'Price': '80.00', 'Quantity': 49}]},
#  'telegram_result': {'code': 201, 'message': 'Telegram message sent to admin'}}}, '
# schedule_result': {'code': 201, 'chedule_result': {'code': 201, 'data': {'Customer_ID': '02', 'Email': 'iamyikiat@gmail', 'Schedule_ID': 141, order_id': 1, 'timeslot': 'Sun, 10 Apr 2022 09:30:00 GMT'}}}


def telegram_bot_sendtext(textMessage):
    
    print(textMessage)
    bot_token='5148498973:AAGd2BFVjJEH3dc4WJmtFyOCWfX3MxRPhEk'
    bot_chatID = '179825290'
    text = " "
    #quantity = textMessage["data"]["order_id"]["order_item"].length
    order_id = textMessage["data"]["order_id"]
    cusomter = textMessage["data"]["customer_id"]
    text = 'Order: ID' + str(order_id) + 'created for ' + cusomter
    print(cusomter)


    send_text= 'https://api.telegram.org/bot' + bot_token +'/sendMessage?chat_id=' +bot_chatID +\
                '&parse_mode=MarkdownV2&text=' + text

    print(send_text)
    response=requests.get(send_text)
    return response.json()

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
