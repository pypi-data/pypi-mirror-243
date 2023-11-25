from netsys_client.conf.controller import ConfController
from .response import Response
import win32print

class Gateway:

    _erros = []
    _printers = []

    def __init__(self):

        self.response = Response()

    def change_config(self, data):
        
        conf = ConfController(data)
        
        if conf.get_erros():

            print(conf.get_erros())

    def search_printers(self):

        self._printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
        self.response.send_message(self._printers)

    def set_erro(self, erro):

        self._erros.append(erro)

    def get_printers(self):

        return self._printers