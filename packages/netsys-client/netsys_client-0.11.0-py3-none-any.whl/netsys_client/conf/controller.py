from . import ConfValidation, ConfMethods

class ConfController(ConfMethods):

    _erros = []
    
    def __init__(self, data):

        self.data = data

        self.execute()

    def execute(self):

        validation = ConfValidation(self.data)

        if validation.get_erros():

            self._erros = validation.get_erros()

        else:
            
            file_path = self.map_conf_path()
            self.write_conf(file_path, self.data)

    def get_erros(self):

        return self._erros