from parse import parse
from hb_transaction import HbTransaction


class HbTransactionPrlvDirect(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger, category):

        super().__init__(date, amount, currency, logger, category)
        self.payment = HbTransaction._PRELEVEMENT_DIRECT
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):
        p = parse("PRLV SEPA {payee}", libelle)
        _payee = p['payee']
        return (self.info, _payee, self.memo)
