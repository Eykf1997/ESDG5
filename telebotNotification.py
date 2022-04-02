import requests


import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
@app.route("/telegramNotification", methods=['POST'])
def telegram_bot_sendtext():
    bot_token='5148498973:AAGd2BFVjJEH3dc4WJmtFyOCWfX3MxRPhEk'
    bot_chatID = '179825290'
    telegramDetails = request.json.get("data")
    print(telegramDetails)
    send_text= 'https://api.telegram.org/bot' + bot_token +'/sendMessage?chat_id=' +bot_chatID +\
                '&parse_mode=MarkdownV2&text='+ telegramDetails['Details'] + ' has a quantity of'+ str(telegramDetails['Quantity']) +'which is the minimum threshold of 50, enter /order to initiate order process' 


    response=requests.get(send_text)
    if response:
        return {
                "code": 201,
                "message":"Telegram message sent to admin"

        }
    return jsonify(
        {
            "code": 404,
            "message": "Telegram message failed to send"
        }
    ), 404    


if __name__ == '__main__':

    app.run(port=5101, debug=True)
