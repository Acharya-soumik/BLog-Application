from flask import Flask
from flask_cors import CORS
import hashlib
import os
import base64
from flask import request
import json
from flask_mysqldb import MySQL
import jwt

app = Flask(__name__)
CORS(app)


app.config["MYSQL_HOST"] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '999Plus1@'
app.config['MYSQL_DB'] = 'blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


def read_data():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * FROM user """
    )
    result = cursor.fetchall()
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return items


def CreateUser(name, email, salt, hashed_pass):
    print(name, email, salt, hashed_pass)
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO user (name,email,salt,password,created_at) values (%s,%s,%s,%s,now()) """, (
            name, email, salt, hashed_pass)
    )
    mysql.connection.commit()
    cursor.close()
    return {"message": "User added"}


def CreateBlog(title, content, user_id, catagory_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO blog (title,content,created_at,user_id,catagory_id) values (%s,%s,now(),%s,%s)""",
        (title, content, user_id, catagory_id))
    mysql.connection.commit()
    cursor.close()
    return {"message": "New Post Added"}


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
            return {"status": "login succesfull", "token": str(token), "u_id": items["id"]}
        else:
            return {"status": "Incorrect Password"}


def find_user(u_id):
    print("u_id is ", u_id)
    all_users = read_data()
    for i in all_users:
        print("my i is ", i["id"])
        if u_id == str(i["id"]):
            print("data found ======================>")
            return i
        else:
            print("Not Found")


def AddComment(comment, user_id, catagory_id, blog_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO comments (comment,created_at,user_id,catagory_id,blog_id) values (%s,now(),%s,%s,%s)""",
        (comment, user_id, catagory_id, blog_id))
    mysql.connection.commit()
    cursor.close()
    return {"message": "New Post Added"}


def getCatagory():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * FROM catagory """
    )
    result = cursor.fetchall()
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return items


def get_user_comments(u_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * FROM comments WHERE blog_id = %s  """, (u_id,)
    )
    result = cursor.fetchall()
    print("result is ====...............", result)
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return items


@app.route("/")
def demo():
    data = read_data()
    temp_data = []
    for items in data:
        temp_data.append(str(items))
    return json.dumps(data, default=str)


@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    res = check_auth(email, password)
    return json.dumps(res)


@app.route("/signup", methods=["POST"])
def register():
    name = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    my_data = write_csv(name, email, password)
    return json.dumps(my_data)


@app.route("/details", methods=["POST"])
def showDetails():
    auth_header = request.headers.get('Authorization')
    print("token is", auth_header)
    token_encoded = auth_header.split(' ')[1]
    decode_data = dict(jwt.decode(
        token_encoded, 'secret', algorithms=['HS256']))
    user_id = decode_data["id"]
    user = find_user(str(user_id))
    return json.dumps(user, default=str)


@app.route("/new_post", methods=["POST"])
def new_blog():
    title = request.json["title"]
    content = request.json["content"]
    user_id = 1,
    catagory_id = 2
    CreateBlog(title, content, user_id, catagory_id)
    return "New Post Added"


@app.route("/catagories")
def catagories():
    list_catagory = getCatagory()
    return json.dumps(list_catagory)


@app.route("/new_comment", methods=["POST"])
def new_comment():
    comment = request.json["comment"]
    user_id = request.json["user_id"]
    catagory_id = request.json["catagory_id"]
    blog_id = request.json["blog_id"]
    b_id = request.json["blog_id"]
    AddComment(comment, user_id, catagory_id, blog_id)
    items = get_user_comments(b_id)
    return json.dumps(items, default=str)


@app.route("/blogs")
def all_blogs():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * FROM blog """
    )
    result = cursor.fetchall()
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return json.dumps(items, default=str)


@app.route("/comments", methods=["POST"])
def all_comments():
    b_id = int(request.json["b_id"])
    items = get_user_comments(b_id)
    return json.dumps(items, default=str)


@app.route("/user_blogs", methods=["POST"])
def user_blogs():
    u_id = request.json["user_id"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT * FROM blog where user_id = %s """, (u_id)
    )
    result = cursor.fetchall()
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return json.dumps(items, default=str)


@app.route("/edit_post", methods=["POST"])
def edit_blogs():
    user_id = request.json["user_id"]
    title = request.json["title"]
    content = request.json["content"]
    u_id = request.json["id"]
    c_id = request.json["catagory_id"]

    cursor = mysql.connection.cursor()
    cursor.execute(
        """UPDATE blog set title =%s , content =%s where user_id = %s and id=%s and catagory_id=%s """, (
            title, content, user_id, u_id, c_id)
    )
    mysql.connection.commit()
    result = cursor.fetchall()
    cursor.close()
    items = []
    for i in result:
        items.append(i)
    return json.dumps(items, default=str)


# @app.route('/uploader', methods=["POST"])
# def upload_file():
#     f = request.files['picture']
#     location = "static/img/" + f.filename
#     f.save(location)
#     return {"path": location}
if __name__ == "__main__":
    app.run(debug=True)
