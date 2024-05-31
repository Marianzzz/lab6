from app.chatbot import ChatBot

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    user_message = data['message']
    bot_response = process_user_message(user_message)
    return jsonify({'response': bot_response})

def process_user_message(user_message):
    return ChatBot.get_instance().respond_to_message(user_message)

if __name__ == '__main__':
    app.run(debug=True)