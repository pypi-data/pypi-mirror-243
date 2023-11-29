from dataclasses import dataclass
from typing import Sequence


@dataclass
class PebbleTokenData:
    aud: str
    """Application for which the token is generated"""

    exp: int
    """Expiration timestamp"""

    iat: int
    """Issued at time (timestamp)"""

    iss: str
    """Issuer : Licence ID that emit the token"""

    lv: int
    """From 1-6 : user level affected by the licence"""

    name: str
    """Display name for the user"""

    roles: Sequence[str]
    """Roles attributed to the user"""

    sub: str
    """User email (used as username)"""

    tid: str
    """Tenant ID : customer id, client id... that will consume resources"""

    token: str
    """Token from which datas has been deserialized"""
