import random
import os


class Subscriber:
    def update(self, message, message_type):
        pass


class BotSubscriber(Subscriber):
    def update(self, message, message_type):
        from app.chatbot import ChatBot
        bot_response = ChatBot.get_instance().respond_to_message(message)
        return bot_response, message_type


class MessageProcessingStrategy:
    def process_message(self, message):
        pass


class BasicMessageProcessingStrategy(MessageProcessingStrategy):
    def process_message(self, message):
        pass


class AdvancedMessageProcessingStrategy(MessageProcessingStrategy):
    def process_message(self, message):
        pass


class MessageHandler:
    def __init__(self, keyword):
        self.keyword = keyword
        self.next_handler = None

    def set_next_handler(self, handler):
        self.next_handler = handler

    def handle_message(self, message):
        if self.keyword.lower() in message.lower():
            return self.handle(message)
        elif self.next_handler:
            return self.next_handler.handle_message(message)
        else:
            return None

    def handle(self, message):
        pass


class GreetingHandler(MessageHandler):
    def handle(self, message):
        return "Привіт! Я чат-бот. Як я можу вам допомогти?", "bot"


class Topic1Handler(MessageHandler):
    def handle(self, message):
        return ChatBot.get_instance().get_response_from_file('topic1'), "bot"


class Topic2Handler(MessageHandler):
    def handle(self, message):
        return ChatBot.get_instance().get_response_from_file('topic2'), "bot"


class DefaultHandler(MessageHandler):
    def handle(self, message):
        return "Ви сказали: " + message, "user"




class Notifier:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def notify(self, message, message_type):
        responses = []
        for subscriber in self._subscribers:
            responses.append(subscriber.update(message, message_type))
        return responses


class ChatBot:
    _instance = None

    @staticmethod
    def get_instance():
        if ChatBot._instance is None:
            ChatBot._instance = ChatBot()
        return ChatBot._instance

    def __init__(self):
        self.responses_folder = "responses"
        self._asked_questions = set()

        # Use the factory to create handlers
        greeting_handler = HandlerFactory.create_handler('greeting', 'привіт')
        topic1_handler = HandlerFactory.create_handler('topic1', 'тема 1')
        topic2_handler = HandlerFactory.create_handler('topic2', 'тема 2')
        default_handler = HandlerFactory.create_handler('default', 'default')

        # Set up the chain of responsibility
        greeting_handler.set_next_handler(topic1_handler)
        topic1_handler.set_next_handler(topic2_handler)
        topic2_handler.set_next_handler(default_handler)

        self.message_handler = greeting_handler
        self.notifier = Notifier()

    def respond_to_message(self, message, message_type='user'):
        response, message_type = self.message_handler.handle_message(message)
        self.notifier.notify(message, message_type)
        return response

    def get_response_from_file(self, topic):
        responses_file = os.path.join(self.responses_folder, f"{topic}.txt")
        if os.path.exists(responses_file):
            with open(responses_file, "r", encoding="utf-8") as file:
                responses = file.readlines()
                available_responses = [response.strip() for response in responses if
                                       response.strip().lower() not in self._asked_questions]
                if available_responses:
                    selected_response = random.choice(available_responses)
                    self._asked_questions.add(selected_response.lower())
                    return selected_response, "bot"
                else:
                    return "На жаль, не залишилося доступних відповідей на цю тему.", "bot"
        else:
            return "На жаль, не вдалося знайти відповіді на цю тему.", "bot"
