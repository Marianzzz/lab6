import random
import os

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
        self.message_handler = GreetingHandler('привіт')
        self.message_handler.set_next_handler(Topic1Handler('тема 1'))
        Topic1Handler('тема 1').set_next_handler(Topic2Handler('тема 2'))
        Topic2Handler('тема 2').set_next_handler(DefaultHandler('default'))

    def respond_to_message(self, message):
        response, message_type = self.message_handler.handle_message(message)
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