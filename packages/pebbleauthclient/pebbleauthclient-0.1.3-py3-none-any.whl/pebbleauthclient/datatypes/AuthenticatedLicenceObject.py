from dataclasses import dataclass


@dataclass
class AuthenticatedLicenceObject:
    app: str
    """Application for which the licence is generated"""

    id: str
    """Licence ID as registered in the Licence server"""

    tenant_id: str
    """Customer id, client id... that will consume resources"""

    user: any
    """Instance of User class who own the licence"""
