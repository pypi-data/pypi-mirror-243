import os.path
import json

import urllib
import urllib.request

import pebbleauthclient.constants as constants
from pebbleauthclient.errors import EmptyJWKSRemoteURIError, EmptyJWKSError


def get_jwk_set() -> dict:
    """
    Return all the JWK currently stored in jwks.json file or in the process memory.

    :return: dict
    """
    if not os.getenv('PBL_AUTH_JWKS'):
        print("NOTICE: Store JWKS in process environment variable")
        os.environ['PBL_AUTH_JWKS'] = json.dumps(read_jwks())
    return json.loads(os.getenv('PBL_AUTH_JWKS'))


def import_remote_jwks(remote_location: str) -> None:
    """
    Import the public RSA key from a remote server to the local /var/credentials/auth/jwks.json file.

    :param remote_location: str
    :return: None
    """
    if not os.path.exists(constants.CERTS_FOLDER):
        os.makedirs(constants.CERTS_FOLDER)

    jwks = ""

    for line in urllib.request.urlopen(remote_location):
        jwks += line.decode('utf-8')

    f = open(constants.JWKS_LOCAL_PATH, "w")
    f.write(jwks)
    f.close()


def read_jwks() -> dict:
    """
    Read the public RSA key from /var/credentials/auth/jwks.json and convert it into JWK Set

    :return: dict
    """
    if not os.path.exists(constants.JWKS_LOCAL_PATH):
        if not constants.JWKS_REMOTE_URI:
            raise EmptyJWKSRemoteURIError()
        import_remote_jwks(constants.JWKS_REMOTE_URI)

    with open(constants.JWKS_LOCAL_PATH) as f:
        data = f.read()

    if not data:
        raise EmptyJWKSError()

    return json.loads(data)
