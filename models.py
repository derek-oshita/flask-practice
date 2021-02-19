from app import db, marshmallow
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
    created_at = db.Column(db.DateTime())
    user = db.Column(db.String(100))
    sub = db.Column(db.Integer, db.ForeignKey("sub.id"))
    

if __name__ == 'models': 
    db.create_all()
