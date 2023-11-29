import jwt
import json

from pebbleauthclient.errors import NotFoundJWKError, NoAlgorithmProvidedError, EmptyTokenError
from pebbleauthclient.key import get_jwk_set
from pebbleauthclient.models import PebbleAuthToken
from pebbleauthclient.token_data import get_token_data_from_jwt_payload


def auth(token: str) -> PebbleAuthToken:
    """
    Authenticate a provided token into and return a valid PebbleAuthToken object

    :param token: str
    :return: PebbleAuthToken
    """
    jwks = get_jwk_set()

    kid = jwt.get_unverified_header(token).get('kid')

    key = None
    jwk = None

    for j in jwks['keys']:
        if j['kid'] == kid:
            key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(j))
            jwk = j
            break

    if not key:
        raise NotFoundJWKError(kid)

    if "alg" not in jwk:
        raise NoAlgorithmProvidedError(kid)

    data = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[jwk['alg']],
        options={
            "verify_aud": False,
            "verify_iss": False
        }
    )

    token_data = get_token_data_from_jwt_payload(data, token)

    return PebbleAuthToken(token_data)


def auth_from_http_headers(headers: dict) -> PebbleAuthToken:
    """
    Authenticate user using the HTTP Authorization header provided with the request

    The Authorization headers must be written according to the standard :

    - Authorization name with capitalized A
    - Token content must start with "Bearer " string (ex : *Bearer full_token_string*)

    :param headers: All provided headers (including Authorization) in a dict
    :return: PebbleAuthToken
    """

    if headers['Authorization']:
        token = headers['Authorization'].replace('Bearer ', "")
        return auth(token)

    raise EmptyTokenError()
