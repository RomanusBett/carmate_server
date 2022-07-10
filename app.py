import redis
from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from uuid import uuid4
from flask_cors import CORS, cross_origin
from config import ApplicationConfig


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db = SQLAlchemy(app)
db.init_app(app)
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})




def get_uuid():
    return uuid4().hex

 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key = True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<user %r>" % self.email
    
@app.route("/register", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])

def register_user():
   email = request.json["email"]
   password  = request.json["password"]


   user_exists = User.query.filter_by(email=email).first() is not None

   if user_exists:
        return jsonify({"error": "user already exists"}),409

   hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
   new_user = User(email=email, password=hashed_password)
   db.session.add(new_user)
   db.session.commit()

   session["user_id"]=new_user.id

   return jsonify({
       "id":new_user.id,
       "email":new_user.email
       })

@app.route("/about")
def get_user():
    user_id=session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorised"}),401
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id":user.id,
        "email":user.email
    })

@app.route("/login", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def login_user():
    email = request.json["email"]
    password  = request.json["password"]


    this_user = User.query.filter_by(email=email).first() 

    if this_user is None:
        return jsonify({"error": "Unauthorised"}), 401

    if not bcrypt.check_password_hash(this_user.password, password):
        return jsonify({"error": "Unauthorised"}), 401

    session["user_id"]=this_user.id

    return jsonify({
        "id":this_user.id,
        "email":this_user.email
    })

@app.route("/@me")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_current_user(): 
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 


@app.route('/logout', methods=['POST'])
def logout_user():
    session.pop("user_id")
    return "200"


if __name__ == "__main__":

    app.run(debug=True)
