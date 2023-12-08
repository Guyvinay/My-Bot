from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mybot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set your OpenAI API key
openai.api_key = ''

class ConversationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2000), nullable=False)

# db.create_all()
with app.app_context():
    db.create_all()
# Maintain conversation history
# conversation_history = []

# Define a route for sending messages to the GPT-3.5 model
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get('message', '')


         # Save user message to the database
        with app.app_context():
            user_history = ConversationHistory(message=f'User: {user_message}')
            db.session.add(user_history)
            db.session.commit()

        # Append user message to the conversation history
        # conversation_history.append(f'User: {user_message}')

        with app.app_context():
            conversation_history = [history.message for history in ConversationHistory.query.all()]

        # Call OpenAI API to get chatbot response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='\n'.join(conversation_history),
            max_tokens=150
        )

        # Extract the generated message from the OpenAI response
        chatbot_response = response['choices'][0]['text'].strip()

        # Append chatbot response to the conversation history
        conversation_history.append(f'Chatbot: {chatbot_response}')
        # print(conversation_history)
        
        with app.app_context():
            chatbot_history = ConversationHistory(message=f'Chatbot: {chatbot_response}')
            db.session.add(chatbot_history)
            db.session.commit()

        # return jsonify(conversation_history)
        return jsonify(chatbot_response)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)