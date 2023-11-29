from __future__ import annotations

from re import sub
import os
import pygame
import pygame.event
import pygame.mixer
import scpup
from json import loads, dumps
from typing import Any, Literal, final, overload
from scpup._internal import load_sound, load_image, load_music


__all__: list[str] = [
  "EauService",
  "EauDisplayService",
  "EauEventService",
  "EauAudioService",
  "EauGameService",
]


class EauServiceMeta(type):
  _instances_: dict[str, EauService] = {}

  def __call__(cls, *args, **kwds) -> Any:
    if cls.__name__ not in cls._instances_:
      instance = super().__call__(*args, **kwds)
      cls._instances_[cls.__name__] = instance
    return cls._instances_[cls.__name__]


class EauService(metaclass=EauServiceMeta):
  """Base class for scpup services. If you want to use a service you'll need to
  call EauService.get and pass the service name as an argument

  Class Attributes:
    view:
      The view currently being displayed.
  """
  view: scpup.EauView
  _view_stack: list[str] = []

  __slots__ = ()

  def _on_set_view(self) -> None:
    """This method is a hook for the subclasses of EauService so that they can
    do tasks when loading a new view"""

  @overload
  @classmethod
  def get(cls, service_name: Literal['EauDisplayService']) -> EauDisplayService:
    """Get the display service"""
  @overload
  @classmethod
  def get(cls, service_name: Literal['EauGameService']) -> EauGameService:
    """Get the game service"""
  @overload
  @classmethod
  def get(cls, service_name: Literal['EauEventService']) -> EauEventService:
    """Get the event service"""
  @overload
  @classmethod
  def get(cls, service_name: Literal['EauAudioService']) -> EauAudioService:
    """Get the audio service"""
  @classmethod
  def get(cls, service_name: str) -> EauService:
    service = cls._instances_.get(service_name, None)
    if not service:
      raise RuntimeError(f"Service '{service_name}' does not exist or has not been initialized.")
    return service

  @classmethod
  def set_view(cls, view: str):
    """Set the current view

    This method is very important since it calls a hook on all EauService
    subclasses to perform some tasks when loading a new view

    Args:
      view:
        The view to set
    """
    view_cls = scpup.EauView.get(view)
    if view_cls:
      view_instance = view_cls()
      if view in cls._view_stack:
        cls._view_stack = cls._view_stack[:cls._view_stack.index(view) + 1]
      else:
        cls._view_stack.append(view)
      cls.view = view_instance
    else:
      raise RuntimeError(f"View '{view}' was not found.")
    for service in cls._instances_.values():
      service._on_set_view()


@final
class EauDisplayService(EauService):
  """A service used for all display related tasks

  Attributes:
    _display:
      The main display of the game
    _background:
      The background of the current view
    _default_bg:
      The default background used in views that don't have a background
    viewport:
      The main display rect
  """

  __slots__: tuple = (
    "_display",
    "_background",
    "_default_bg",
    "viewport"
  )

  def __init__(self, *, size: tuple[int, int], icon_path: str | None, caption: str | None):
    """Initialize the display service"""
    self.viewport = pygame.Rect(0, 0, *size)
    self._display: pygame.Surface = pygame.display.set_mode(size)
    if icon_path:
      img, _ = load_image(icon_path)
      pygame.display.set_icon(img)
    if caption:
      pygame.display.set_caption(caption)
    pygame.mouse.set_visible(0)
    bg = pygame.Surface(self.size)
    bg.fill(pygame.Color(86, 193, 219))
    self._default_bg = bg.convert()
    self._background: pygame.surface.Surface = self._default_bg

  @property
  def size(self) -> tuple[int, int]:
    return self.viewport.size

  def _on_set_view(self) -> None:
    """Set the current view and the players sprites"""
    self._background = self.view.background or self._default_bg
    scpup.EauPlayer.set_sprites(self.view.player_sprite)
    self._display.blit(self._background, (0, 0))

  def update_view(self, *args, **kwargs) -> None:
    """Main display update method

    This method calls the `clear` method, then the `update` method, and then the
    `draw` method of the view and the players. This method also checks for
    collitions between the players sprites and the view sprites, and then
    between the players sprites and the other players sprites.

    Args:
      *args, **kwargs:
        Any arguments to pass to the sprites update method
    """
    self.view.clear(self._display, self._background)
    scpup.EauPlayer.clear(self._display, self._background)
    self.view.update(*args, rect=self.viewport, **kwargs)
    scpup.EauPlayer.update(*args, rect=self.viewport, **kwargs)
    self.view.draw(self._display)
    scpup.EauPlayer.draw(self._display)
    # scpup.EauPlayer.check_collitions()
    # scpup.EauPlayer.check_collitions(self.view.sprites)
    pygame.display.flip()


EAU_EVENT = pygame.event.custom_type()


@final
class EauEventService(EauService):
  """A service used for event related tasks"""
  __slots__ = ()

  def __init__(self) -> None:
    """Initializes the event service"""
    pygame.key.set_repeat()
    pygame.key.stop_text_input()
    pygame.event.set_blocked([
        pygame.MOUSEMOTION,
        pygame.WINDOWLEAVE,
        pygame.WINDOWENTER,
        pygame.WINDOWFOCUSLOST,
        pygame.WINDOWFOCUSGAINED,
        pygame.WINDOWSHOWN,
        pygame.WINDOWCLOSE,
        pygame.ACTIVEEVENT,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP,
        pygame.VIDEOEXPOSE,
        pygame.VIDEORESIZE,
        pygame.WINDOWEXPOSED,
        pygame.AUDIODEVICEADDED,
        pygame.AUDIODEVICEREMOVED
    ])
    # pygame.event.clear()

  def process_queue(self):
    """Main method which handles the event queue

    This method handles the event queue. It is intended to be so generic that
    it can be used in scpup as well as in other games, but work still in
    progress....
    """
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return False
      elif event.type == pygame.JOYDEVICEADDED:
        j: pygame.joystick.JoystickType = pygame.joystick.Joystick(event.device_index)
        scpup.EauCtrl.create(j)
      elif event.type == pygame.JOYDEVICEREMOVED:
        scpup.EauPlayer.remove_player(event.instance_id)
        scpup.EauCtrl.remove_ctrl(event.instance_id)
      elif event.type in [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN]:
        player: scpup.EauPlayer | None = scpup.EauPlayer(event.instance_id)
        if player:
          if event.type == pygame.JOYAXISMOTION:
            player.handle_joystick_input(event.axis, event.value)
          else:
            player.handle_joystick_input(event.button)
        elif event.type == pygame.JOYBUTTONDOWN:
          ctrl = scpup.EauCtrl(event.instance_id)
          if ctrl.action(event.button) == scpup.EauAction.START:
            scpup.EauPlayer.create(with_ctrl=ctrl)
      elif event.type == EAU_EVENT:
        if event.subtype == scpup.EauEventSubtype.QUIT:
          return False
        elif event.subtype == scpup.EauEventSubtype.VIEW:
          self.view.on(
            event_name=event.event_name,
            actioner=event.actioner,
            **(event.data if 'data' in event.__dict__ else {})
          )
        elif event.subtype == scpup.EauEventSubtype.NAV:
          EauService.set_view(event.to_view)
    return True

  @overload
  def post(
    self,
    subtype: Literal[scpup.EauEventSubtype.VIEW],
    *,
    event_name: str,
    actioner: scpup.EauSprite,
    data: dict[str, Any] = {}
  ):
    """Post an EAU_EVENT of VIEW subtype

    This method sends an event to the view so sprites can comunicate with it

    Args:
      event_name:
        The name of the event for the view to handle
    """
  @overload
  def post(self, subtype: Literal[scpup.EauEventSubtype.QUIT]):
    """Post en EAU_EVENT of QUIT subtype

    This method sends a quit event, and when received the game closes.
    """
  @overload
  def post(self, subtype: Literal[scpup.EauEventSubtype.NAV], *, to_view: str):
    """Post an EAU_EVENT of NAV subtype

    This method is used to navigate to another view

    Args:
      view_name:
        The name of the class or the class of the view to navigate to
    """
  def post(self, subtype: scpup.EauEventSubtype, **kwargs):
    ev = pygame.event.Event(EAU_EVENT, {
      "subtype": subtype,
      **kwargs
    })
    pygame.event.post(ev)


class EauChannel:
  """A wrapper for a pygame.mixer.Channel

  Attributes:
    channel: The wrapped channel
    sounds: the sounds loaded and stored by this instance
  """
  __slots__ = (
    "channel",
    "sounds"
  )

  def __init__(self, ch_idx: int):
    """Initialize an EauChannel with a channel id for the pygame.mixer.Channel

    Args:
      ch_idx: The index of the pygame.mixer.Channel
    """
    self.channel = pygame.mixer.Channel(ch_idx)
    self.sounds = dict()

  @property
  def volume(self) -> float:
    """Get the volume of this channel

    Returns:
      A number between 0 and 1
    """
    return round(self.channel.get_volume(), 1)

  @volume.setter
  def volume(self, value: float):
    """Sets the volume of this channel

    Args:
      value: a value between 0 and 1
    """
    self.channel.set_volume(round(value, 1))

  def load(self, sid: str, *paths: str):
    if sid not in self.sounds:
      self.sounds[sid] = load_sound(*paths)

  def play(self, sid: str):
    """Start playing a sound

    This will only start playing the sound if it has been previously loaded and
    there is no other sound playing

    Args:
      sid: The sound id.
    """
    if sid in self.sounds and self.channel.get_queue() is None:
      self.channel.play(self.sounds[sid])

  def pause(self):
    """Pause this channels playback"""
    self.channel.pause()

  def unpause(self):
    """Unpause this channels playback"""
    self.channel.unpause()

  def stop(self):
    """Stop this channels playback"""
    self.channel.stop()


class EauAudioService(EauService):
  """A service used for audio related tasks

  TODO: Maybe add the sounds dict to this class instead of being in each channel

  Attributes:
    bg: A channel for the background music
    sfx:
      A dict with all the channels available for sound effects. Each key is the
      player or view that is the "owner" of that channel.
  """
  __slots__ = (
    "sfx",
    "bg",
  )

  def __init__(self, *, bg_sound_path: str | None = None):
    """Initializes the audio service

    Args:
      bg_sound_path:
        The path segments of the background music, None means no background
        music. Defaults to None.
    """
    pygame.mixer.set_num_channels(5)  # Maybe remove this
    self.sfx = {
      "view": EauChannel(0),
      "p1": EauChannel(1),
      "p2": EauChannel(2),
      "p3": EauChannel(3),
      "p4": EauChannel(4),
    }
    if bg_sound_path:
      load_music(bg_sound_path)
      pygame.mixer.music.play(-1)

  def load(self, owner: Literal["p1", "p2", "p3", "p4", "view"], sound_id: str, *paths: str) -> None:
    """Load a sound given its file path and store it

    Args:
      sound_id:
        The key of the saved sound
      path:
        The path segments of the sound. It has to be somewhere under
        `<root>/assets/sounds/`.
    """
    self.sfx[owner].load(sound_id, *paths)

  def play(self, name: str, channel: Literal["p1", "p2", "p3", "p4", "view"] | None = "view") -> None:
    """Play a sound previously registered

    Args:
      name:
        The key that was used to store the sound
    """
    if channel:
      self.sfx[channel].play(name)
    else:
      sfxchannel = next((c for c in self.sfx.values() if name in c.sounds and c.channel.get_queue() is None), None)
      if sfxchannel:
        sfxchannel.play(name)

  @overload
  def volume(self, channel: str) -> float:
    """Get the volume of a channel

    Args:
      channel: Either bg for background or sfx for all the special effects

    Returns:
      float: The current volume of the channel
    """
  @overload
  def volume(self, channel: str, action: str) -> float:
    """Set the volume of a channel

    Args:
      channel: Either bg for background or sfx for all the special effects
      action: Either + or - to increase or decrease the volume

    Returns:
      float: The new volume of the channel
    """
  def volume(self, channel: str, action: str | None = None) -> float:
    if action:
      if channel == "bg":
        currvol = pygame.mixer.music.get_volume()
        # currvol = self.bg.volume
        if action == "-" and currvol > 0:
          pygame.mixer.music.set_volume(currvol - 0.1)
        elif action == "+" and currvol < 1:
          pygame.mixer.music.set_volume(currvol + 0.1)
        newvol = pygame.mixer.music.get_volume()
      else:
        currvol = list(self.sfx.values())[0].volume
        for sfx in self.sfx.values():
          if sfx.volume > 0 and action == '-':
            sfx.volume -= 0.1
          elif sfx.volume < 1 and action == '+':
            sfx.volume += 0.1
        newvol = list(self.sfx.values())[0].volume
      self._change_volume_surf(currvol, newvol, channel)
      return newvol
    else:
      vol = self.bg.volume if channel == "bg" else list(self.sfx.values())[0].volume
      return vol

  def init_volume_sprite(self, sprite: scpup.EauSprite):
    vol = self.volume(sprite.name)
    sub = sprite.image.subsurface(
      pygame.Rect(0, 0, 120 * vol, sprite.rect.height)
    )
    scpup.EauColor.VOLUME.apply(sub)

  def _change_volume_surf(self, currvol: float, newvol: float, channel: str):
    if currvol != newvol and 0 <= newvol <= 1:
      vol_sprite = next((spr for spr in self.view.sprites if spr.subgroup == "volume" and spr.name == channel), None)
      if not vol_sprite:
        return
      sub = vol_sprite.image.subsurface(
        pygame.Rect(120 * min(currvol, newvol), 0, 12, vol_sprite.rect.height)
      )
      if newvol > currvol:
        scpup.EauColor.VOLUME.apply(sub, scpup.EauColor.SEARCH_COLOR)
      else:
        scpup.EauColor.SEARCH_COLOR.apply(sub, scpup.EauColor.VOLUME)


class EauGameService(EauService):
  """Service used for tasks related to the game itself, for example storing the
  difficulty, or the map, or even saving/loading the game state.

  Attributes:
    difficulty: The game difficulty
    game_name:
      The game name. (Thinking that this library will not be used only by scpup
      but by other games too)
  """
  __slots__ = (
    "difficulty",
    "game_name"
  )

  def __init__(self, game_name: str) -> None:
    """Initializes the game service

    Args:
      game_name: The name of the game (e.g. Crystal Party)
    """
    self.game_name = game_name.strip()
    self.difficulty = scpup.EauDifficulty.MEDIUM

  @property
  def filename(self) -> str:
    return sub(r'[^\w]', '', self.game_name.replace(' ', '_').lower()) + '.mblk'

  def save(self):
    """Save the current state of the game

    This method saves the current state of the game in a json format XOR
    encrypted (with the key 31) in a file called: `<game_name>.mblk`. The json
    format of the saved game is the following:

    ```json
    {
      "difficulty": "int"
    }
    ```
    """
    data = dumps({"difficulty": self.difficulty.value}).encode()
    outdata = [x ^ 31 for x in data if x != 31 and x != 0]
    with open(self.filename, 'wb') as savefile:
      savefile.write(bytearray(outdata))

  def load(self):
    """Load a saved state of the game

    This method will try to load a file called `<game_name>.mblk` and XOR
    decrypt it (using 31 as the key).
    """
    file = self.filename
    if not os.path.exists(file):
      return
    with open(file, 'rb') as savedfile:
      indata = [x ^ 31 for x in savedfile.read() if x != 31 and x != 0]
    data = loads(bytes(indata).decode())
    self.difficulty = scpup.EauDifficulty(int(data["difficulty"]))
