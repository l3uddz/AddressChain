import json
import logging

import misc

log = logging.getLogger(__name__)


class Block:
    def __init__(self, user, key, proof, addresses, prev):
        self.user = user
        self.key = key
        self.proof = proof
        self.addresses = addresses
        self.hash = misc.crypt.sha256_hash(user)
        self.prev = prev

    # internals
    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            pass

        # Default behaviour
        return None
