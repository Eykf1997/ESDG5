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
receiver_address = 'elmer.yeo.2020@smu.edu.sg'
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)






monitorBindingKey='*.info'

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
    process_email_step(message,order)
    print(order)
    




def process_email_step(message,quantity):
        print('email process start')
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Lilas Blooms order request'   #The subject line
        mail_content='Hello Customer, You have ordered' +" "+ quantity + " of "
        #The body and the attachments for the mail
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
