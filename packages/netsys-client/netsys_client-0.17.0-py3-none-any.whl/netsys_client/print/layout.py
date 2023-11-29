class PrintLayout:

    def get_layout_default(self, data):

        self._layout = f"""
========================================
{data['dt'][:10].ljust(10)}                         {data['hour'][:5].ljust(5)}
{data['razao'][:40].center(40)}
{data['endereco'][:40].center(40)}
{data['tel'][:40].center(40)}
{data['txt1'][:40].center(40)}
----------------------------------------
CLIENTE: {data['clienteid'][:6].ljust(6)} | {data['clientedsc'][:20].ljust(20)}
TIPO PAGAMENTO: {data['tipopg'][:9].ljust(9)} | PARCELAS: {data['qtdparc'][:2].ljust(2)}
VENCIMENTOS:
        """
    
        for i in range(1, int(data['qtdparc']) + 1):

            self._layout += f"""
{data[f'vencimento{i}']['vencdt']}
VLR: R$ {data[f'vencimento{i}']['vencdvlr']}
            """

        self._layout += """
----------------------------------------
CODIGO | DESCRICAO
    QTDE x R$ UND | R$ DESC | R$ VLR
----------------------------------------
        """
    
        for i in range(1, int(data['qtdtotal']) + 1):

            self._layout += f"""
{data[f'produto{i}']['prodid'][:6].ljust(6)} | {data[f'produto{i}']['proddsc'][:31].center(31)}
{data[f'produto{i}']['prodqtd'][:3].ljust(3)} x R$ {data[f'produto{i}']['proddvlr'][:10].ljust(3)} | R$ {data[f'produto{i}']['proddesconto'][:11].ljust(3)} | R$ {data[f'produto{i}']['prodtotal'][:11].ljust(3)}
            """

        self._layout += f"""
----------------------------------------
            Sub Total..:  R$  {data['subtotal'][:10].ljust(10)}
            Desconto...:  R$  {data['desconto'][:10].ljust(10)}
            Total Geral:  R$  {data['totalgeral'][:10].ljust(10)}

            Valor Pago.:  R$  {data['valorpago'][:10].ljust(10)}
            Troco......:  R$  {data['troco'][:10].ljust(10)}
----------------------------------------
VENDEDOR: {data['userid'][:6].ljust(6)} | {data['userdsc'][:20].ljust(20)}
----------------------------------------
{data['txt2'][:40].center(40)}
{data['txt3'][:40].center(40)}
========================================
        """ 
    
        return self._layout

    def get_layout_consignado(self, data):

        self._layout = f"""
========================================
{data['dt'][:10].ljust(10)}                         {data['hour'][:5].ljust(5)}
{data['razao'][:40].center(40)}
{data['endereco'][:40].center(40)}
{data['tel'][:40].center(40)}
{data['txt1'][:40].center(40)}
----------------------------------------
CLIENTE: {data['clienteid'][:6].ljust(6)} | {data['clientedsc'][:20].ljust(20)}
TIPO PAGAMENTO: {data['tipopg'][:9].ljust(9)}
PRAZO DE DEVOLUCAO: {data['devolucao'][:8].ljust(8)}
----------------------------------------
CODIGO | DESCRICAO
    QTDE x R$ UND | R$ VLR
----------------------------------------
        """

        for i in range(1, int(data['qtdtotal']) + 1):

            self._layout += f"""
{data[f'produto{i}']['prodid'][:6].ljust(6)} | {data[f'produto{i}']['proddsc'][:31].center(31)}
{data[f'produto{i}']['prodqtd'][:3].ljust(3)} x R$ {data[f'produto{i}']['proddvlr'][:10].ljust(3)} | R$ {data[f'produto{i}']['prodtotal'][:11].ljust(3)}
            """

        self._layout += f"""
----------------------------------------
            Total Geral:  R$  {data['totalgeral'][:10].ljust(10)}
----------------------------------------
VENDEDOR: {data['userid'][:6].ljust(6)} | {data['userdsc'][:20].ljust(20)}
----------------------------------------
{data['txt2'][:40].center(40)}
{data['txt3'][:40].center(40)}
========================================
        """ 

        return self._layout