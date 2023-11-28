from abc import ABCMeta, abstractmethod
import scpup


__all__ = [
  "EauButton",
  "EauBackButton"
]


class EauButton(scpup.EauAnimatedSprite, metaclass=ABCMeta):
  """A button for user interfaces like menus.

  Inherits from EauAnimatedSprite but this is an abstract class. You have to
  implement 'action' method in its subclasses.
  """
  __slots__ = ()

  def __init__(self, image: str, position: scpup.EauPosition, pressed_image: str | None = None):
    """Initialize a UI button

    Args:
        image: The button's image path
        position: The position of the button. Defaults to None.
        pressed_image:
          The button's image path when its pressed. If omitted or None, this
          will be the same as the button's image but with '_pressed' added
          before the extension. Defaults to None.
    """
    pressed_image = pressed_image or f"{image[:image.rindex('.')]}_pressed.png"
    super().__init__(
      image,
      images={"click": pressed_image},
      secuences=[
        scpup.EauSecuence("click", scpup.EauSecuenceStep(0, 8), sound_path="menu_click.wav")
      ],
      position=position,
      subgroup="buttons"
    )

  @abstractmethod
  def action(self) -> None:
    """Method that will be run when this button is clicked"""


class EauBackButton(EauButton):
  def __init__(self, image: str, position: scpup.EauPosition, pressed_image: str | None = None):
    super().__init__(image, position, pressed_image)

  def action(self) -> None:
    to_view = scpup.EauService._view_stack[-2]
    scpup.EauService.get('EauEventService').post(scpup.EauEventSubtype.NAV, to_view=to_view)
