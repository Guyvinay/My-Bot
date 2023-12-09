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

#Endpoint for Get All users
@app.route('/users',methods=['GET'])
def get_all_users() :
    try :

        users = Users.query.all()
        users_list = [
            {
                'user_id':user.id,
                'username':user.username,
                'name':user.name
            }
            for user in users
        ]
        print(users_list)
        return jsonify({
            'users':users_list,
            'total_users':len(users_list)
        })

    except Exception as ex : 
        error_message = f"An error occurred: {str(ex)}"
        return jsonify({
            'error':error_message
        })


#Endpoint for Get users by username
@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username) : 
    try:
        # user = Users.query.get(username)
        user = Users.query.filter_by(username=username).first()
        if user:
            return jsonify({'user_id': user.id, 'username': user.username, 'name': user.name})
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

#Endpoint for update user by username
#Endpoint for delete user
# Delete a user
@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        # user = Users.query.get(user_id)
        user = Users.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500




if __name__ == '__main__':
    app.run(debug=True)