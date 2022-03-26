from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/loginDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Login(db.Model):
    __tablename__ = 'login'
    
    username = db.Column(db.String(20), primary_key=True)
    password= db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)

    def __init__(self, username, password, customer_id = None, admin_id = None):
        self.admin_id = admin_id
        self.username = username
        self.password = password
        self.customer_id = customer_id

    def json(self):
        return {"admin_id": self.admin_id, "username": self.username, "password": self.password, "customer_id": self.customer_id}
 

 
@app.route("/login")
def get_all():
    login_list = Login.query.all()
    if len(login_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "logins": [login.json() for login in login_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no login info."
        }
    ), 404

 
@app.route("/login/<string:username>")
def find_by_username(username):
    login = Login.query.filter_by(username=username).first()
    if login:
        print(login.admin_id, login.customer_id)
        return jsonify(
            {
                "code": 200,
                "data": login.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Username not found."
        }
    ), 404   

 
@app.route("/login/<string:username>", methods=['POST'])
def create_username(username):
    if (Login.query.filter_by(username=username).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "username": username
                },
                "message": "Username already exists."
            }
        ), 400

    data = request.get_json()
    login = Login(username, **data)

    try:
        db.session.add(login)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "username": username
                },
                "message": "An error occurred creating the account."
            }
        ), 500

    return jsonify(
        {   
            "code": 201,
            "data": username
        }
    ), 201

@app.route("/login/<string:username>", methods=['PUT'])
def update_login(username):
    login = Login.query.filter_by(username=username).first()
    if login:
        data = request.get_json()
        if "password" in data:
            login.password = data['password']
        if "customer_id" in data:
            login.customer_id = data['customer_id'] 
        if "admin_id" in data:
            login.admin_id = data['admin_id'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": login.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "Login not found."
        }
    ), 404

@app.route("/login/<string:username>", methods=['DELETE'])
def delete_login(username):
    login = Login.query.filter_by(username=username).first()
    if login:
        db.session.delete(login)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "username": username
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "username": username
            },
            "message": "Login not found."
        }
    ), 404

 
if __name__ == '__main__':
    app.run(port=5000, debug=True)