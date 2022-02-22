from parse import parse
from hb_transaction import HbTransaction


class HbTransactionCarte(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._CARTE_BANCAIRE
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):

        _info = ""
        _payee = ""
        _memo = ""
        if libelle.startswith("PAIEMENT PAR CARTE") or libelle.startswith("CARTE") or libelle.startswith("RETRAIT DAB"):
            p = parse("{} {:tg} {}", libelle)
            _payee = p[2]
        elif libelle.startswith("ANNUL ACHAT") or libelle.startswith("AVOIR CARTE"):
            p = parse("{}  {}", libelle)
            _payee = p[1]

        return(_info, _payee, _memo)
