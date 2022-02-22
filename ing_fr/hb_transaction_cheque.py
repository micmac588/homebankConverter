from parse import parse
import re
from hb_transaction import HbTransaction


class HbTransactionCheque(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._CHEQUE
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):
        _payee = ""
        _info = ""
        _memo = ""
        if re.match(r"CHEQUE", libelle):
            p = parse("CHEQUE {}", libelle)
            _info = "CHEQUE %s" % p[0]
        else:
            if re.match(r"PAIEMENT D'UN CH.*QUE", libelle):
                p = parse("PAIEMENT D'UN CH{}QUE {}", libelle)
                _info = "CHEQUE %s" % p[1]

        return(_info, _payee, _memo)
