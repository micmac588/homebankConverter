from parse import parse
import re
from hb_transaction import HbTransaction


class HbTransactionCheque(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger, category):

        super().__init__(date, amount, currency, logger, category)
        self.payment = HbTransaction._CHEQUE
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):
        p = parse("CHQ. {}", libelle)
        _info = "CH. %s" % p[0]
        return (_info, self.payee, self.memo)
