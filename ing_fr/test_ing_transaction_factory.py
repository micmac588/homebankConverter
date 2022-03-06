import pytest
import logging
from ing_transaction_factory import IngTransactionFactory

normal_cases_input = [
    (["26/05/2020", "PAIEMENT PAR CARTE 22/05/2020 payee", "", "-5,80", "EUR"], 1, "payee", ""),
    (["16/08/2019", "ANNUL ACHAT  payee", "", "16,02", "EUR"], 1, "payee", ""),
    (["28/04/2020", "PAIEMENT D'UN CH�QUE 1234567", "", "-147,94", "EUR"], 2, "", "CHEQUE 1234567"),
    (["19/02/2020", "CHEQUE 3969751", "", "-25,00", "EUR"], 2, "", "CHEQUE 3969751"),
    (["27/04/2020", "PRLV SEPA payee : something1 transfert_id DE payee : something2", "", "-57,48", "EUR"], 11, "payee", "transfert_id"),
    (["25/04/2020", "RETRAIT DAB EN EURO ZONE EURO 24/04/2020 payee", "", "-80,00", "EUR"], 1, "payee", ""),
    (["20/04/2020", "VIREMENT SEPA RECU payee", "", "2000,00", "EUR"], 4, "payee", ""),
    (["03/02/2020", "VIREMENT EMIS VERS payee 01234567891 info", "", "-100,00", "EUR"], 4, "payee 01234567891", "info"),
    (["20/01/2020", "VIREMENT RECU payee 00123456789 info", "", "487,89", "EUR"], 4, "payee 00123456789", "info"),
    (["21/01/2020", "VIREMENT RECU payee 98765432100", "", "487,89", "EUR"], 4, "payee 98765432100", ""),
    (["22/01/2020", "VIREMENT RECU 44444444444 info", "", "487,89", "EUR"], 4, "44444444444", "info"),
    (["01/04/2020", "VIREMENT SEPA EMIS VERS payee 01234567890 info", "", "-100,00", "EUR"], 4, "payee 01234567890", "info"),
    (["02/04/2020", "VIREMENT SEPA EMIS VERS  01234567890 info", "", "-200,00", "EUR"], 4, "01234567890", "info"),
    (["12/10/2019", "VIREMENT SEPA EMIS VERS   info", "", "-4000,00", "EUR"], 4, "", "info"),
    (["01/03/2020", "VIREMENT SEPA EMIS VERS", "", "-200,00", "EUR"], 4, "", ""),
    (["23/08/2021", "REMISE CHEQUE(S) 0000879", "", "2116,80", "EUR"], 9, "", "0000879"),
    (["06/08/2019", "COMMISSION SUR ACHAT REGLE EN DEVISES OU EN EUROS HORS ZONE EURO 05/08/2019 37.4 GBP", "", "-0,82", "EUR"], 10, "ING DIRECT", "Commission sur 37.4 GBP"),
    (["07/08/2019", "UNEXPECTED PREFIX", "", "-200,00", "EUR"], 0, "", "")
]


@pytest.mark.parametrize("ing_transaction, expected_payment, expected_payee, expected_info", normal_cases_input)
def test_normal_cases(ing_transaction, expected_payment, expected_payee, expected_info):
    f = IngTransactionFactory(logging)
    t = f.get_transaction(ing_transaction)
    t.toCsv()
    print("%s" % t)
    assert t.payment == expected_payment
    assert t.payee == expected_payee
    assert t.info == expected_info


error_cases_input = [
    (["blabla", "PAIEMENT PAR CARTE 22/05/2020 INVALID DATE", "", "5,80", "EUR"]),
    (["01/05/2020", "PAIEMENT PAR CARTE 22/05/2020 INVALID AMOUNT1", "", "blabla", "EUR"]),
    (["02/05/2020", "PAIEMENT PAR CARTE 22/05/2020 INVALID AMOUNT2", "", "5,800", "EUR"]),
    (["02/05/2020", "PAIEMENT PAR CARTE 22/05/2020 INVALID AMOUNT3", "", "5,801", "EUR"]),
    (["02/05/2020", "PAIEMENT PAR CARTE 22/05/2020 INVALID AMOUNT4", "", "5.80", "EUR"]),
    (["02/05/2020", "PAIEMENT PAR CARTE 22/05/2020 INVALID CURRENCY", "", "5,80", "USD"]),
]


@pytest.mark.parametrize("ing_transaction", error_cases_input)
def test_error_cases(ing_transaction):
    f = IngTransactionFactory(logging)
    with pytest.raises(ValueError):
        f.get_transaction(ing_transaction)
