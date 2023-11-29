"""scpup package contains the classes, constants, types, etc., needed in the
game SCPUP (Super Crystal Pokebros Ultimate Party) and any other AramEau games.
"""

from .bases import *  # noqa
from .common import *  # noqa
from .utils import *  # noqa
from ._internal.services import EauService  # noqa
from .game import Game  # noqa

__name__ = "scpup"
__package__ = "scpup"
