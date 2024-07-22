# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class YourConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        # Process the received data
        self.send(text_data=json.dumps({
            'message': 'Response from server'
        }))
