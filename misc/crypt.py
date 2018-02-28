import hashlib
import json
import logging

import ecdsa

log = logging.getLogger(__name__)


def sha256_hash(data):
    """ Take some data and return sha256 hash """
    try:
        if isinstance(data, str):
            return hashlib.sha256(data.encode()).hexdigest()
        elif isinstance(data, dict) or isinstance(data, list):
            return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        elif isinstance(data, int):
            return hashlib.sha256(str(data).encode()).hexdigest()
        elif isinstance(data, bytes):
            return hashlib.sha256(data).hexdigest()
        else:
            log.error("Unable to sha256_hash unexpected type %s: %r", type(data).__name__, data)
            return None
    except Exception:
        log.exception("Exception while hashing %r: ", data)
    return None


def ecdsa_generate():
    """ Generate ECDSA keypair """
    try:
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        return private_key.to_string().hex(), public_key.to_string().hex()
    except Exception:
        log.exception("Exception generating priv/pub keypair: ")
    return None, None


def ecdsa_sign(priv_key, data):
    """ Sign data with ECDSA priv_key """
    try:
        data_to_sign = None
        if isinstance(data, str):
            data_to_sign = data
        elif isinstance(data, dict) or isinstance(data, list):
            data_to_sign = json.dumps(data, sort_keys=True, separators=(',', ':'))
        elif isinstance(data, int):
            data_to_sign = str(data)
        elif isinstance(data, bytes):
            data_to_sign = str(data)

        sk = ecdsa.SigningKey.from_string(bytearray.fromhex(priv_key), curve=ecdsa.SECP256k1)
        return sk.sign(data_to_sign.encode('utf-8')).hex()
    except Exception:
        log.exception("Exception signing %r with priv_key %r: ", data, priv_key)
    return None


def ecdsa_verify(pub_key, data, signature):
    """ Validate signature was from pub_keys corresponding priv_key """
    try:
        data_to_sign = None
        if isinstance(data, str):
            data_to_sign = data
        elif isinstance(data, dict) or isinstance(data, list):
            data_to_sign = json.dumps(data, sort_keys=True, separators=(',', ':'))
        elif isinstance(data, int):
            data_to_sign = str(data)
        elif isinstance(data, bytes):
            data_to_sign = str(data)

        vk = ecdsa.VerifyingKey.from_string(bytearray.fromhex(pub_key), curve=ecdsa.SECP256k1)
        return vk.verify(bytearray.fromhex(signature), data_to_sign.encode('utf-8'))
    except ecdsa.BadSignatureError:
        return False
    except Exception:
        log.exception("Exception while verifying signature %r for pub_key %r against data %r: ", signature, pub_key,
                      data)
    return False
