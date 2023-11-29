import win32print

class PrintMethods:

    def get_printer_list(self, token):

        self._printers = {printer[2]: printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)}
        message = {
            'token': token,
            'printers': self._printers
        }

        return message
    
    def execute(self, printer, layout):

        impressora_padrao = win32print.GetDefaultPrinter()
        win32print.SetDefaultPrinter(printer)
        hPrinter = win32print.OpenPrinter(printer)
        win32print.StartDocPrinter(hPrinter, 1, ('TestPrintJob', None, 'RAW'))
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, layout.encode())
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.SetDefaultPrinter(impressora_padrao)