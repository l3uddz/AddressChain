#!/usr/bin/env python3
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import click
import urllib3

import misc
from node import Node

############################################################
# INIT
############################################################

# Logging
log_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)-10s - %(name)-35s - %(funcName)-30s - %(message)s')
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Set misc loggers to ERROR
logging.getLogger('urllib3').setLevel(logging.ERROR)
urllib3.disable_warnings()

# Set console logger
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

# Set file logger
file_handler = RotatingFileHandler(
    os.path.join(os.path.dirname(sys.argv[0]), 'activity.log'),
    maxBytes=1024 * 1024 * 5,
    backupCount=5
)
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# Set default logging level
root_logger.setLevel(logging.DEBUG)
log = root_logger.getChild('address_chain')

# config
cfg = misc.config.load_config()
if not cfg:
    sys.exit("Failed to load config...")


############################################################
# OPTIONS
############################################################

@click.group()
@click.option('--debug/--no-debug', default=True)
def cli(debug):
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    log.info('Debug mode is %s' % ('ON' if debug else 'OFF'))


############################################################
# COMMANDS
############################################################

@cli.command()
def node():
    """
    Start the AddressChain node
    :return:
    """
    log.info("Starting node...")


@cli.command()
def client():
    """
    Start the AddressChain client
    :return:
    """
    log.info("Starting client...")


############################################################
# MAIN
############################################################

if __name__ == "__main__":
    # chain = Blockchain()
    # addresses = {
    #     'BTC': {
    #         'Savings': '12345',
    #         'Checking': '1234567'
    #     },
    #     'ETH': ['12345', '123456', '1234567']
    # }
    # block = Block('james', cfg.key.pub, misc.crypt.ecdsa_sign(cfg.key.priv, addresses), addresses, None)
    # log.info("Block: %r", block)
    # chain.add_block(block)
    # log.info("Blockchain Height: %d", len(chain))
    #
    # block2 = Block('l3uddz', cfg.key.pub, misc.crypt.ecdsa_sign(cfg.key.priv, addresses), addresses, 'james')
    # log.info("Block: %r", block2)
    # chain.add_block(block2)
    # log.info("Blockchain Height: %d", len(chain))

    node = Node()
    node.start_node()

    exit(0)
    cli()
