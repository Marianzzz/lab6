import spacy
import random
import os
class ChatBot:
    _instance = None
    _subscribers = []
    _subscribers = []
    _asked_greetings = set()

    @staticmethod
    def get_instance():
        if ChatBot._instance is None:
            ChatBot._instance = ChatBot()
        return ChatBot._instance

    def __init__(self):
        self.greeting_message = "Привіт! Я чат-бот. Як я можу вам допомогти?"
        self.nlp = spacy.load("xx_ent_wiki_sm")
        self.responses_folder = "responses"
        self._asked_questions = set()

    def respond_to_message(self, message, message_type=None):
        if message_type == "bot":
            return self.get_response_from_file(message)
        elif 'привіт' in message.lower() and message not in ChatBot._asked_greetings:
            ChatBot._asked_greetings.add(message)
            return self.greeting_message, "bot"
        elif 'хто ти' in message.lower() or 'твоє ім' in message.lower():
            return "Я чат-бот, який може поспілкуватись з вами, щоб розпочати напишіть Тема 1 або Тема 2.", "bot"
        elif 'тема 1' in message.lower():
            return self.get_response_from_file("topic1")
        elif 'тема 2' in message.lower():
            return self.get_response_from_file("topic2")
        else:
             return "Ви сказали: " + message, "user"

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

    @staticmethod
    def add_subscriber(subscriber):
        ChatBot._subscribers.append(subscriber)

    @staticmethod
    def notify_subscribers(message):
        for subscriber in ChatBot._subscribers:
            subscriber.update(message)