from parse import parse
from hb_transaction import HbTransaction


class HbTransactionDepot(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger, category):

        super().__init__(date, amount, currency, logger, category)
        self.payment = HbTransaction._DEPOT
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):

        p = parse("REM CHQ N. {:7d}", libelle)
        _info = str(p[0]).zfill(7)

        return (_info, self.payee, self.memo)
