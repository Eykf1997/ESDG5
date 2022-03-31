from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/customerDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

CORS(app) 
 
class Customer(db.Model):
    __tablename__ = 'customer'
# change primary key to email
# set customer_id to auto_increment
    customer_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self,email, name, customer_id = None):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def json(self):
        return {"customer_id": self.customer_id, "name": self.name, "email": self.email}    


 
@app.route("/customer")
def get_all():
    customer_list = Customer.query.all()
    if len(customer_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "customers": [customer.json() for customer in customer_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no customers."
        }
    ), 404

 
@app.route("/customer/<string:email>")
def find_by_email(email):
    customer = Customer.query.filter_by(email=email).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Customer not found."
        }
    ), 404      
 
@app.route("/customer/<string:email>", methods=['POST'])
def create_email(email):
    if (Customer.query.filter_by(email=email).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "email": email
                },
                "message": "Customer already exists."
            }
        ), 400

    data = request.get_json()
    customer = Customer(email, **data)

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": email
                },
                "message": "An error occurred creating the customer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": customer.json()
        }
    ), 201

@app.route("/customer/<string:email>", methods=['PUT'])
def update_customer(email):
    customer = Customer.query.filter_by(email=email).first()
    if customer:
        data = request.get_json()
        if "name" in data:
            customer.name = data['name']
        if "customer_id" in data:
            customer.customer_id = data['customer_id'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "email": email
            },
            "message": "Customer not found."
        }
    ), 404

@app.route("/customer/<string:email>", methods=['DELETE'])
def delete_customer(email):
    customer = Customer.query.filter_by(email=email).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "email": email
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "email": email
            },
            "message": "Customer not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)