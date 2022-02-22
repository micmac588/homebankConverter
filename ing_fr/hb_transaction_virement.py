from parse import parse
from hb_transaction import HbTransaction


class HbTransactionVirement(HbTransaction):

    def __init__(self, date, libelle, amount, currency, logger):

        super().__init__(date, amount, currency, logger)
        self.payment = HbTransaction._VIREMENT
        self.parse_libelle(libelle)

    def parse_libelle(self, libelle):
        self.payee = ""
        self.info = ""
        self.memo = ""

        if libelle.startswith("VIREMENT SEPA EMIS VERS"):
            self._process_virement_sep_emis_vers(libelle)
        elif libelle.startswith("VIREMENT RECU"):
            self._process_virement_recu(libelle)
        elif libelle.startswith("VIREMENT EMIS VERS"):
            p = parse("VIREMENT EMIS VERS {} {:11d} {}", libelle)
            self.payee = p[0] + " " + str(p[1]).zfill(11)
            self.info = p[2]
        elif libelle.startswith("VIREMENT SEPA RECU"):
            p = parse("VIREMENT SEPA RECU {}", libelle)
            self.payee = p[0]

    def _process_virement_sep_emis_vers(self, libelle):
        try:
            p = parse("VIREMENT SEPA EMIS VERS {} {:11d} {}", libelle)
            self.payee = p[0] + " " + str(p[1]).zfill(11)
            self.info = p[2]
        except TypeError:
            try:
                p = parse("VIREMENT SEPA EMIS VERS  {:11d} {}", libelle)
                self.payee = str(p[0]).zfill(11)
                self.info = p[1]
            except TypeError:
                try:
                    p = parse("VIREMENT SEPA EMIS VERS   {}", libelle)
                    self.payee = ""
                    self.info = p[0]
                except TypeError:
                    p = parse("VIREMENT SEPA EMIS VERS", libelle)
                    self.payee = ""
                    self.info = ""

    def _process_virement_recu(self, libelle):
        try:
            p = parse("VIREMENT RECU {} {:11d} {}", libelle)
            self.info = p[2]
        except TypeError:
            p = parse("VIREMENT RECU {} {:11d}", libelle)
            self.info = ""
        try:
            self.payee = p[0] + " " + str(p[1]).zfill(11)
        except TypeError:
            p = parse("VIREMENT RECU {:11d} {}", libelle)
            self.payee = str(p[0]).zfill(11)
            self.info = p[1]
