#!/usr/bin/env python3
import argparse
import csv
import logging
from ing_fr.ing_transaction_factory import IngTransactionFactory


def prepare_logger(logger_name, verbosity, log_file=None):
    """Initialize and set the logger.

    :param logger_name: the name of the logger to create
    :type logger_name: string
    :param verbosity: verbosity level: 0 -> default, 1 -> info, 2 -> debug
    :type  verbosity: int
    :param log_file: if not None, file where to save the logs.
    :type  log_file: string (path)
    :return: a configured logger
    :rtype: logging.Logger
    """

    logging.getLogger('parse').setLevel(logging.ERROR)

    logger = logging.getLogger(logger_name)

    log_level = logging.WARNING - (verbosity * 10)
    log_format = "[%(filename)-30s:%(lineno)-4d][%(levelname)-7s] %(message)s"
    logging.basicConfig(format=log_format, level=log_level)

    # create and add file logger
    if log_file:
        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="The ING csv file.", required=True)
    parser.add_argument("-o", "--outputfile", help="The HomeBank csv file.", required=False, default="homebank.csv")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase the verbosity", required=False)
    parser.add_argument("-l", "--logfile", help="log file name", required=False)

    args = parser.parse_args()

    input_file = args.inputfile
    ouput_file = args.outputfile
    logger = prepare_logger("homebank_converter", args.verbosity, args.logfile)

    with open(input_file, "r", encoding="ISO-8859-1") as fi:
        with open(ouput_file, "w", encoding="ISO-8859-1") as fo:

            icsv = csv.reader(fi, delimiter=';')
            ocsv = csv.writer(fo, delimiter=';')

            factory = IngTransactionFactory(logger)
            nb_lines = 0
            for row in icsv:
                logger.debug("process %s" % row)
                t = factory.get_transaction(row)
                logger.debug("result  [%s]" % t)
                ocsv.writerow(t.toCsv())
                nb_lines += 1

            logger.info("%s lines processed." % nb_lines)


if __name__ == "__main__":
    main()
