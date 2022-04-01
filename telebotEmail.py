import requests
import telebot


def telegram_bot_sendtext(bouquetDetail,bouquetQuantity):
    bot_token='5148498973:AAGd2BFVjJEH3dc4WJmtFyOCWfX3MxRPhEk'
    bot_chatID = '179825290'
    send_text= 'https://api.telegram.org/bot' + bot_token +'/sendMessage?chat_id=' +bot_chatID +\
                '&parse_mode=MarkdownV2&text=' + bouquetDetail + " has a quantity of " + str(bouquetQuantity) +  " which is the minimum threshold of 50, enter /order to initiate order process"

    global bouquetDetailGlobal
    global bouquetQuantityGlobal

    bouquetDetailGlobal = bouquetDetail
    bouquetQuantityGlobal = bouquetQuantity

    response=requests.get(send_text)
    return response.json()
    




