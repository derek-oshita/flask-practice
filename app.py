import os 

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# SET BASE DIRECTORY 
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLITE DATABASE
DATABASE = 'sqlite:///' + os.path.join(basedir, 'db.reddit')

# SETUP DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT DATABASE
db = SQLAlchemy(app)

# INIT MARSHMALLOW
marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000

# ROUTES GO HERE

# HOME
@app.route('/')
def hello_world(): 
    return 'Hello world...'

# CREATE SUB
@app.route('/sub', methods=['POST', 'GET'])
# GET SUB W/ ID
@app.route('/sub/<subid>', methods=['GET'])
def create_sub(subid = None): 
    from models import Sub
    if subid== None and request.method == 'GET': 
        return Sub.get_subs()
    elif subid == None: 
        name = request.json['name']
        description = request.json['description']
        return Sub.create_sub(name, description)
    else: 
        return Sub.get_sub(subid)

# GET POSTS
@app.route('/post', methods=['POST', 'GET'])
@app.route('/post/<postid>', methods=['GET'])
def create_post(postid = None): 
    from models import Post
    if postid == None and request.method == 'GET': 
        return Post.get_posts()
    elif postid == None: 
        title = request.json['title']
        body = request.json['body']
        user = request.json['user']
        sub = request.json['sub']
        return Post.create_post(title, body, user, sub)
    else: 
        return Post.get_post(postid)

# UPDATE / DELETE POST
@app.route('/post/<postid>', methods=['PUT', 'DELETE'])
def update_or_delete_post(postid=None): 
    from models import Post
    if request.method == 'PUT': 
        req = request.get_json()
        return Post.update_post(postid, **req)
    else: 
        return Post.delete_post(postid)

# COMMENT
@app.route('/comment', methods=['POST', 'GET'])
@app.route('/comment/<commentid>', methods=['GET'])
def create_comment(commentid=None): 
    from models import Comment
    if commentid == None and request.method == "POST":
        title = request.json["title"]
        text = request.json["text"]
        post = request.json["post"]
        return Comment.create_comment(title, text, post)
    elif commentid != None and request.method == "GET":
        return Comment.get_comment(commentid)
    else: 
        return Comment.get_comments()

@app.route('/comment/<commentid>', methods=["PUT", "DELETE"])
def update_or_delete_comment(commentid): 
    from models import Comment
    if request.method == "PUT": 
        req = request.get_json()
        return Comment.update_comment(commentid, **req)



    



if __name__ == '__main__': 
    app.run(debug=DEBUG, port=PORT)