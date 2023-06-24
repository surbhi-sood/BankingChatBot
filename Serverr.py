from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from chatbot import get_response, get_response2
import pyttsx3

engine = pyttsx3.init()


class ChatServer(WebSocket):
    current_question = None
    has_greeted = False

    def handleMessage(self):
        message = self.data
        #engine.setProperty('rate', 160)

        if self.current_question is None:
            # No current question, process the user's message
            response = get_response(message)

            a = get_response2(message)
        elif self.current_question is not None:
            # User clicked on a suggested question, use it as the next input
            response = get_response(self.current_question)
            a = get_response2(self.current_question)

            self.current_question = None

        self.sendMessage(response)
        if a != "":
            self.sendMessage(" {}".format(a))
        # engine.say(response)
        # engine.runAndWait()
    def handleConnected(self):
        print(self.address, 'connected')

        if not self.has_greeted:
            greeting_messages = [
                "Hi, I am Rapid!",
                "Welcome to SSFB chat server!",
                "How may I help you?"
            ]

            for message in greeting_messages:
                self.sendMessage(message)

            self.has_greeted = True
            # engine.say(greeting_messages)
            # engine.runAndWait()

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()
