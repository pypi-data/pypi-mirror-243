class Response:
    def __init__(self, answer, time):
        self.answer = answer
        self.time = time

class Error:
    def __init__(self, message):
        self.message = message

class Conversation:
    def __init__(self, conversation, user):
        self.conversation = conversation
        self.user = user
