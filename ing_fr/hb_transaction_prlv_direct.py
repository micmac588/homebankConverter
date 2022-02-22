from parse import parse
from hb_transaction import HbTransaction


class HbTransactionPrlvDirect(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._PRELEVEMENT_DIRECT
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):
        p = parse("PRLV SEPA {transfert_emitter} : {something} {transfert_id_and_emitter} : {something2}", libelle)
        _payee = p['transfert_id_and_emitter']
        _info = ""
        _memo = ""
        return(_info, _payee, _memo)
