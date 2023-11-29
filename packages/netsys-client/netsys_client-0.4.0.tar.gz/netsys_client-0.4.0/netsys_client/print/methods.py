import win32print

class PrintMethods:

    def get_printer_list(self, token):

        self._printers = {printer[2]: printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)}
        message = {
            'token': token,
            'printers': self._printers
        }

        return message