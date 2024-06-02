

class HandlerFactory:
    @staticmethod
    def create_handler(handler_type, keyword):
        if handler_type == 'greeting':
            return GreetingHandler(keyword)
        elif handler_type == 'topic1':
            return Topic1Handler(keyword)
        elif handler_type == 'topic2':
            return Topic2Handler(keyword)
        elif handler_type == 'default':
            return DefaultHandler(keyword)
        else:
            raise ValueError(f"Unknown handler type: {handler_type}")
