import logging

import misc
from proto import errors

log = logging.getLogger(__name__)


class Blockchain:
    def __init__(self):
        self.chain = {}

    def validate_block(self, block):
        """ Validate the supplied block """
        # check block has user present / does not already exist
        if not block.user:
            raise errors.BlockHasNoUser
        elif block.user in self.chain and block.hash != self.chain[block.user].hash:
            raise errors.BlockHasExistingUser
        # check block has addresses present
        if not block.addresses:
            raise errors.BlockHasNoAddresses
        # check block has key present
        if not block.key:
            raise errors.BlockHasNoKey
        # check block has prev present and references a valid block
        if not block.prev and len(self.chain):
            raise errors.BlockHasNoPrev
        elif len(self.chain) and block.prev not in self.chain:
            raise errors.BlockHasInvalidPrev
        # check block has proof present
        if not block.proof:
            raise errors.BlockHasNoProof
        # validate supplied proof
        if not misc.crypt.ecdsa_verify(block.key, block.addresses, block.proof):
            raise errors.BlockHasInvalidProof
        return True

    def add_block(self, block):
        """ Add a new block to the chain """
        # validate block is valid
        if not self.validate_block(block):
            raise errors.BlockIsInvalid

        self.chain[block.user] = block

    # internals
    def __len__(self):
        return len(self.chain)
