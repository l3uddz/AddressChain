# blockchain errors


# block
class BlockIsInvalid(Exception):
    """ Block was not valid """
    pass


class BlockHasNoUser(Exception):
    """ There was no user key in this block """
    pass


class BlockHasExistingUser(Exception):
    """ Block referenced a user that already exists """
    pass


class BlockHasNoAddresses(Exception):
    """ There was no addresses key in this block """
    pass


class BlockHasNoKey(Exception):
    """ There was no pub_key key in this block """
    pass


class BlockHasNoProof(Exception):
    """ There was no proof key in this block """
    pass


class BlockHasInvalidProof(Exception):
    """ The proof supplied in this block could not be verified """
    pass


class BlockHasNoPrev(Exception):
    """ There was no prev key in this block """
    pass


class BlockHasInvalidPrev(Exception):
    """ Block referenced an invalid prev block """
    pass
