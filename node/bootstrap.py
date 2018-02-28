import logging

import misc

log = logging.getLogger(__name__)
cfg = misc.config.load_config()


def get_ips():
    found_ips = []

    for host in cfg.node.bootstrap:
        ip, port = misc.str.split_ip_port(host)
        if misc.str.validate_ip(ip):
            # supplied host was an IP, add this to bootstrap ip list
            log.debug("Bootstrap from: %s", host)
            found_ips.append(host)
            continue
        else:
            # resolve host and add ip's
            log.debug("Resolving bootstrap ip(s) from %s", host)
            host_ips = misc.net.get_host_ips(host)
            if not host_ips or not len(host_ips):
                log.error("Unable to resolve bootstrap ip(s) from %s", host)
                continue
            else:
                log.debug("Bootstrap from: %s", host_ips)
                found_ips.extend(host_ips)
    return found_ips
