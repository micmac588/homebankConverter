# homebankConverter
It converts your Bank account historic csv file into another csv file you can import in HomeBank application (http://homebank.free.fr/en/).

# pre-requisites
python3 and additionnal packages (see requirements.txt)

# usage
- ``git clone https://github.com/micmac588/homebankConverter.git``

- ``cd homebankConverter``

- ``./homebank_converter.py -i bank_input_file.csv -o homebank_output_file.csv -v``

# linter
- ``flake8``

# testing
- ``coverage run -m  pytest -s``

- ``coverage html``

# limitation
Support french ING Bank account historic only.

# contribution
Contribution are welcomed to add support for new banks.
- Create a new directory (example ing_fr)
- Create a new Class derived from TransactionFactory
- Create a new Class derived from HbTransaction
- Add test, best coverage as possible. Use anonymised data.

# roadmap
- Support of Boursorama

