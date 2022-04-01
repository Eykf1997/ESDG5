import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Schedule(db.Model):
    __tablename__ = 'schedule'

    Schedule_ID = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    timeslot = db.Column(db.DateTime, nullable=False)
    Customer_ID = db.Column(db.String)
    Email = db.Column(db.String)

    # def __init__(self, Schedule_ID, order_id, timeslot, Customer_ID, Email):
    #     self.Schedule_ID = Schedule_ID
    #     self.order_id = order_id
    #     self.timeslot = timeslot
    #     self.Customer_ID = Customer_ID
    #     self.Email = Email

    def json(self):
         return {"Schedule_ID": self.Schedule_ID, "order_id": self.order_id, "timeslot": self.timeslot, "Customer_ID": self.Customer_ID, "Email": self.Email}



@app.route("/schedule")
def get_all():
    Schedulelist = Schedule.query.all()
    if len(Schedulelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "schedule": [schedule.json() for schedule in Schedulelist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no schedule."
        }
    ), 404



@app.route("/schedule", methods=['POST'])
def create_schedule():
    schedule_cart = request.json.get('schedule')
    #print(schedule_cart[0]["Schedule_ID"])
    # Schedule_ID = request.json.get('Schedule_ID')
    # collection_date = request.json.get('collection_date')
    # timeslot = request.json.get('timeslot')
    # Customer_ID = request.json.get('Customer_ID')
    # Phone = request.json.get('Phone')
    schedule = Schedule( order_id=schedule_cart[0]["order_id"], timeslot=schedule_cart[0]["timeslot"], Customer_ID=schedule_cart[0]["Customer_ID"], Email=schedule_cart[0]["Email"])

    # cart_item = request.json.get('cart_item')
    # for item in cart_item:
    #     order.order_item.append(Order_Item(
    #         Items_ID=item['Items_ID'], quantity=item['quantity']))

    try:
        db.session.add(schedule)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": schedule.json()
        }
    ), 201




if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5003, debug=True)