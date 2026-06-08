import pygame
from ..engine.scene import Scene
from ..engine.engine import Engine
from .story import StoryScene


# vars for placeholder title screen
BG_COLOR = (18, 14, 28) # dark violet
TITLE_COLOR = (220, 160, 200) # soft pink
BTN_COLOR = (50, 30, 70) # violet
BTN_HOVER_COLOR = (80, 50, 100) # desaturated violet
BTN_TEXT_COLOR = (240, 220, 255) # pale violet

FONT_NAME = "segoeui"
TITLE_FONT_SIZE = 64
BTN_FONT_SIZE = 32

SCREEN_W, SCREEN_H = 1280, 720
BTN_W, BTN_H = 280, 60
BTN_CENTER = (SCREEN_W // 2, SCREEN_H // 2 + 80)
TITLE_CENTER = (SCREEN_W // 2, SCREEN_H // 2 - 40)

TITLE_TEXT = "class act's project yuri"
BTN_TEXT = "start"


class TitleScene(Scene):
    """ the main title screen of the game! """
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        self.font_title = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
        self.font_btn = pygame.font.SysFont(FONT_NAME, BTN_FONT_SIZE)
        self.btn_rect = pygame.Rect(0, 0, BTN_W, BTN_H)
        self.btn_rect.center = BTN_CENTER

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_rect.collidepoint(event.pos):
                self.engine.switch(StoryScene(self.engine))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_COLOR)

        title = self.font_title.render(TITLE_TEXT, True, TITLE_COLOR)
        surface.blit(title, title.get_rect(center=TITLE_CENTER))

        hovered = self.btn_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, BTN_HOVER_COLOR if hovered else BTN_COLOR, self.btn_rect, border_radius=8)
        btn_text = self.font_btn.render(BTN_TEXT, True, BTN_TEXT_COLOR)
        surface.blit(btn_text, btn_text.get_rect(center=self.btn_rect.center))
