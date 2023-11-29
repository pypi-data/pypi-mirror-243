from __future__ import annotations
import pygame
from enum import Enum, auto, IntEnum


__all__: list[str] = [
  "EauEventSubtype",
  "EauColor",
  "EauDifficulty",
  "EauAxis",
  "EauAction",
  "EauLayoutType"
]


class EauLayoutType(Enum):
  """Enumeration of the different layout types"""
  Position = auto()
  Top = auto()
  Bottom = auto()
  Center = auto()
  Left = auto()
  Right = auto()


class EauAxis(Enum):
  """Enumeration that has all axis available. Left and Right sticks have a
  vertical and horizontal movement. The triggers are also considered axes."""
  LS_X = auto()
  LS_Y = auto()
  RS_X = auto()
  RS_Y = auto()
  LT = auto()
  RT = auto()

  def __str__(self) -> str:
    if self.name.startswith("LS"):
      mv = self.name[-1]
      return f"<Left stick {mv}>"
    elif self.name.startswith("RS"):
      mv = self.name[-1]
      return f"<Right stick {mv}>"
    else:
      side = "Left" if self.name[0] == "L" else "Right"
      return f"<{side} trigger>"

  def __repr__(self) -> str:
    return str(self)


class EauAction(IntEnum):
  """Enumeration that has all the mappeable buttons."""
  START = auto()
  SELECT = auto()
  GUIDE = auto()
  A = auto()
  B = auto()
  X = auto()
  Y = auto()
  LB = auto()
  RB = auto()
  LS = auto()
  RS = auto()
  RT = auto()
  LT = auto()
  DPAD_UP = auto()
  DPAD_RIGHT = auto()
  DPAD_DOWN = auto()
  DPAD_LEFT = auto()
  LS_LEFT = auto()
  LS_RIGHT = auto()
  LS_UP = auto()
  LS_DOWN = auto()
  RS_LEFT = auto()
  RS_RIGHT = auto()
  RS_UP = auto()
  RS_DOWN = auto()

  def __repr__(self) -> str:
    return str(self)

  def __str__(self) -> str:
    return f"<Action: {self.name}>"


class EauDifficulty(Enum):
  EASY = 1
  MEDIUM = 2
  HARD = 3


class EauEventSubtype(Enum):
  """A subtype of the EAU_EVENT events"""
  NAV = auto()
  QUIT = auto()
  VIEW = auto()


class EauColor(Enum):
  MINT = pygame.Color(14, 235, 139)
  ORANGE = pygame.Color(245, 155, 0)
  YELLOW = pygame.Color(240, 240, 0)
  GREEN = pygame.Color(26, 161, 62)
  PURPLE = pygame.Color(158, 66, 245)
  BLUE = pygame.Color(15, 127, 247)
  RED = pygame.Color(180, 24, 50)
  WHITE = pygame.Color(255, 255, 255)
  BLACK = pygame.Color(0, 0, 0)
  LIGHT_BLUE = pygame.Color(199, 249, 255)
  GRAY = pygame.Color(170, 170, 170)
  BACKGROUND = pygame.Color(230, 230, 230)
  BTN_SELECTED = pygame.Color(252, 226, 56)
  ERROR = pygame.Color(181, 5, 5)
  TRANSPARENT = pygame.Color(0, 0, 0, 0)
  PAUSE = pygame.Color(120, 120, 120)
  DARKEN = pygame.Color(0, 0, 0, 200)
  DARK_GRAY = pygame.Color(50, 50, 50)
  TEXT_BOX_BG = pygame.Color(200, 200, 200)
  TEXT_HIGHTLIGHT_BG = pygame.Color(248, 255, 0)
  VOLUME = pygame.Color(27, 135, 56)
  SEARCH_COLOR = pygame.Color(100, 100, 100)

  def apply(self, surf: pygame.surface.Surface, search_color: EauColor | None = None):
    pygame.transform.threshold(
      surf,
      surf,
      search_color=search_color.value if search_color else EauColor.SEARCH_COLOR.value,
      threshold=pygame.Color(5, 5, 5),
      set_color=self.value,
      set_behavior=1,
      inverse_set=True
    )
