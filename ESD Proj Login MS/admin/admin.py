from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/adminDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self, admin_id, name, email):
        self.admin_id = admin_id
        self.name = name
        self.email = email

    def json(self):
        return {"admin_id": self.admin_id, "name": self.name, "email": self.email}
    

 
    
# according to adminDB.sql information 
#admin_id int auto_increment,
#name varchar(40),
#email varchar(40),
#constraint admin_pk primary key(admin_id));
#insert into admin(name, email) values('jun', 'jun@gmail.com');
#GRANT REFERENCES ON adminDB.admin TO loginDB;-- 
 
@app.route("/admin")
def get_all():
# copy the code to get all admin from book.py 
    admin_list = Admin.query.all()
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

 
@app.route("/admin/<int:admin_id>")
def find_by_admin_id(admin_id):
# copy the code to get admin by id from book.py  
    admin = Admin.query.filter_by(admin_id=admin_id).first()
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

 
@app.route("/admin/<int:admin_id>", methods=['POST'])
def create_admin_id(admin_id):
# copy the code to create admin from book.py 
    if (Admin.query.filter_by(admin_id=admin_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "admin_id": admin_id
                },
                "message": "Admin already exists."
            }
        ), 400

    data = request.get_json()
    admin = Admin(admin_id, **data)

    try:
        db.session.add(admin)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "admin_id": admin_id
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

@app.route("/admin/<int:admin_id>", methods=['PUT'])
def update_admin(admin_id):
    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if admin:
        data = request.get_json()
        if data['name']:
            admin.name = data['name']
        if data['email']:
            admin.email = data['email'] 
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
                "admin_id": admin_id
            },
            "message": "Admin not found."
        }
    ), 404

@app.route("/admin/<int:admin_id>", methods=['DELETE'])
def delete_admin(admin_id):
    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "admin_id": admin_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "admin_id": admin_id
            },
            "message": "Admin not found."
        }
    ), 404
 
if __name__ == '__main__':
    app.run(port=5002, debug=True)