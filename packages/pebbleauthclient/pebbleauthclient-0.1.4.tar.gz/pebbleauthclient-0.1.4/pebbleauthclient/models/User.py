from typing import Sequence
from pebbleauthclient.datatypes import UserObject


class User(UserObject):
    """
    This object represent an authenticated user.

    :param user: UserObject
    """
    def __init__(self, user: UserObject):

        self.username: str = user.username
        """User name (should be an email)"""

        self.display_name: str = user.display_name
        """Name to be displayed (free 255 chars). Nullable"""

        self.level: int = user.level
        """User level from 1 to 6"""

        self.roles: Sequence[str] = user.roles
        """Roles granted to the user"""

    def has_role(self, role: str) -> bool:
        """
        Check if the user has the argument specified role.

        :param role: str
        :return: bool
        """
        if self.roles:
            return role in self.roles
        return False
