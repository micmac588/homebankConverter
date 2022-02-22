from parse import parse
from hb_transaction import HbTransaction


class HbTransactionVirement(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._VIREMENT
        (self.info, self.payee, self.memo) = self.parse_libelle(libelle)

    def parse_libelle(self, libelle):
        _payee = ""
        _info = ""
        _memo = ""

        if libelle.startswith("VIREMENT SEPA EMIS VERS"):
            try:
                p = parse("VIREMENT SEPA EMIS VERS {} {:11d} {}", libelle)
                _payee = p[0] + " " + str(p[1]).zfill(11)
                _info = p[2]
            except TypeError:
                try:
                    p = parse("VIREMENT SEPA EMIS VERS  {:11d} {}", libelle)
                    _payee = str(p[0]).zfill(11)
                    _info = p[1]
                except TypeError:
                    try:
                        p = parse("VIREMENT SEPA EMIS VERS   {}", libelle)
                        _payee = ""
                        _info = p[0]
                    except TypeError:
                        p = parse("VIREMENT SEPA EMIS VERS", libelle)
                        _payee = ""
                        _info = ""
        elif libelle.startswith("VIREMENT RECU"):
            try:
                p = parse("VIREMENT RECU {} {:11d} {}", libelle)
                _info = p[2]
            except TypeError:
                p = parse("VIREMENT RECU {} {:11d}", libelle)
                _info = ""
            try:
                _payee = p[0] + " " + str(p[1]).zfill(11)
            except TypeError:
                p = parse("VIREMENT RECU {:11d} {}", libelle)
                _payee = str(p[0]).zfill(11)
                _info = p[1]
        elif libelle.startswith("VIREMENT EMIS VERS"):
            p = parse("VIREMENT EMIS VERS {} {:11d} {}", libelle)
            _payee = p[0] + " " + str(p[1]).zfill(11)
            _info = p[2]
        elif libelle.startswith("VIREMENT SEPA RECU"):
            p = parse("VIREMENT SEPA RECU {}", libelle)
            _payee = p[0]

        return(_info, _payee, _memo)
