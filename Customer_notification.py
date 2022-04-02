#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os


import amqp_setup
import requests

from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
sender_address = 'eykf123@gmail.com'
sender_pass = 'ESDGROUP5!'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)






monitorBindingKey='*.customer'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Customer_Notification'
    
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
    process_email_step(order)
    print(order)
    

#{'order_result': 
# {'code': 201, 'data': 
# {'created': 'Sun, 03 Apr 2022 00:28:16 GMT', 'customer_id': 'gleena', 'modified': 'Sun, 03 Apr 2022 00:28:16 GMT', 'order_id': 312, 'order_item': 
# [{'Item_Id': '1', 'order_id': 312, 'order_item_id': 621, 'quantity': 1}, {'Item_Id': '2', 'order_id': 312, 'order_item_id': 622, 'quantity': 1}], 'status': 'NEW'}},
#  'inventory_result': 
# {'code': 201, 'data': 
# {'inventory_result': {'code': 201, 'data': 
# [{'Details': '99 rose bouquet', 'Expiry_date': '2022-03-20', 'Item_Id': 1, 'Item_Name': 'Willow Series ', 'Price': '500.00', 'Quantity': 49}, {'Details': 'Blue Baby Breath', 'Expiry_date': '2022-03-26', 'Item_Id': 2, 'Item_Name': 'Blue Baby Breath Bouquet', 'Price': '80.00', 'Quantity': 49}]},
#  'telegram_result': {'code': 201, 'message': 'Telegram message sent to admin'}}}, '
# schedule_result': {'code': 201, 'data': {'Customer_ID': '02', 'Email': 'iamyikiat@gmail', 'Schedule_ID': 178, 'order_id': 1, 'timeslot': 'Sun, 10 Apr 2022 09:30:00 GMT'}}}

def process_email_step(order):
        print('email process start')
       # order_cart = request.json.get('cart_item')str(order_cart["quantity"]) 
        print(order)
        email = order["schedule_result"]["data"]["Email"]
        flower = " "
        allflower = order["inventory_result"]["data"]["inventory_result"]["data"]
        for i in allflower: 
            flower = flower + str(i["Item_Name"]) + "   "
        print(flower)
        print(email)
        receiver_address = email
        # item = order["data"]["order_result"]["data"]["item_id"]
        # quantity = order["data"]["order_result"]["data"]["order_item"].length
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Lilas Blooms order request'   #The subject line
        mail_content='Hello Customer, You have ordered' + flower 
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')



if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
