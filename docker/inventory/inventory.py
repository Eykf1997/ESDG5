from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/inventory'
#app.config['SQLALCHEMY_DATABASE_URI']= environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    Item_Id = db.Column(db.Integer,primary_key=True)
    Quantity = db.Column(db.String(5), nullable=False)
    Details = db.Column(db.String(64), nullable=False)
    Expiry_Date = db.Column(db.String(10), nullable=False)
    Item_Name = db.Column(db.String(64), nullable=False)
    Price = db.Column(db.Float(precision=2), nullable=False)
    
    def __init__(self, Item_Id, Quantity, Details, Expiry_Date, Item_Name, Price):
        self.Item_Id = Item_Id
        self.Quantity = Quantity
        self.Details = Details
        self.Expiry_Date = Expiry_Date
        self.Item_Name = Item_Name
        self.Price = Price
        
    def json(self):
        return {'Item_Id': self.Item_Id, 'Quantity': self.Quantity, 'Details': self.Details, 'Expiry_Date': self.Expiry_Date, 'Item_Name': self.Item_Name, 'Price': self.Price}
    
@app.route("/inventory")
def get_all():
    inventorylist = Inventory.query.all()
    if len(inventorylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [bouquet.json() for bouquet in inventorylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bouquets."
        }
    ), 404

@app.route("/inventory/<string:Item_Id>")
def find_by_Item_Id(Item_Id):
    getItem = Inventory.query.filter_by(Item_Id=Item_Id).first()
    if getItem:
        return jsonify(
            {
                "code": 200,
                "data": getItem.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Bouquet not found."
        }
    ), 404

# app.route default uses GET method, so other method need to declare
@app.route("/inventory/<string:Item_Id>", methods=['POST'])
# Create bouquet
def create_bouquet(Item_Id):
    if (Inventory.query.filter_by(Item_Id=Item_Id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "Item_Id": Item_Id
                },
                "message": "Bouquet already exists."
            }
        ), 400
        
    data = request.get_json()
    newBouquet = Inventory(Item_Id, **data)
    
    try:
        db.session.add(newBouquet)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "Item_Id": Item_Id
                },
                "message": "An error occurred creating the bouquet."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": newBouquet.json()
        }
    ), 201
    
    
#havent test this function    
@app.route("/inventory/<string:Item_Id>", methods=['PUT'])
def update_bouquet(Item_Id):
    bouquet = Book.query.filter_by(Item_Id=Item_Id).first()
    if bouquet:
        data = request.get_json()
        if data['Item_Id']:
            bouquet.Item_Id = data['Item_Id']
        if data['Item_Name']:
            bouquet.Item_Name = data['Item_Name']
        if data['Quantity']:
            bouquet.Quantity = data['Quantity'] 
        if data['Price']:
            bouquet.Price = data['Price'] 
        if data['Details']:
            bouquet.Details = data['Details'] 
        if data['Expiry_Date']:
            bouquet.Expiry_Date = data['Expiry_Date'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": bouquet.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Item_Id": Item_Id
            },
            "message": "Bouquet not found."
        }
    ), 404

#havent test this function
@app.route("/inventory/<string:Item_Id>", methods=['DELETE'])
def delete_bouquet(Item_Id):
    bouquet = Inventory.query.filter_by(Item_Id=Item_Id).first()
    if bouquet:
        db.session.delete(bouquet)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Item_Id": Item_Id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Item_Id": Item_Id
            },
            "message": "Bouquet not found."
        }
    ), 404
    
    
# host 0.0.0.0 allows service to be accessible from other network not only my comp
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    
    # Challenge: shift in consumer preference - to free & easy tour
    # Strategy: Assetlight Model? Education - using virtual tour guide does not need to focus on tour trip but can be on education trip - booking of accomodation can be done through app
    # why people come to Singapore -> the tourism board data -> analytic -> propose recommendation on education because they come here for...
    
    #Plan itenary, app give recommendation, according to routing, recommend accommodation then enable user to book hotel, receive booking then confirmation, reach sg see monument wants to know what it is about, use app image recognition & details appear, AR enable interaction w user, got game for user, if user wants select dialect then it will 