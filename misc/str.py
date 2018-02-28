import logging

from IPy import IP

import misc

log = logging.getLogger(__name__)


def decode_utf8(data):
    try:
        return data.decode('utf-8').strip()
    except Exception:
        pass
    return None


def extract_json(data):
    try:
        decoded_str = decode_utf8(data)
        json_str = find_between(decoded_str, "{", "}")
        return json_str if json_str else None
    except Exception:
        pass
    return None


# Reference: https://stackoverflow.com/a/3368991
def find_between(s, first, last, strip=False):
    try:
        start = s.index(first) + len(first)
        end = s.rindex(last, start)
        return s[start - 1 if not strip else start:end + 1 if not strip else end]
    except ValueError:
        return None


def validate_ip(ip):
    try:
        if IP(ip.strip()):
            return True
    except Exception:
        pass
    return False


def split_ip_port(addr):
    ip = ""
    port = misc.config.base_config['node']['port']

    if ":" in addr:
        ip, port = addr.split(":")
    else:
        ip = addr
    return ip, int(port)
