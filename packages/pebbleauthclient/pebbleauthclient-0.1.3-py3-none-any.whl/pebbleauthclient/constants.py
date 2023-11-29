import os

JWKS_REMOTE_URI: str = os.getenv('PBL_JWKS_REMOTE_URI')
"""
Return the location of remote pebble authenticator public keys set (JWKS) as defined in the sys global
environment variables
"""

CERTS_FOLDER: str = "./var/credentials/auth"
"""
Contains the local folder for temporary store authentication credentials. Storing locally the credentials improves
server response.
"""

JWKS_LOCAL_PATH: str = CERTS_FOLDER + "/jwks.json"
"""
Contains the local path for the public keys set (JWKS)
"""
