from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from chatbot import get_response, get_response2


class ChatServer(WebSocket):
    
    def handleMessage(self):
        # echo message back to client
        message = self.data
        # message1=self.data

        response = get_response(message)
        a = get_response2(message)

        self.sendMessage(response)
        if a != "":
            self.sendMessage(a)


        # self.sendMessage(a)

    def handleConnected(self):
        print(self.address, 'connected')
        greeting_messages = [
            "Hi, I am Rapid!",
            "Welcome to SSFB chat server!",
            "How may I help you?"
        ]

        for message in greeting_messages:
            self.sendMessage(message)
            



    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()
