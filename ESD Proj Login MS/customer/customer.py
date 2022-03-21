from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/customerDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def json(self):
        return {"customer_id": self.customer_id, "name": self.name, "email": self.email}    

 
    
#according to customerDB.sql information 
#create table customer(
#customer_id int auto_increment,
#name varchar(40),
#email varchar(40),
#constraint customer_pk primary key (customer_id));
#insert into customer(name, email) values('may', 'may@gmail.com');
#GRANT REFERENCES ON customerDB.customer TO loginDB;
 
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

 
@app.route("/customer/<int:customer_id>")
def find_by_customer_id(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
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
 
@app.route("/customer/<int:customer_id>", methods=['POST'])
def create_customer_id(customer_id):
    if (Customer.query.filter_by(customer_id=customer_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "customer_id": customer_id
                },
                "message": "Customer already exists."
            }
        ), 400

    data = request.get_json()
    customer = Customer(customer_id, **data)

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "customer_id": customer_id
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

@app.route("/customer/<int:customer_id>", methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        data = request.get_json()
        if data['name']:
            customer.name = data['name']
        if data['email']:
            customer.email = data['email'] 
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
                "customer_id": customer_id
            },
            "message": "Customer not found."
        }
    ), 404

@app.route("/customer/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "customer_id": customer_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "customer_id": customer_id
            },
            "message": "Customer not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)