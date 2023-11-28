from __future__ import annotations

import pygame
from ._internal.services import EauService


class Game:
  __slots__ = ()

  def __init__(
    self,
    *,
    game_name: str,
    initial_view_name: str,
    views_path: str,
    sprites_path: str,
    font_path: str | None = None,
    window_size: tuple[int, int] = (1200, 800),
    icon_path: str | None = None,
    background_music_path: str | None = None,
  ):
    from .common.text import EauText
    from ._internal import load_package, EauDisplayService, EauEventService, EauAudioService, EauGameService

    pygame.init()

    EauDisplayService(size=window_size, caption=game_name, icon_path=icon_path)
    EauEventService()
    EauAudioService(bg_sound_path=background_music_path)
    EauGameService(game_name)

    EauText.set_font(font_path)

    load_package(views_path)
    load_package(sprites_path)

    EauService.set_view(initial_view_name)

  def play(self) -> None:
    clock = pygame.time.Clock()
    running = True
    eventService = EauService.get('EauEventService')
    displayService = EauService.get('EauDisplayService')
    while running:
      clock.tick(60)
      running = eventService.process_queue()
      displayService.update_view()
    pygame.quit()
