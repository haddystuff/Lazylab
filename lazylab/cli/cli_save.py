import argparse
from lazylab.tasker.tasker import Tasker
import logging
from lazylab.cli.cli_constants import *


def main():
    # Reading arguments
    parser = argparse.ArgumentParser(description='lazylab command which save reqested lab')
    parser.add_argument('lab_name', type=str, help='lab name')
    parser.add_argument('new_lab_name', type=str, help='new lab name')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    
    # Getting lab_name
    lab_name = args.lab_name
    new_lab_name = args.new_lab_name
    
    # Create a custom logger
    logger = logging.getLogger("lazylab")
    #Set level
    logger.setLevel(LOGGING_LEVEL[args.verbose])
    # Create logger handler
    logger_handler = logging.StreamHandler()
    # set format
    output_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(output_format)
    # set logger handler
    logger.addHandler(logger_handler)
    
    # Creating tasker object and reqesting deploy
    task = Tasker()
    logger.debug('Saving lab')
    task.save_lab(lab_name, new_lab_name)


if __name__ == "__main__":
    main()
