import logging

import dns.resolver
import requests

import misc

log = logging.getLogger(__name__)


def get_host_ips(host):
    ips = []
    try:
        results = dns.resolver.query(host, 'A')
        for ip in results:
            if ip.to_text() not in ips:
                ips.append(ip.to_text())
    except Exception:
        log.exception("Failed resolving host %s: ", host)
    return ips


def get_public_ip():
    try:
        res = requests.get('https://canihazip.com/s', verify=False)
        if res.status_code == 200 and misc.str.validate_ip(res.text):
            return res.text.strip()
    except Exception:
        log.exception("Exception retrieving public ip: ")
    return None


def upnp_forward_port(port, name=None):
    try:
        pass
    except Exception:
        log.exception("Exception opening port %d via upnp: ", port)
    return None
