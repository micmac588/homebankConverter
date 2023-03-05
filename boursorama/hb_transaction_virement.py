from parse import parse
from hb_transaction import HbTransaction


class HbTransactionVirement(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger, category):

        super().__init__(date, amount, currency, logger, category)
        self.payment = HbTransaction._VIREMENT
        (self.info, self.payee, self.memo) = self.parse_libelle(libelle)

    def parse_libelle(self, libelle):
        if libelle.startswith("VIR INST") or libelle.startswith("VIR SEPA"):
            p = parse("VIR {} {payee}", libelle)
        elif libelle.startswith("VIR"):
            p = parse("VIR {payee}", libelle)
        else:
            raise ValueError("Can't identify payee from libelle %s" % libelle)

        return (self.info, p['payee'], self.memo)
