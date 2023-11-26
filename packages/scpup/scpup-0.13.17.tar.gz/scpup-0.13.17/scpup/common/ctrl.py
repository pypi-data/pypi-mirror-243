"""This module contains the helper classes for game controllers.

This module has the button and stick mappings of the following controllers:

* PS4
  * PS4 Controller
  * DualSense Wireless Controller
* PS5
  * Sony Interactive Entertainment Wireless Controller
* Xbox
  * Xbox Series X Controller
  * Xbox One Series X Controller

The mapping classes also are used to get information of each stick and trigger
"""

from __future__ import annotations
import pygame
import pygame.joystick
import scpup
from abc import abstractmethod, ABCMeta
from typing import overload, final

__all__: list[str] = [
  "EauCtrl",
  "EauCtrlMapping",
  "EauXboxCtrlMapping",
  "EauPS4CtrlMapping",
  "EauPS5CtrlMapping",
]


class EauCtrlMappingMeta(ABCMeta):
  """Metaclass of the EauCtrlMapping class. This class implements a Singleton"""
  _instances_: dict = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances_:
      instance = super().__call__(*args, **kwargs)
      cls._instances_[cls] = instance
    return cls._instances_[cls]


class EauCtrlMapping(metaclass=EauCtrlMappingMeta):
  """A mapping between the buttons of a controller to the button id of a
  pygame.event.Event. This class implements the Singleton pattern."""
  __slots__: tuple = ()

  @staticmethod
  def get(name: str) -> EauXboxCtrlMapping | EauPS4CtrlMapping | EauPS5CtrlMapping:
    """Get the mapping instance of a certain controller given the name of that
    controller.

    Args:
      name:
        The name of the controller as described in the pygame.joystick
        documentation.

    Raises:
      ValueError:
        The name is not a valid controller name or it has not been mapped yet.

    Returns: The instance of the corresponding controller mapping.
    """
    if name in ["Xbox Series X Controller", "Xbox One Series X Controller"]:
      return EauXboxCtrlMapping()
    elif name in ["PS4 Controller", "DualSense Wireless Controller"]:
      return EauPS4CtrlMapping()
    elif name in ["Sony Interactive Entertainment Wireless Controller"]:
      return EauPS5CtrlMapping()
    raise ValueError(f"Controller not defined: '{name}'")

  @abstractmethod
  def __getitem__(self, key: int) -> scpup.EauAction:
    """Gets a scpup.EauAction given a key (which would be the button id of a
    pygame.event.Event).

    Args:
      key:
        The button that is received from a pygame.event.Event instance when a
        JOYBUTTONUP or JOYBUTTONDOWN event is received.

    Returns:
      EauAction: The button that the received key maps to.

    Raises:
      KeyError: The key is a integer but does not correspond to a button.
      TypeError:
        It could be that the key is not an integer or any other unexpected
        error.
    """

  @overload
  @abstractmethod
  def axis(self, axis: scpup.EauAxis) -> int:
    """Get the axis number given an EauAxis identifier

    Args:
      axis: The EauAxis identifier of the axis

    Returns:
      int: The axis number
    """
  @overload
  @abstractmethod
  def axis(self, axis: int) -> scpup.EauAxis:
    """Get the EauAxis identifier given an axis number

    Args:
      axis: The axis number

    Returns:
      EauAxis:The EauAxis identifier corresponding to the axis number received
    """
  @abstractmethod
  def axis(self, axis: scpup.EauAxis | int) -> int | scpup.EauAxis:
    ...


@final
class EauXboxCtrlMapping(EauCtrlMapping):
  __slots__: tuple = ()

  def __getitem__(self, key: int) -> scpup.EauAction:
    if key < 0 or key > 10:
      raise KeyError(f'No mapping for button {key}')
    elif key == 0:
      return scpup.EauAction.A
    elif key == 1:
      return scpup.EauAction.B
    elif key == 2:
      return scpup.EauAction.X
    elif key == 3:
      return scpup.EauAction.Y
    elif key == 4:
      return scpup.EauAction.LB
    elif key == 5:
      return scpup.EauAction.RB
    elif key == 6:
      return scpup.EauAction.SELECT
    elif key == 7:
      return scpup.EauAction.START
    elif key == 8:
      return scpup.EauAction.LS
    elif key == 9:
      return scpup.EauAction.RS
    elif key == 10:
      return scpup.EauAction.GUIDE
    raise TypeError('Unexpected Error')

  @overload
  def axis(self, axis: scpup.EauAxis) -> int: ...

  @overload
  def axis(self, axis: int) -> scpup.EauAxis: ...

  def axis(self, axis: scpup.EauAxis | int) -> int | scpup.EauAxis:
    if isinstance(axis, scpup.EauAxis):
      if axis == scpup.EauAxis.LS_X:
        return 0
      elif axis == scpup.EauAxis.LS_Y:
        return 1
      elif axis == scpup.EauAxis.RS_X:
        return 3
      elif axis == scpup.EauAxis.RS_Y:
        return 4
      elif axis == scpup.EauAxis.LT:
        return 2
      elif axis == scpup.EauAxis.RT:
        return 5
      raise TypeError(f"Unknown axis number: '{axis}'")
    else:
      if axis == 0:
        return scpup.EauAxis.LS_X
      elif axis == 1:
        return scpup.EauAxis.LS_Y
      elif axis == 3:
        return scpup.EauAxis.RS_X
      elif axis == 4:
        return scpup.EauAxis.RS_Y
      elif axis == 2:
        return scpup.EauAxis.LT
      elif axis == 5:
        return scpup.EauAxis.RT
      raise TypeError(f"Unknown axis identifier: '{axis}'")


@final
class EauPS4CtrlMapping(EauCtrlMapping):
  __slots__: tuple = ()

  def __getitem__(self, key: int) -> scpup.EauAction:
    if key < 0 or key > 14:
      raise KeyError(f'No mapping for button {key}')
    elif key == 0:
      return scpup.EauAction.A
    elif key == 1:
      return scpup.EauAction.B
    elif key == 2:
      return scpup.EauAction.X
    elif key == 3:
      return scpup.EauAction.Y
    elif key == 4:
      return scpup.EauAction.SELECT
    elif key == 5:
      return scpup.EauAction.GUIDE
    elif key == 6:
      return scpup.EauAction.START
    elif key == 7:
      return scpup.EauAction.LS
    elif key == 8:
      return scpup.EauAction.RS
    elif key == 9:
      return scpup.EauAction.LB
    elif key == 10:
      return scpup.EauAction.RB
    elif key == 11:
      return scpup.EauAction.DPAD_UP
    elif key == 12:
      return scpup.EauAction.DPAD_DOWN
    elif key == 13:
      return scpup.EauAction.DPAD_LEFT
    elif key == 14:
      return scpup.EauAction.DPAD_RIGHT
    raise TypeError('Unexpected Error')

  @overload
  def axis(self, axis: scpup.EauAxis) -> int: ...

  @overload
  def axis(self, axis: int) -> scpup.EauAxis: ...

  def axis(self, axis: scpup.EauAxis | int) -> int | scpup.EauAxis:
    if isinstance(axis, scpup.EauAxis):
      if axis == scpup.EauAxis.LS_X:
        return 0
      elif axis == scpup.EauAxis.LS_Y:
        return 1
      elif axis == scpup.EauAxis.RS_X:
        return 2
      elif axis == scpup.EauAxis.RS_Y:
        return 3
      elif axis == scpup.EauAxis.LT:
        return 4
      elif axis == scpup.EauAxis.RT:
        return 5
      raise TypeError(f"Unknown axis number: '{axis}'")
    else:
      if axis == 0:
        return scpup.EauAxis.LS_X
      elif axis == 1:
        return scpup.EauAxis.LS_Y
      elif axis == 2:
        return scpup.EauAxis.RS_X
      elif axis == 3:
        return scpup.EauAxis.RS_Y
      elif axis == 4:
        return scpup.EauAxis.LT
      elif axis == 5:
        return scpup.EauAxis.RT
      raise TypeError(f"Unknown axis identifier: '{axis}'")


@final
class EauPS5CtrlMapping(EauCtrlMapping):
  __slots__: tuple = ()

  def __getitem__(self, key: int) -> scpup.EauAction:
    if key < 0 or key > 12:
      raise KeyError(f'No mapping for button {key}')
    elif key == 0:
      return scpup.EauAction.A
    elif key == 1:
      return scpup.EauAction.B
    elif key == 2:
      return scpup.EauAction.X
    elif key == 3:
      return scpup.EauAction.Y
    elif key == 4:
      return scpup.EauAction.LB
    elif key == 5:
      return scpup.EauAction.RB
    # elif key == 6:
    #   return scpup.EauAction.LT
    # elif key == 7:
    #   return scpup.EauAction.RT
    elif key == 8:
      return scpup.EauAction.SELECT
    elif key == 9:
      return scpup.EauAction.START
    elif key == 10:
      return scpup.EauAction.GUIDE
    elif key == 11:
      return scpup.EauAction.LS
    elif key == 12:
      return scpup.EauAction.RS
    raise TypeError('Unexpected Error')

  @overload
  def axis(self, axis: scpup.EauAxis) -> int: ...

  @overload
  def axis(self, axis: int) -> scpup.EauAxis: ...

  def axis(self, axis: scpup.EauAxis | int) -> int | scpup.EauAxis:  # type: ignore
    if isinstance(axis, scpup.EauAxis):
      if axis == scpup.EauAxis.LS_X:
        return 0
      elif axis == scpup.EauAxis.LS_Y:
        return 1
      elif axis == scpup.EauAxis.RS_X:
        return 3
      elif axis == scpup.EauAxis.RS_Y:
        return 4
      elif axis == scpup.EauAxis.LT:
        return 2
      elif axis == scpup.EauAxis.RT:
        return 5
      raise TypeError(f"Unknown axis number: '{axis}'")
    else:
      if axis == 0:
        return scpup.EauAxis.LS_X
      elif axis == 1:
        return scpup.EauAxis.LS_Y
      elif axis == 3:
        return scpup.EauAxis.RS_X
      elif axis == 4:
        return scpup.EauAxis.RS_Y
      elif axis == 2:
        return scpup.EauAxis.LT
      elif axis == 5:
        return scpup.EauAxis.RT
      raise TypeError(f"Unknown axis identifier: '{axis}'")


class EauCtrlMeta(type):
  """Metaclass of the EauCtrl class. This class implements a Singleton, but
  instead of storing only 1 instance of the EauCtrl class, it holds an instance
  for every pygame.joystick.Joystick instance"""
  _instances: dict[int, EauCtrl] = {}

  def __call__(cls, val: pygame.joystick.JoystickType | int) -> EauCtrl:
    """Create a new instance or retrieve an instance of the EauCtrl class"""
    if isinstance(val, int):
      return next(ctrl for iid, ctrl in cls._instances.items() if iid == val)
    iid = val.get_instance_id()
    if iid not in cls._instances:
      instance = super().__call__(val)
      cls._instances[iid] = instance
    return cls._instances[iid]

  def remove_ctrl(cls, iid: int) -> None:
    """Remove a controller from the saved instances, given an instance id.

    Args:
      iid: The instance id of the joystick to look for.
    """
    if iid in cls._instances:
      del cls._instances[iid]

  def create(cls, joystick: pygame.joystick.JoystickType) -> None:
    """Create a new controller with the given joystick

    Args:
      joystick: The joystick to be assigned to the new controller.
    """
    cls.__call__(joystick)


@final
class EauCtrl(metaclass=EauCtrlMeta):
  """A wrapper around a pygame.joystick object that also has its mapping.

  Attributes:
    joystick: The wrapped pygame.joystick object.
    _mapping: The corresponding EauCtrlMapping object.
    threshold: Class attribute that is used for the sticks dead zone adjustment.
  """
  threshold = 0.3

  __slots__: tuple = (
    "joystick",
    "_mapping",
  )

  @overload
  def __init__(self, iid: int):
    """Get an EauCtrl instance given an instance id.

    Args:
      iid: The instance id of the joystick wrapped by the EauCtrl.
    """
  @overload
  def __init__(self, joystick: pygame.joystick.JoystickType):
    """Initializes a controller wrapper for a given joystick.

    This class implements a Singleton which uses the joystick instance ids as
    keys to store EauCtrl instances, so if the instance id of the joystick
    provided is already stored then that EauCtrl will be retrieved instead of
    creating a new one.

    Args:
      joystick: The pygame.joystick that will be wrapped.
    """

  def __init__(self, joystick: pygame.joystick.JoystickType) -> None:  # type: ignore
    self._mapping: EauXboxCtrlMapping | EauPS4CtrlMapping | EauPS5CtrlMapping = EauCtrlMapping.get(joystick.get_name())
    self.joystick: pygame.joystick.JoystickType = joystick

  @property
  def iid(self) -> int:
    """Gets the instance id of the wrapped joystick."""
    return self.joystick.get_instance_id()

  @property
  def LS(self) -> tuple[float, float]:
    """Get the current state of the left stick

    Returns:
      tuple[float, float]:
        Horizontal and vertical state of the left stick. Values go from -1 to 1
    """
    return (
      self.joystick.get_axis(self._mapping.axis(scpup.EauAxis.LS_X)),
      self.joystick.get_axis(self._mapping.axis(scpup.EauAxis.LS_Y))
    )

  @property
  def RS(self) -> tuple[float, float]:
    """Get the current state of the right stick

    Returns:
      tuple[float, float]:
        Horizontal and vertical state of the right stick. Values go from -1 to 1
    """
    return (
      self.joystick.get_axis(self._mapping.axis(scpup.EauAxis.RS_X)),
      self.joystick.get_axis(self._mapping.axis(scpup.EauAxis.RS_Y))
    )

  @property
  def triggers(self) -> tuple[float, float]:
    """Get the current state of the triggers

    Returns:
      tuple[float, float]:
        Left trigger and right trigger states. Values go from 0 to 1 (Not sure)
    """
    return (
      self.joystick.get_axis(self._mapping.axis(scpup.EauAxis.LT)),
      self.joystick.get_axis(self._mapping.axis(scpup.EauAxis.RT))
    )

  @overload
  def action(self, button_num: int) -> scpup.EauAction:
    """Get an action given a button number

    Args:
      button_num: The button number

    Returns:
      scpup.EauAction: The action that the button matches to.
    """
  @overload
  def action(self, axis_num: int, value: float) -> scpup.EauAction:
    """Get an action given an axis number and its value

    Args:
      axis_num: The axis number
      value: The movement of the axis

    Returns:
      scpup.EauAction:
        The action that the axis matches to. The value is used to determinate
        the direction of the movement.
    """
  def action(self, num: int, value: float | None = None) -> scpup.EauAction | None:  # type: ignore
    if value is not None:
      if -self.threshold < value < self.threshold:
        return None
      axis = self._mapping.axis(num)
      if axis == scpup.EauAxis.LS_X:
        return scpup.EauAction.LS_LEFT if value < -self.threshold else scpup.EauAction.LS_RIGHT
      elif axis == scpup.EauAxis.LS_Y:
        return scpup.EauAction.LS_UP if value < -self.threshold else scpup.EauAction.LS_DOWN
      elif axis == scpup.EauAxis.RS_X:
        return scpup.EauAction.RS_LEFT if value < -self.threshold else scpup.EauAction.RS_RIGHT
      elif axis == scpup.EauAxis.RS_Y:
        return scpup.EauAction.RS_UP if value < -self.threshold else scpup.EauAction.RS_DOWN
      elif axis == scpup.EauAxis.LT:
        return scpup.EauAction.LT
      elif axis == scpup.EauAxis.RT:
        return scpup.EauAction.RT
    else:
      try:
        action = self._mapping[num]
        return action
      except (TypeError, KeyError):
        return None
