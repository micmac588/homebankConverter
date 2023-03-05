import re
from transaction_factory import TransactionFactory
from .hb_transaction_carte import HbTransactionCarte
from .hb_transaction_virement import HbTransactionVirement
from .hb_transaction_cheque import HbTransactionCheque
from .hb_transaction_frais_bancaire import HbTransactionFraisBancaire
from .hb_transaction_prlv_direct import HbTransactionPrlvDirect
from .hb_transaction_depot import HbTransactionDepot
from hb_transaction import HbTransaction


class IngTransactionFactory(TransactionFactory):

    def get_transaction(self, bank_transaction):

        _date = bank_transaction[0]
        _libelle = bank_transaction[1]
        _amount = bank_transaction[3]
        _currency = bank_transaction[4]

        if _libelle.startswith("PAIEMENT PAR CARTE") or \
           _libelle.startswith("CARTE") or \
           _libelle.startswith("RETRAIT DAB") or \
           _libelle.startswith("ANNUL ACHAT") or \
           _libelle.startswith("AVOIR CARTE"):
            t = HbTransactionCarte(_date, _libelle, _amount, _currency, self.logger)
        elif _libelle.startswith("VIREMENT EMIS VERS") or _libelle.startswith("VIREMENT SEPA EMIS VERS") or _libelle.startswith("VIREMENT RECU") or _libelle.startswith("VIREMENT SEPA RECU"):
            t = HbTransactionVirement(_date, _libelle, _amount, _currency, self.logger)
        elif re.match(r"PAIEMENT D'UN CH.*QUE", _libelle) or re.match(r"CHEQUE", _libelle):
            t = HbTransactionCheque(_date, _libelle, _amount, _currency, self.logger)
        elif _libelle.startswith("PRLV SEPA"):
            t = HbTransactionPrlvDirect(_date, _libelle, _amount, _currency, self.logger)
        elif _libelle.startswith("COMMISSION SUR ACHAT REGLE EN DEVISES OU EN EUROS HORS ZONE EURO"):
            t = HbTransactionFraisBancaire(_date, _libelle, _amount, _currency, self.logger)
        elif _libelle.startswith("REMISE CHEQUE(S)"):
            t = HbTransactionDepot(_date, _libelle, _amount, _currency, self.logger)
        else:
            self.logger.warning("Can't identify payment from _libelle %s" % _libelle)
            t = HbTransaction(_date, _amount, _currency, self.logger)
        return t
