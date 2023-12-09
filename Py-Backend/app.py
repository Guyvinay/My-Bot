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
    prompt = db.Column(db.String(1500), nullable=False)
    response = db.Column(db.String(4000), nullable=False)

#Creating modals
with app.app_context():
    db.create_all()

# conversation_history = []

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

# Users-OPS-OVER-HERE

#Chats-OPS-STARTS-here

#Endpoint for creating Chat
@app.route('/chats/<username>', methods=['POST'])
def create_chats(username) : 
    try :
        data = request.get_json()
        title = data.get('title','')
        description = data.get('description','')
        # print(title+" "+description)
        user = Users.query.filter_by(username=username).first()
        print(user)
        if user :
            new_chat = Chat(
                user_id = user.id,
                title = title,
                description = description
            )
            db.session.add(new_chat)
            db.session.commit()
            return jsonify({
                'chat_id':new_chat.id,
                'chat_title':new_chat.title,
                'user_name':user.username
            })
        else :
            return jsonify({
                'error':f'User: {username} not found!'
            })

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

# Get all chats
@app.route('/chats', methods=['GET'])
def get_all_chats():
    try:
        chats = Chat.query.all()  # Use user_id instead of users
        chat_list = [{'chat_id': chat.id, 'title': chat.title, 'description': chat.description} for chat in chats]
        return jsonify(
            {
                'chats': chat_list,
                'total_chats':len(chat_list)
                }
            )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


# Get all chats for a user
@app.route('/chats/<username>', methods=['GET'])
def get_chats_of_a_user(username):
    try:
        user = Users.query.filter_by(username=username).first()
        if not user :
            return jsonify({
                'error':f'Username: {username}, not found!'
            })
        chats = Chat.query.filter_by(user_id=user.id).all()  # Use user_id instead of users
        chat_list = [{'chat_id': chat.id, 'title': chat.title, 'description': chat.description} for chat in chats]
        return jsonify(
            {
                'chats': chat_list,
                'total_chats':len(chat_list)
                }
            )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

# Get a particular chats for a user
@app.route('/chats/<username>/<chat_id>', methods=['GET'])
def get_a_chat_of_a_user(username, chat_id):
    try:
        # print(username+" "+chat_id)
        user = Users.query.filter_by(username=username).first()
        if not user :
            return jsonify({
                'error':f'Username: {username}, not found!'
            })
        
        chat = Chat.query.filter_by(id=chat_id,user_id=user.id).first()
        if not chat :
           return jsonify({
                'error':f'Chat ID: {chat_id}, not found!'
            })
        
        print(chat.conversations[3].response)

        # chat_list = [{'chat_id': chat.id, 'title': chat.title, 'description': chat.description} for chat in user.chats]
        # print(chat_list)


        conversation_list = [
            {
                'conversation_id': conversation.id, 'prompt': conversation.prompt, 
                'description': conversation.response
            } 
            for conversation in chat.conversations
            ]
        print(conversation_list)


        # print(chat.title)
        # chat = next(
        #     (chat for chat in user.chats if chat['id'] == chat_id),
        #     None
        # )
        # print([{'chat':chat.title}for chat in user.chats])

        return jsonify({
            'id':chat.id,
            'title':chat.title,
            'description':chat.description,
            'user_id':chat.user_id,
            'conversations':conversation_list,
            'total_conversation':len(conversation_list)
        })

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

# Delete a chat
@app.route('/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    try:
        chat = Chat.query.get(chat_id)
        if chat:
            db.session.delete(chat)
            db.session.commit()
            return jsonify({'message': 'Chat deleted successfully'})
        else:
            return jsonify({'error': 'Chat not found'}), 404

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

# Delete a chat of a user
@app.route('/chats/<username>/<chat_id>', methods=['DELETE'])
def delete_chat_of_a_user(username,chat_id):
    try:
        user = Users.query.filter_by(username=username).first()
        if not user :
            return jsonify({
                'error':f'Username: {username}, not found!'
            })
        
        chat = Chat.query.filter_by(id=chat_id,user_id=user.id).first()

        if not chat :
            return jsonify({
                'error':f'Chat ID: {chat_id}, not found!'
            })
        
        db.session.delete(chat)
        db.session.commit()
        return jsonify({'message': 'Chat deleted successfully'})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

#chat-OPS-DONE-here

#Conversation-withopen-ai-starts-here
@app.route('/chats/<username>/<chat_id>',methods=['POST'])
def create_conversation_with_openai(username,chat_id) : 
    try :
        data = request.get_json()
        prompt = data.get('prompt','')
        user_prompt = data.get('prompt','')
        # print(username+" "+chat_id)
        #Retrieving user with username
        user = Users.query.filter_by(username=username).first()
        if not user :
            return jsonify({
                'error':f'Username: {username}, not found!'
            })
        #Retrieving chat with chat_id
        chat = Chat.query.filter_by(id=chat_id,user_id=user.id).first()

        if not chat :
           return jsonify({
                'error':f'Chat ID: {chat_id}, not found!'
            })

        conversation_history = Conversation.query.filter_by(chat_id=chat_id).all()
        # print(conversation_history)

        if conversation_history:
            chat_history = '\n'.join([f'User: {conv.prompt}\nChatbot: {conv.response}' for conv in conversation_history])
            prompt = f'{chat_history}\nUser: {prompt}\n'
        else:
            # If no conversation history exists, start with the user's prompt
            prompt = f'User: {prompt}\n'

        print(prompt)

        #Calling open AI api 
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'{prompt}\n',
            max_tokens=150
        )

        # Extract the generated message from the OpenAI response
        bot_response = response['choices'][0]['text'].strip()

        new_conversation = Conversation(chat_id=chat_id, prompt=user_prompt, response=bot_response)
        db.session.add(new_conversation)
        db.session.commit()

        print(new_conversation)


        return jsonify({
            "prompt":new_conversation.prompt,
            "response":bot_response
        })


    except Exception as ex : 
        error_message = f"An error occurred: {str(ex)}"
        return jsonify({'error': error_message}), 500

# Getting conversation of a particular chat
# @app.route('/chats/<username>/<chat_id>/')


if __name__ == '__main__':
    app.run(debug=True)