from pebbleauthclient.models.User import User
from pebbleauthclient.datatypes import AuthenticatedLicenceObject


class AuthenticatedLicence(AuthenticatedLicenceObject):

    """
    This object represent information stored in a licence owned by a user.

    :param token_object: AuthenticatedLicenceObject
    """

    def __init__(self, token_object: AuthenticatedLicenceObject):
        self.app: str = token_object.app
        self.id: str = token_object.id
        self.tenant_id: str = token_object.tenant_id
        self.user: User = token_object.user

    def get_user(self) -> User:
        """
        Return the user who own the licence

        :return: User
        """
        return self.user
