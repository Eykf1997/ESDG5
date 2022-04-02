import requests
import telebot
from telebot import types
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


API_TOKEN = '5148498973:AAGd2BFVjJEH3dc4WJmtFyOCWfX3MxRPhEk'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.itemName = None
        self.itemQuantity = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['order'])
def send_welcome(message):
    msg = bot.reply_to(message, """This is the vendor ordering system. What's your name?""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Willow Series', 'Blue Baby Breath Bouquet','Pastel Bouquet','Cotton Dreams','Emcantador Bouquet','Hydrangeas & Baby Breath Bouquet','Jasper Bouquet','Condolence Stands')
        msg = bot.reply_to(message, 'What would you like to order?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_flower_step)
    except Exception as e:
        bot.reply_to(message, 'fail at name step')


def process_flower_step(message):
    try:
        chat_id = message.chat.id
        flower = message.text
        user = user_dict[chat_id]
        user.flower = flower
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        msg = bot.reply_to(message, 'How many would you like to order', reply_markup=markup)
        bot.register_next_step_handler(msg, process_quantity_step)
    except Exception as e:
        bot.reply_to(message, 'fail at flower step')


def process_quantity_step(message):
    try:
        chat_id = message.chat.id
        quantity = message.text
        if not quantity.isdigit():
            msg = bot.reply_to(message, 'Quantity should be a number. How many would you like?')
            bot.register_next_step_handler(msg, process_quantity_step)
            return
        user = user_dict[chat_id]
        user.quantity = quantity
        chat_id = message.chat.id
        user = user_dict[chat_id]
        emailMessage = MIMEMultipart()
        emailMessage['From'] = sender_address
        emailMessage['To'] = receiver_address
        emailMessage['Subject'] = 'Lilas Blooms order request'   #The subject line
        mail_content='Hello Vendor, I ('+user.name+ ') would like to order' +" "+ user.quantity + " of " + user.flower
        #The body and the attachments for the mail
        emailMessage.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = emailMessage.as_string()
        session.sendmail(sender_address, receiver_address, text)
        bot.send_message(message.chat.id, 'Email Sent!')
        session.quit()
        print('Mail Sent')
    except Exception as e:
        print(e)
        bot.reply_to(message, 'fail to send email')




# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()