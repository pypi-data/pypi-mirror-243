class EmptyJWKSRemoteURIError(Exception):
    """
    This error should be raised when ``PBL_JWKS_REMOTE_URI`` environment variable is empty or not set.
    If this error occurs, you should export ``PBL_JWKS_REMOTE_URI``

    .. code-block::
        :caption: Locally solution

        export PBL_JWKS_REMOTE_URI=https://SERVER_URI/path/jwks.json

    .. code-block::
        :caption: Dockerfile solution

        ENV PBL_JWKS_REMOTE_URI=https://SERVER_URI/path/jwks.json
    """
    def __init__(self):
        message = ("The public JWK Set URI is empty. It can be due to a misconfiguration on your server. Did you "
                   "export PBL_JWKS_REMOTE_URI environment variable on your system or on your .env file ?")
        print("ERROR: " + message)
        super().__init__(message)


class EmptyJWKSError(Exception):
    """
    This error should be raised when the JWK set is empty. jwks.json might be corrupted, empty or not exists.
    """
    def __init__(self):
        message = "Public keys set is empty. jwks.json file might be corrupted, empty or not exist."
        super().__init__(message)


class NotFoundJWKError(Exception):
    """
    This error should be raised when the JWK used to generate the token is not found in the JWK Set.

    :param kid: key id that cause the error
    """
    def __init__(self, kid: str):
        message = "JWK key was not found for this kid (" + kid + ")"
        super().__init__(message)


class NoAlgorithmProvidedError(Exception):
    """
    This error should be raised when the algorithm used to decode the JWT token is empty or badly provided.

    :param kid: key id that cause the error
    """
    def __init__(self, kid: str):
        message = "No algorithm is provided for this JWK (" + kid + ("). It might be cause by a badly encoded of the "
                                                                     "public Json Web Key (JWK).")
        super().__init__(message)


class EmptyTokenError(Exception):
    """
    This error should be raised when the token is not provided or empty.
    """
    def __init__(self):
        message = "Empty token."
        super().__init__(message)
