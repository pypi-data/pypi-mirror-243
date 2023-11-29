from . import ConfMethods

class ConfController(ConfMethods):
    
    def __init__(self, data):

        self._data = data
        self._file_path = self.map_conf_path()

    def execute(self):
            
        self._file_dict = self.read_conf(self._file_path, self._data)
        self.write_conf(self._file_path, self._file_dict)

    def get_parameter(self, parameter):

        self._file_dict = self.read_conf()
        return self._file_dict[parameter]