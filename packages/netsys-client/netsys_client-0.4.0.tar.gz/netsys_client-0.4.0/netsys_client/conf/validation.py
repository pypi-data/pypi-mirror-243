from . import Params

class ConfValidation:

    _erros = []
    
    def __init__(self, data: dict):

        self.data = data

        self.validate()

    def validate(self):

        for key, value in self.data.items():

            if key in Params.params_list:

                try:

                    self.data[key] = str(value)

                except:

                    self._erros.append(f'O valor de {key} precisa ser um texto!')
        
            else:

                self._erros.append(f'O termo {key} não é um parâmetro válido!')

    def get_erros(self):

        return self._erros

        