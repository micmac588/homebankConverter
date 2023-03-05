import re
from datetime import datetime


class HbTransaction():

    """
    see http://homebank.free.fr/help/misc-csvformat.html
    """

    _AUCUN = 0
    _CARTE_BANCAIRE = 1
    _CHEQUE = 2
    _ESPECE = 3
    _VIREMENT = 4
    _VIREMENT_INTERNE = 5  # Can't use it for import
    _CARTE_DE_DEBIT = 6
    _VIREMENT_PERMANENT = 7
    _PAIEMENT_ELECTRONIQUE = 8
    _DEPOT = 9
    _FRAIS_BANCAIRE = 10
    _PRELEVEMENT_DIRECT = 11

    def __init__(self, date, amount, currency, logger, category=""):
        self.date = date
        self._assertDate()
        self.amount = amount
        self._assertAmount()
        self.currency = currency
        self._assertCurrency()
        self.category = ""  # not managed
        self.logger = logger
        self.payment = self._AUCUN
        self.info = ""
        self.payee = ""
        self.memo = ""
        self.tags = ""  # not managed

    def _assertDate(self):
        """
        Check the date is HomeBank compatible
        """
        datetime.strptime(self.date, "%d-%m-%Y")

    def _assertAmount(self):
        """
        Check the amount is HomeBank compatible: n digits,2 digits
        example: 12345,80
        """
        if not re.match(r".*\d,\D*(\d)\D*(\d)\D*$", self.amount):
            raise ValueError("Unexpected amount %s" % self.amount)

    def _assertCurrency(self):
        """
        Check the currency is euro (€)
        """
        if self.currency != "EUR":
            raise ValueError("Unexpected currency %s" % self.currency)

    def toCsv(self):
        return (self.date, self.payment, self.info, self.payee, self.memo, self.amount, self.category, self.tags)

    def __str__(self):
        return "%s;%s;%s;%s;%s;%s;%s;%s" % (self.date, self.payment, self.info, self.payee, self.memo, self.amount, self.category, self.tags)
