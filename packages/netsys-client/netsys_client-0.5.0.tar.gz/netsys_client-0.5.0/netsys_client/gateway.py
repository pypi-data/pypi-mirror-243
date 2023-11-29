from . import ConfController, PrintController
from response import Response
import json

class Gateway:

    _erros = []

    def __init__(self):

        self.response = Response()

    def change_config(self, data):
        
        conf = ConfController(data)
        
        if conf.get_erros():

            print(conf.get_erros())

    def search_printers(self):

        print = PrintController()
        message = print.get_printer_list(self._token)
        self.response.send_message(json.dumps(message))
    
    def set_erro(self, erro):

        self._erros.append(erro)

    def set_token(self, token):

        self._token = token