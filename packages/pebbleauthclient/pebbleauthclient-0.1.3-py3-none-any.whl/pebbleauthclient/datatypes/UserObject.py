from dataclasses import dataclass
from typing import Sequence


@dataclass
class UserObject:
    username: str
    """Unique username. Most of the time, it is a email address"""

    display_name: str
    """Name of the user used for display"""

    level: int
    """From 1-6 : user level"""

    roles: Sequence[str]
    """Roles affected to the user"""
