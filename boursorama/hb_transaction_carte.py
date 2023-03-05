from parse import parse
from hb_transaction import HbTransaction


class HbTransactionCarte(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger, category):

        super().__init__(date, amount, currency, logger, category)
        self.payment = HbTransaction._CARTE_BANCAIRE
        if category.startswith('Autorisation paiement'):
            self.parseLibelleWhenEnCours(libelle)
        else:
            self.parseLibelle(libelle)

    def parseLibelleWhenEnCours(self, libelle):
        self.payee = libelle

    def parseLibelle(self, libelle):
        if libelle.startswith("CARTE"):
            p = parse("CARTE {} {payee} CB*{cb_num}", libelle)
        elif libelle.startswith("RETRAIT DAB"):
            p = parse("{payee} DAB {} CB*{cb_num}", libelle)
        elif libelle.startswith("AVOIR"):
            p = parse("AVOIR {} {payee} CB*{cb_num}", libelle)
        else:
            raise ValueError("Can't identify payee from libelle %s" % libelle)

        self.logger.debug("p %s" % p)

        self.info = "CB*" + p['cb_num']
        self.payee = p['payee']
