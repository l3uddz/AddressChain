import logging

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Factory

import misc
from node import bootstrap
from node.protocol import NodeProtocol, PeerTypes

log = logging.getLogger(__name__)


class NodeFactory(Factory):
    def __init__(self, config, public_ip):
        self.cfg = config
        self.peers = {}
        self.node_id = self.cfg.key.pub
        self.public_addr = "%s:%d" % (public_ip, self.cfg.node.port) if public_ip else None

    def startFactory(self):
        self.start_bootstrap()

    def buildProtocol(self, addr):
        return NodeProtocol(self)

    def start_bootstrap(self):
        bootstrap_ips = bootstrap.get_ips()
        for addr in bootstrap_ips:
            ip, port = misc.str.split_ip_port(addr)
            log.info("Connecting to bootstrap peer at: %s:%d", ip, port)
            point = TCP4ClientEndpoint(reactor, ip, port)
            d = connectProtocol(point, NodeProtocol(self, PeerTypes.CONNECTED_TO))
            d.addCallback(self.peer_handshake)

    def peer_handshake(self, p):
        p.send_hello()
