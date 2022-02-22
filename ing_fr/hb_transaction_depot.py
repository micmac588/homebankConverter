from parse import parse
from hb_transaction import HbTransaction


class HbTransactionDepot(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._DEPOT
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):

        p = parse("REMISE CHEQUE(S) {:7d}", libelle)
        _payee = ""
        _info = str(p[0]).zfill(7)
        _memo = ""

        return(_info, _payee, _memo)
