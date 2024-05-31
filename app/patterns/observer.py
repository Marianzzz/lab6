class Subscriber:
    def update(self, message):
        pass

class BotSubscriber(Subscriber):
    def update(self, message, message_type):
        from app.chatbot import ChatBot
        bot_response = ChatBot.get_instance().respond_to_message(message)
        return bot_response, message_type
