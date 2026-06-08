from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from .engine import Engine


class Scene:
    """ this is the base class, actual scenes inherit this """

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: int) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass
