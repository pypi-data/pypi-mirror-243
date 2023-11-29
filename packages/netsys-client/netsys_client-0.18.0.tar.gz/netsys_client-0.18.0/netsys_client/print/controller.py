from . import PrintMethods, PrintLayout

class PrintController(PrintMethods, PrintLayout):

    def print_data(self, data):

        data['txt1'] = "<CUPOM NAO FISCAL>"
        data['txt2'] = "<TROCA SOMENTE COM APRESENTACAO DESTE>"
        data['txt3'] = "<VOLTE SEMPRE>"

        if data['tipolayout'] == 1:
            layout = self.get_layout_default(data)
        else:
            layout = self.get_layout_consignado(data)

        printer = 'EPSON'

        self.execute(printer, layout)