from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/adminDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Admin(db.Model):
    __tablename__ = 'admin'
# change primary key to email
# set admin_id to auto_increment
    admin_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self, email, name, admin_id=None):
        self.admin_id = admin_id
        self.name = name
        self.email = email

    def json(self):
        return {"admin_id": self.admin_id, "name": self.name, "email": self.email}
    

 
@app.route("/admin")
def get_all():
# copy the code to get all admin from book.py 
    admin_list = Admin.query.all()
    print(admin_list)
    if len(admin_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "admins": [admin.json() for admin in admin_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no admins."
        }
    ), 404

 
@app.route("/admin/<string:email>")
def find_by_email(email):
# copy the code to get admin by id from book.py  
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        return jsonify(
            {
                "code": 200,
                "data": admin.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Admin not found."
        }
    ), 404   

 
@app.route("/admin/<string:email>", methods=['POST'])
def create_admin(email):
# copy the code to create admin from book.py 
    if (Admin.query.filter_by(email=email).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "email": email
                },
                "message": "Admin already exists."
            }
        ), 400

    data = request.get_json()
    admin = Admin(email, **data)
    print(admin)
    try:
        db.session.add(admin)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": email
                },
                "message": "An error occurred creating the admin."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": admin.json()
        }
    ), 201

@app.route("/admin/<string:email>", methods=['PUT'])
def update_admin(email):
    admin = Admin.query.filter_by(email=email).first()
    print(admin)
    if admin:
        data = request.get_json()
        print(data)
        if "name" in data:
            admin.name = data['name']
        if "admin_id" in data:
            admin.admin_id = data['admin_id']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": admin.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "email": email
            },
            "message": "Admin not found."
        }
    ), 404

@app.route("/admin/<string:email>", methods=['DELETE'])
def delete_admin(email):
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        db.session.delete(admin)
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
            "message": "Admin not found."
        }
    ), 404
 
if __name__ == '__main__':
    app.run(port=5002, debug=True)