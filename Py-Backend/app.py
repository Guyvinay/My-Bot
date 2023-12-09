from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mybot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

openai.api_key = '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'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100))
    chats = db.relationship('Chat', backref='users', lazy=True)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    conversations = db.relationship('Conversation', backref='chat', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    prompt = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500), nullable=False)

#Creating modals
with app.app_context():
    db.create_all()


#endpoint for creating user
@app.route('/users', methods=['POST'])
def create_users():
    try :
        data = request.get_json()
        username = data.get('username','')
        password = data.get('password','')
        name = data.get('name','')
        # print(data)
        #Checking if user already exists
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user : 
            return jsonify({
                'error':f'username: {username}, already exists!'
            })
        
        #create a new user
        new_user = Users(
            username = username,
            password = password,
            name = name
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'status':'user created successfully',
            'name':new_user.name,
            'user_id':new_user.id
        })
    #Exception handling
    except Exception as ex:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(ex)}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)