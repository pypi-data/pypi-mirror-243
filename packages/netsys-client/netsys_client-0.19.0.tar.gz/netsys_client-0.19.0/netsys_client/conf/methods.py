import os

class ConfMethods:

    def map_conf_path(self):

        user_path = os.path.expanduser('~')

        return f'{user_path}/teste.conf'
    
    def read_conf(self, file_path, data: dict):

        with open(file_path, 'r') as file:

            file_dict = {line.split('=')[0].replace('\n', ''): line.split('=')[1].replace('\n', '') for line in file}

        for key, value in data.items():

            file_dict[f'{key}'] = value

        return file_dict

    def write_conf(self, file_path, file_dict):

        with open(file_path, 'w') as file:
            
            for key, value in file_dict.items():

                file.write(f'{key}={value}\n')
