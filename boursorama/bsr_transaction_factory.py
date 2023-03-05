import datetime
from transaction_factory import TransactionFactory
from .hb_transaction_carte import HbTransactionCarte
from .hb_transaction_virement import HbTransactionVirement
from .hb_transaction_cheque import HbTransactionCheque
from .hb_transaction_prlv_direct import HbTransactionPrlvDirect
from .hb_transaction_depot import HbTransactionDepot
from hb_transaction import HbTransaction


class BsrTransactionFactory(TransactionFactory):

    def get_transaction(self, bank_transaction):
        if bank_transaction[0] == 'dateOp':
            return None
        _date = datetime.datetime.strptime(bank_transaction[0], '%Y-%m-%d').strftime('%d-%m-%Y')
        _libelle = bank_transaction[2]
        _category = bank_transaction[3]
        if not _category:
            self.logger.warning("Category not defined")
        _amount = bank_transaction[5]
        _currency = "EUR"

        if _libelle.startswith("CARTE") or \
           _libelle.startswith("RETRAIT") or \
           _libelle.startswith("AVOIR"):
            t = HbTransactionCarte(_date, _libelle, _amount, _currency, self.logger, _category)
        elif _libelle.startswith("VIR"):
            t = HbTransactionVirement(_date, _libelle, _amount, _currency, self.logger, _category)
        elif _libelle.startswith("CHQ."):
            t = HbTransactionCheque(_date, _libelle, _amount, _currency, self.logger, _category)
        elif _libelle.startswith("PRLV SEPA"):
            t = HbTransactionPrlvDirect(_date, _libelle, _amount, _currency, self.logger, _category)
        elif _libelle.startswith("REM CHQ"):
            t = HbTransactionDepot(_date, _libelle, _amount, _currency, self.logger, _category)
        else:
            self.logger.warning("Can't identify payment from _libelle %s" % _libelle)
            t = HbTransaction(_date, _amount, _currency, self.logger, _category)
        return t
