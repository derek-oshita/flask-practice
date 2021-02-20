from flask_practice_app import db, marshmallow
from flask import jsonify
from marshmallow import fields

# import datetime as dt

# THE BASE CLASS FOR ALL OF YOUR MODELS ARE CALLED db.Model- ITS STORED ON THE SQLALCHEMY INSTANCE YOU HAVE TO CREATE
class Sub(db.Model): 
    # TABLE CONFIG: THIS ATTRIBUTE ACCOMMODATES EXISTING TABLES AND APPLIES FUTHER ARGUMENTS WITHIN THE CONSTRUCTOR TO EXISTING TABLE
    __table_args__ = {'extend_existing': True}

    # WHEN INSTANTIATING A SUB, WE CALL ON THE DB CONSTRUCTOR TO DEFINE THE COLUMNS, ITS NAME, AND WHAT INFORMATION SHOULD BE INSERTED
    # ONE COLUMN MUST BE DENOTED AS THE PRIMARY-KEY TO CREATE RELATIONSHIPS (unique)
    id = db.Column(db.Integer, primary_key=True)
    # 100 REPRESENTS THE MAX LENGTH OF THE STRING 
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))

    def __init__(self, name, description): 
        self.name = name
        self.description = description 

    # THIS DECORATOR EXISTS SO YOU CAN CREATE CLASS METHODS THAT ARE PASSED THE ACTUAL CLASS OBJ WITHIN THE FUNCTION CALL 
    @classmethod
    # SETTER METHOD FOR VALIDATION AND ABSTRACTION (AVOID DIRECT ACCESS OF A CLASS FIELD/PRIVATE FIELDS)
    def create_sub(cls, name, description): 
        new_sub = Sub(name, description)
        try: 
            db.session.add(new_sub)
            db.session.commit()
        except: 
            db.session.rollback()
            raise Exception('Session rollback')
        return sub_schema.jsonify(new_sub)

    # GETTER METHOD FOR VALIDATION
    @classmethod 
    def get_sub(cls, subid): 
        sub = Sub.query.get(subid)
        return sub_schema.jsonify(sub)

    @classmethod 
    def get_subs(cls): 
        subs = Sub.query.all()
        return subs_schema.jsonify(subs)


# SCHEMA SET UP USING MARSHMALLOW BECAUSE IT USES CLASSES RATHER THAN DICTIONARIES (EASY CODE REUSE AND CONFIGURATION)
# YOU CAN USE THIS LIBRARY TO DICTATE WHAT FIELDS WILL BE SENT BACK TO THE USER IN RESPONSE
class SubSchema(marshmallow.Schema): 
    class Meta: 
        fields = ('id', 'name', 'description')

sub_schema = SubSchema()
subs_schema = SubSchema(many=True)

# POST MODEL GOES HERE
class Post(db.Model): 
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(500))
    # created_at = db.Column(db.DateTime())
    user = db.Column(db.String(100))
    sub = db.Column(db.Integer, db.ForeignKey("sub.id"))

    def __init__(self, title, body, user, sub): 
        self.title = title
        self.body = body 
        self.user = user 
        self.sub = sub

    # GETTER (SINGLE POST)
    @classmethod
    def get_post(cls, postid): 
        post = Post.query.get(postid)
        return post_schema.jsonify(post)

    # GETTER (ALL POSTS)
    @classmethod
    def get_posts(cls): 
        posts = Post.query.all()
        return posts_schema.jsonify(posts)

    # SETTER
    @classmethod
    def create_post(cls, title, body, user, sub): 
        new_post = Post(title, body, user, sub)
        try: 
            db.session.add(new_post)
            db.session.commit()
        except: 
            db.session.rollback()
            raise Exception('Session rollback')
        return post_schema.jsonify(new_post)

    # DELETE
    @classmethod 
    def delete_post(cls, postid): 
        post = Post.query.get(postid)
        db.session.delete(post)
        db.session.commit()
        return post_schema.jsonify(post)


    # UPDATE
    @classmethod
    def update_post(cls, postid, title=None, body=None, user=None, sub=None):
        post = Post.query.get(postid)
        if title != None: 
            post.title = title
        if body != None: 
            post.body = body 
        if user != None: 
            post.user = user
        if sub != None:
            post.sub = sub
        db.session.commit()
        return post_schema.jsonify(post)
    
# POST SCHEMA
class PostSchema(marshmallow.Schema): 
    class Meta: 
        fields = ('id', 'title', 'body', 'user', 'sub')

post_schema = PostSchema()
posts_schema = PostSchema(many =  True)

# COMMENT MODEL
class Comment(db.Model): 
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(300))
    post = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __init__(self, title, text, post): 
        self.title = title
        self.text = text
        self.post = post

    # CREATE COMMENT 
    @classmethod
    def create_comment(cls, title, text, post): 
        new_comment = Comment(title, text, post)
        try: 
            db.session.add(new_comment)
            db.session.commit()
        except: 
            db.session.rollback()
            raise Exception("Session rollback...")
        return comment_schema.jsonify(new_comment)

    # GET COMMENT 
    @classmethod 
    def get_comment(cls, commentid): 
        comment = Comment.query.get(commentid)
        return comment_schema.jsonify(comment)

    # GET COMMENTS 
    @classmethod 
    def get_comments(cls): 
        comments = Comment.query.all()
        return comments_schema.jsonify(comments)

    # UPDATE COMMENTS (see what happens when we don't set to NONE)
    @classmethod 
    def update_comment(cls, commentid, title, text, post): 
        comment = Comment.query.get(commentid)
        if title != None: 
            comment.title = title
        if text != None: 
            comment.text = text
        if post != None: 
            comment.post = post 
        db.session.commit()
        return comment_schema.jsonify(comment)

    @classmethod 
    def delete_comment(cls, commentid): 
        comment = Comment.query.get(commentid)
        db.session.delete(comment)
        db.session.commit()
        return comment_schema.jsonify(comment)



# COMMENT SCHEMA 
class CommentSchema(marshmallow.Schema): 
    class Meta: 
        fields = ('id', 'title', 'text', 'post')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


if __name__ == 'models': 
    db.create_all()
