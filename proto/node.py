import json
import logging

log = logging.getLogger(__name__)


class PacketTypes:
    # network
    NETWORK_HELLO = "hello"

    # peers
    PEERS_ADD = "peers_add"
    PEERS_GET = "peers_get"

    # block (users)
    USER_GET = "user_get"
    USER_ADD = "user_add"


class NodeStates:
    HELLO = "HELLO"
    READY = "READY"


class PeerTypes:
    CONNECTED_TO = 1
    CONNECTION_FROM = 2


class PacketRequest:
    def __init__(self, data, type):
        self.data = data
        self.type = type

    # internals
    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            pass

        # Default behaviour
        return None


class PacketResponse:
    def __init__(self, data, error=None):
        self.data = data
        self.error = error

    # internals
    def __repr__(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            pass

        # Default behaviour
        return None
