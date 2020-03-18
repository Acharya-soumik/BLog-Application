from flask import Flask
from flask_cors import CORS
import hashlib
import os
import base64
from flask import request
import json
from flask_mysqldb import MySQL
import jwt
import os

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
    res = cursor.fetchall()
    cursor.close()
    item = []
    for i in res:
        item.append(i)
    return item


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
    cursor = mysql.connection.cursor()
    cursor.execute("""select * from user where email=%s""", (email,))
    res = cursor.fetchall()
    cursor.close()
    if len(res) == 0:
        return {"status": "Incorrect Email Address"}
    else:
        user_salt = res[0]["salt"]
        user_pass = res[0]["password"]
    hex_pass = md5_hash(password, user_salt)
    if hex_pass == user_pass:
        token = jwt.encode(
            {"id": res[0]["id"], "email": res[0]["email"]}, "secret", algorithm="HS256")
        return {"status": "login succesfull", "token": str(token), "u_id": res[0]["id"]}
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
    user_id = request.json["user_id"]
    catagory_id = request.json["catagory_id"]
    CreateBlog(title, content, user_id, catagory_id)
    return "New Post Added"


@app.route("/catagories")
def catagories():
    list_catagory = getCatagory()
    return json.dumps(list_catagory)


@app.route("/new_category", methods=["POST"])
def newCategory():
    category = request.json["category"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """insert into catagory (catagories) values (%s) """, (category,))
    mysql.connection.commit()
    cursor.close()
    return "category added"


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
        """select blog.id as blog_id ,user.id as id,catagory_id,title,content ,blog.created_at,name,email from blog join user on blog.user_id = user.id
"""
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


@app.route("/delete_blogs", methods=["POST"])
def delete_post():
    user_id = request.json["user_id"]
    u_id = request.json["id"]
    c_id = request.json["catagory_id"]
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return "Cannot Delete"
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """delete from  comments  where user_id = %s and blog_id=%s and catagory_id=%s """, (
                user_id, u_id, c_id)
        )

        cursor.execute(
            """delete from  blog  where user_id = %s and id=%s and catagory_id=%s """, (
                user_id, u_id, c_id)
        )
        mysql.connection.commit()
        cursor.close()
        return "user deleted"


@app.route('/uploader/<user_id>', methods=["POST"])
def upload_file(user_id):
    f = request.files['picture']
    cursor = mysql.connection.cursor()
    try:
        locationfolder = "../Client/public/image/" + str(user_id)
        os.mkdir(locationfolder)
        locationimage = "../Client/public/image/" + \
            str(user_id) + "/" + f.filename
        f.save(locationimage)
        img_path = "./image/"+str(user_id)+"/"+f.filename
        cursor.execute(
            """update user set image = %s where id = %s""", (img_path, int(user_id)))
        mysql.connection.commit()
        cursor.close()
        return {"path": img_path}
    except OSError:
        locationimage = "../Client/public/image/" + \
            str(user_id) + "/" + f.filename
        img_path = "./image/"+str(user_id)+"/"+f.filename
        f.save(locationimage)
        cursor.execute(
            """update user set image = %s where id = %s""", (img_path, int(user_id)))
        mysql.connection.commit()
        cursor.close()
        return {"path": img_path}


if __name__ == "__main__":
    app.run(debug=True)
