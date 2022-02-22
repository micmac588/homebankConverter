from parse import parse
from hb_transaction import HbTransaction


class HbTransactionFraisBancaire(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._FRAIS_BANCAIRE
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):
        p = parse("COMMISSION SUR ACHAT REGLE EN DEVISES OU EN EUROS HORS ZONE EURO {:tg} {}", libelle)
        _payee = "ING DIRECT"
        _info = "Commission sur " + p[1]
        _memo = ""
        return(_info, _payee, _memo)
