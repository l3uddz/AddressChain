import logging

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

import misc
from node import bootstrap, factory, protocol

log = logging.getLogger(__name__)


class Node:
    def __init__(self):
        self.cfg = misc.config.load_config()
        self.endpoint = TCP4ServerEndpoint(reactor, self.cfg.node.port)

    def start_node(self):
        # log.info("Forwarding port %d via UPnP", self.cfg.node.port)
        # misc.net.upnp_forward_port(self.cfg.node.port)
        log.info("Starting node on port %d", self.cfg.node.port)
        self.endpoint.listen(factory.NodeFactory(self.cfg, misc.net.get_public_ip()))
        reactor.run()

    def stop_node(self):
        pass
