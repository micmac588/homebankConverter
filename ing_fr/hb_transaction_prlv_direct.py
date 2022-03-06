from parse import parse
from hb_transaction import HbTransaction


class HbTransactionPrlvDirect(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._PRELEVEMENT_DIRECT
        (self.info, self.payee, self.memo) = self.parseLibelle(libelle)

    def parseLibelle(self, libelle):
        p = parse("PRLV SEPA {transfert_emitter} : {something} {transfert_id} DE {transfert_emitter2} : {something2}", libelle)
        _payee = p['transfert_emitter']
        _info = p['transfert_id']
        _memo = ""
        if p['transfert_emitter'] != p['transfert_emitter2']:
            self.logger.warning("Something unexpected here!")
        return(_info, _payee, _memo)
