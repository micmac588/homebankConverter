
class TransactionFactory:

    def __init__(self, logger):
        self.logger = logger

    def get_transaction(self, bank_transaction):
        """
        return an object HbTransaction or an object derived from him.
        """
        raise NotImplementedError
