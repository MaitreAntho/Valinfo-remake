import json
from websocket_server import WebsocketServer



class Server:
    def __init__(self, log, Error):
        self.Error = Error
        self.log = log
        self.lastMessage = ""

    def start_server(self):
        try:
            with open('config.json', "r") as conf:
                port = json.load(conf)["port"]
            self.server = WebsocketServer(host='127.0.0.1', port=port)
            self.server.set_fn_new_client(self.handle_new_client)
            self.server.handle_error = self._handle_error
            self.server.run_forever(threaded=True)
        except Exception as e:
            self.Error.PortError(port)

    def _handle_error(self, request, client_address):
        # a stray/incomplete connection (browser private-network preflight, port
        # probe, etc.) shouldn't spam a traceback for every one of these
        self.log(f"discarded a malformed connection from {client_address}")

    def handle_new_client(self, client, server):
        if self.lastMessage != "":
            self.send_message(self.lastMessage)


    def send_message(self, message):
        self.lastMessage = message
        self.server.send_message_to_all(message)

        
    
