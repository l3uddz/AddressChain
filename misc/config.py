import json
import logging
import os
import sys

from attrdict import AttrDict

from misc import crypt

log = logging.getLogger(__name__)

config_path = os.path.join(os.path.dirname(sys.argv[0]), 'config.json')
base_config = {
    'key': {
        'pub': '',
        'priv': ''
    },
    'node': {
        'bootstrap': ['127.0.0.1'],
        'port': 5999
    },
    'user': ''
}


def build_config():
    """ Build default config along with new priv/pub keypair if config.json does not exist """
    if not os.path.exists(config_path):
        # generate key pair
        priv_key, pub_key = crypt.ecdsa_generate()
        if not priv_key or not pub_key:
            log.error("Unable to generate public/private keypair....")
            exit(0)
        else:
            # fill default config with generated keypair
            base_config['key']['pub'] = pub_key
            base_config['key']['priv'] = priv_key

        # dump default config
        log.info("Dumping initial config to: %s", config_path)
        with open(config_path, 'w') as fp:
            json.dump(base_config, fp, sort_keys=True, indent=2)
        return True
    else:
        return False


def load_config():
    """ Load config.json """
    try:
        with open(config_path, 'r') as fp:
            return AttrDict(json.load(fp))
    except Exception:
        log.exception("Exception loading config from %s", config_path)
    return None


# MAIN
if build_config():
    sys.exit("Please edit the default configuration before running again!")
