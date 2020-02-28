from flask import Flask
from flask import Blueprint
from flask import request
from flask_cors import CORS
import hashlib
import os
import base64
import json
from flask_mysqldb import MySQL
import jwt

auth = Blueprint("auth", __name__)
CORS(auth)

auth_config = Flask(__name__)


auth_config.config["MYSQL_HOST"] = "localhost"
auth_config.config['MYSQL_USER'] = 'root'
auth_config.config['MYSQL_PASSWORD'] = '999Plus1@'
auth_config.config['MYSQL_DB'] = 'blog'
auth_config.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(auth_config)


def read_data():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * FROM catagories """
    )
    result = cursor.fetchall()
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return items


def CreateUser(name, email, salt, hashed_pass):
    print(name, email, salt, hashed_pass)
    catagory = "sleep"
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO user (name,email,salt,password,created_at) values (%s,%s,%s,%s,now()) """, (
            name, email, salt, hashed_pass)
    )
    mysql.connection.commit()
    cursor.close()
    return {"message": "User added"}


def generate_salt():
    salt = os.urandom(16)
    return base64.b64encode(salt)


def md5_hash(string, salt):
    hash = hashlib.md5()
    new_str = salt+string
    hash.update(new_str.encode('utf-8'))
    return hash.hexdigest()


def write_csv(name, email, password):
    if len(email) < 5 or len(name) < 2:
        return "Invalid Credentials"
    salt = generate_salt()
    cur_data = read_data()
    for items in cur_data:
        if items["email"] == email:
            return "Email Already Exists"

    hashed_pass = md5_hash(password, salt)
    CreateUser(name, email, salt, hashed_pass)

    return "Registration Succesfull"


def check_auth(email, password):
    data = read_data()
    for items in data:
        print(items)
        if items["email"] != email:
            return {"status": "Incorrect Email address"}
        elif items["email"] == email:
            user_salt = items["salt"]
            user_pass = items["password"]
        hex_pass = md5_hash(password, user_salt)
        if hex_pass == user_pass:
            token = jwt.encode(
                {"id": items["id"], "email": items["email"]}, 'secret', algorithm="HS256")
            return {"status": "login succesfull", "token": str(token)}
        else:
            return {"status": "Incorrect Password"}


@auth.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    res = check_auth(email, password)
    return json.dumps(res)


@auth.route("/signup", methods=["POST"])
def register():
    name = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    my_data = write_csv(name, email, password)
    return json.dumps(my_data)


def find_user(u_id):
    all_users = read_data()
    for i in all_users:
        if u_id == i["id"]:
            return i


@auth.route("/details", methods=["POST"])
def showDetails():
    auth_header = request.headers.get('Authorization')
    print("token is", auth_header)
    token_encoded = auth_header.split(' ')[1]
    decode_data = dict(jwt.decode(
        token_encoded, 'secret', algorithms=['HS256']))
    user_id = decode_data["id"]
    user = find_user(str(user_id))
    return json.dumps(user)
