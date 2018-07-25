import json
from websocket import create_connection


#socket = 'ws://mwstest.infrontservices.com/mws'
socket = 'wss://mws_beta_001.infrontservices.com/Beta_001'

#Function to send load via websocket
def socketconn(socket,load):
    try:
        ws = create_connection(socket)
        ws.send(json.dumps(load))
    except ValueError:
        print("Connection Error: Server cannot be reached")
    response = ws.recv()
    response_eval = json.loads(response)
    return response_eval

#Object to handle connection
class InfrontConnect:
    def __init__(self, username, password):
        self.username = username
        self.password = password
# login request without keep alive
    def login(self):
        global md_login_token
        md_login_request = {
            "request_data": "ValueToBeReturnedInResponse",
            "md_login_request":
            {
                "login_id": self.username,
                "password": self.password,
                "client_application": "WEB",
                "client_application_version": "1.0",
                "country_code": "no",
                "language_code": "en"
            }
            }
        response = socketconn(socket,md_login_request)
        md_login_token = response['session_token']
        return md_login_token
# Keep alive requests based on login() request
    def login_keepAlive(self):
        md_keep_alive_request = {"session_token": self.login(),
                                 "md_keep_alive_request": {}}
        reponse = socketconn(socket,md_keep_alive_request)
        error_code = reponse['error_code']
        if error_code != 0:
            print("Error on login_keepAlive")
        else:
            print("Connected! Session is kept alive.")
        return md_login_token



