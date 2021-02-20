from flask_practice_app import app
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_practice_app.models import Sub, Post, Comment

# HOME
@app.route('/')
def hello_world(): 
    return render_template('base.html')

##########################################################################################################################################
# SUB - GET / POST
@app.route('/sub', methods=['POST', 'GET'])
@app.route('/sub/<subid>', methods=['GET'])
def create_sub(subid = None): 
    if subid== None and request.method == 'GET': 
        return Sub.get_subs()
    elif subid == None: 
        name = request.json['name']
        description = request.json['description']
        return Sub.create_sub(name, description)
    else: 
        return Sub.get_sub(subid)

##########################################################################################################################################
# POST - GET / POST
@app.route('/post', methods=['POST', 'GET'])
@app.route('/post/<postid>', methods=['GET'])
def create_post(postid = None): 
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

# POST - UPDATE / DELETE
@app.route('/post/<postid>', methods=['PUT', 'DELETE'])
def update_or_delete_post(postid=None): 
    if request.method == 'PUT': 
        req = request.get_json()
        return Post.update_post(postid, **req)
    else: 
        return Post.delete_post(postid)

##########################################################################################################################################
# COMMENT - GET /POST
@app.route('/comment', methods=['POST', 'GET'])
@app.route('/comment/<commentid>', methods=['GET'])
def create_comment(commentid=None): 
    if commentid == None and request.method == "POST":
        title = request.json["title"]
        text = request.json["text"]
        post = request.json["post"]
        return Comment.create_comment(title, text, post)
    elif commentid != None and request.method == "GET":
        return Comment.get_comment(commentid)
    else: 
        return Comment.get_comments()

# COMMENT - UPDATE / DELETE 
@app.route('/comment/<commentid>', methods=["PUT", "DELETE"])
def update_or_delete_comment(commentid): 
    if request.method == "PUT": 
        req = request.get_json()
        return Comment.update_comment(commentid, **req)
    else: 
        return Comment.delete_comment(commentid)