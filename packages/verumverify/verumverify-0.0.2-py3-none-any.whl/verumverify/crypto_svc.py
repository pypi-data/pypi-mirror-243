from base64 import b64decode

import requests
import rfc3161ng
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from pyasn1.codec.der import decoder, encoder

HASH_ALGORITHM = hashes.SHA256()


def load_pem_public_key_from_file(public_key_file: str):
    with open(public_key_file, "rb") as raw:
        return load_pem_public_key_from_bytes(raw.read())


def load_pem_public_key_from_bytes(raw: bytes):
    return serialization.load_pem_public_key(raw)


def verified(message, signature, public_key):
    try:
        public_key.verify(
            b64decode(signature),
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.AUTO
            ),
            hashes.SHA256())
        return True
    except InvalidSignature:
        return False


def verify_ts(tsr, data) -> bool:

    tsr, _ = decoder.decode(tsr, asn1Spec=rfc3161ng.TimeStampResp())

    try:
        response = requests.get(TS_CERT)
        if response.status_code == 200:
            freetsa_cert = response.content
        else:
            freetsa_cert = None
    except ConnectionError:
        freetsa_cert = None

    tst = encoder.encode(tsr.time_stamp_token)
    rt = rfc3161ng.RemoteTimestamper(
        TS_URL, certificate=freetsa_cert)
    return rt.check(tst, data)


def time_from_tsr(tsr):
    tsr, _ = decoder.decode(tsr, asn1Spec=rfc3161ng.TimeStampResp())
    return rfc3161ng.get_timestamp(encoder.encode(tsr.time_stamp_token))


TS_URL = "http://freetsa.org/tsr"
TS_CERT = "https://freetsa.org/files/tsa.crt"
CA_CERT = "https://freetsa.org/files/cacert.pem"
