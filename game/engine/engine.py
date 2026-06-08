from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from .scene import Scene


class Engine:
    def __init__(self) -> None:
        self.scene: Scene | None = None
        self.next_scene: Scene | None = None

    def switch(self, scene: Scene) -> None:
        """ sets up the next scene to switch to on next event/update """
        self.next_scene = scene

    def flush(self) -> None:
        """ exits the current scene and enters the next scene """
        if self.next_scene is not None:
            if self.scene is not None:
                self.scene.on_exit()
            self.scene = self.next_scene
            self.next_scene = None
            self.scene.on_enter()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.scene:
            self.scene.handle_event(event)
        self.flush() # events can trigger scene changes

    def update(self, dt: int) -> None:
        if self.scene:
            self.scene.update(dt)
        self.flush() # updates can trigger scene changes

    def draw(self, surface: pygame.Surface) -> None:
        if self.scene:
            self.scene.draw(surface)
