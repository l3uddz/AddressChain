import json
import logging

from attrdict import AttrDict
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import Protocol, connectionDone

import misc
from proto import PacketTypes, PacketResponse, PacketRequest, NodeStates, PeerTypes

log = logging.getLogger(__name__)


class NodeProtocol(Protocol):
    def __init__(self, factory, peer_type=PeerTypes.CONNECTION_FROM):
        self.factory = factory
        self.node_id = self.factory.node_id
        self.remote_node_id = None
        self.state = NodeStates.HELLO
        self.peer_type = peer_type
        self.remote_addr = ""
        self.remote_peer_addr = ""

    # protocol events
    def connectionMade(self):
        remote_addr = self.transport.getPeer()
        self.remote_addr = "%s:%d" % (remote_addr.host, remote_addr.port)
        log.info("Connected to %s", self.transport.getPeer())

    def connectionLost(self, reason=connectionDone):
        # remove remote_node_id from peer list
        if self.remote_node_id in self.factory.peers:
            self.factory.peers.pop(self.remote_node_id)

        log.info("Connection lost to %s", self.transport.getPeer())

    def dataReceived(self, data):
        try:
            # loop lines and pass lines to appropriate handler
            for line in data.splitlines():
                # parse line and ignore unknown packet types
                decoded_line = misc.str.extract_json(line)
                if not decoded_line or not decoded_line.startswith("{"):
                    log.info("Received unknown packet type from %s, ignoring...", self.transport.getPeer())
                    continue

                # process message
                res = self._deferred(self._process_message, decoded_line)
                if not res.result:
                    continue

                # return response
                log.info("Sending response: %s", res.result)
                return self._send_packet(res.result)

        except Exception:
            log.exception("Exception parsing data from %s: ", self.transport.getPeer())
        return

    # sends
    def send_hello(self):
        packet = PacketRequest({"node_id": self.node_id, 'addr': self.factory.public_addr}, PacketTypes.NETWORK_HELLO)
        self._send_packet(packet)
        self.state = NodeStates.READY
        return

    def send_get_peers(self):
        packet = PacketRequest(None, PacketTypes.PEERS_GET)
        return self._send_packet(packet)

    # handlers
    async def handle_hello(self, packet):
        log.debug("Processing %s packet: %r", PacketTypes.NETWORK_HELLO, packet)
        if not packet.data.node_id:
            return PacketResponse(None, 'INVALID_NODEID')
        elif packet.data.node_id == self.node_id:
            log.debug("Connected to myself, disconnecting...")
            self.transport.loseConnection()
        else:
            self.remote_node_id = packet.data.node_id
            self.remote_peer_addr = packet.data.addr
            self.factory.peers[self.remote_node_id] = self
            log.info("Added %s to connected peers list", self.remote_node_id)
            # say hello back if we are in HELLO state
            if self.state == NodeStates.HELLO:
                self.send_hello()
            # ask for their peers
            self.send_get_peers()

        return None

    async def handle_get_peers(self, packet):
        log.debug("Processing %s packet: %r", PacketTypes.PEERS_GET, packet)
        peers = {}
        for peer_node_id, peer in self.factory.peers.items():
            if peer.peer_type == PeerTypes.CONNECTION_FROM and not self.remote_peer_addr:
                continue
            if peer.peer_type == PeerTypes.CONNECTED_TO:
                peers[peer.remote_node_id] = peer.remote_addr
            else:
                peers[peer.remote_node_id] = peer.remote_peer_addr
        return self._send_packet(PacketRequest({'peers': peers}, PacketTypes.PEERS_ADD))

    async def handle_add_peers(self, packet):
        log.debug("Processing %s packet: %r", PacketTypes.PEERS_ADD, packet)
        if not len(packet.data.peers):
            log.debug("Discovered no new peers from %s", self.transport.getPeer())
            return

        # loop returned peers
        new_peers = 0
        for peer_node_id, peer_addr in packet.data.peers.items():
            if peer_node_id == self.node_id:
                # skip this peer as it is ourselves
                continue
            elif peer_node_id in self.factory.peers:
                # skip peers already connected too
                continue
            # connect to peer
            self._connect_to_peer(peer_addr)
            new_peers += 1

        if new_peers:
            log.info("Discovered %d new peers from %s", new_peers, self.transport.getPeer())
        return

    # internals
    def _deferred(self, func, *args):
        call = func(*args)
        return defer.ensureDeferred(call).addErrback(self._process_message_error)

    def _send_packet(self, packet):
        return self.transport.write("{}\n".format(packet).encode())

    def _connect_to_peer(self, addr):
        ip, port = misc.str.split_ip_port(addr)
        log.info("Connecting to discovered peer at: %s:%d", ip, port)
        point = TCP4ClientEndpoint(reactor, ip, port)
        d = connectProtocol(point, NodeProtocol(self.factory, PeerTypes.CONNECTED_TO))
        d.addCallback(self.factory.peer_handshake)

    @staticmethod
    def _process_message_error(error):
        log.error("Error processing message:\n%s", error)
        return None

    async def _process_message(self, msg):
        packet = AttrDict(json.loads(msg))
        if not packet:
            log.info("Received unknown packet type from %s, ignoring...", self.transport.getPeer())
            return None

        log.info("Received %s packet from %s", packet.type, self.transport.getPeer())

        # pass packet to appropriate handler
        if packet.type == PacketTypes.NETWORK_HELLO:
            return await self.handle_hello(packet)
        elif packet.type == PacketTypes.PEERS_GET:
            return await self.handle_get_peers(packet)
        elif packet.type == PacketTypes.PEERS_ADD:
            return await self.handle_add_peers(packet)

        return "ERR"
