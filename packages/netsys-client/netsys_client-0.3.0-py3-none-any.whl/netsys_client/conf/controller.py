from netsys_client.conf.validation import ConfValidation
from netsys_client.conf.methods import ConfMethod

class ConfController:

    _erros = []
    
    def __init__(self, data):

        self.data = data

        self.execute()

    def execute(self):

        validation = ConfValidation(self.data)

        if validation.get_erros():

            self._erros = validation.get_erros()

        else:

            method = ConfMethod()
            
            file_path = method.map_conf_path()
            method.write_conf(file_path, self.data)

    def get_erros(self):

        return self._erros