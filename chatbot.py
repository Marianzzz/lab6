from flask import Flask, request, jsonify, render_template
from patterns import observer
from patterns.strategy import BasicMessageProcessingStrategy, AdvancedMessageProcessingStrategy

from patterns.singleton import ChatBot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])

def receive_message():
    data = request.get_json()
    user_message = data['message']
    if user_message.lower() == 'привіт' or ChatBot._asked_greetings:
        bot_response, response_type = process_user_message(user_message, data)
    else:
        bot_response, response_type = "Для початку розмови напишіть 'Привіт'.", "bot"
    return jsonify({'response': bot_response, 'message_type': response_type})

def process_user_message(user_message, data):
    bot = ChatBot.get_instance()
    processing_strategy = get_processing_strategy(data)
    message_type = get_message_type(data)
    processing_strategy.process_message(user_message)
    bot_response, response_type = bot.respond_to_message(user_message, message_type)
    return bot_response, response_type

def get_processing_strategy(data):
    return AdvancedMessageProcessingStrategy() if data.get('advanced_processing') else BasicMessageProcessingStrategy()

def get_message_type(data):
    message_type = data.get('message_type')
    return message_type if message_type in ['user', 'bot'] else 'user'

if __name__ == '__main__':
    app.run(debug=True)
