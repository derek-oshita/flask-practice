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
@app.route('/sub', methods=['POST'])
# GET SUB W/ ID
@app.route('/sub/<subid>', methods=['GET'])
def create_sub(subid = None): 
    from models import Sub
    if subid == None: 
        name = request.json['name']
        description = request.json['description']

        return Sub.create_sub(name, description)
    
    else: 
        return Sub.get_sub(subid)


if __name__ == '__main__': 
    app.run(debug=DEBUG, port=PORT)