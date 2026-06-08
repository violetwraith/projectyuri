# from __future__ import annotations
import json
import os
import pygame
from ..engine.scene import Scene
from ..engine.engine import Engine

# vars for placeholder mockup recreation

SCREEN_W, SCREEN_H = 1280, 720

# sidebar
SIDEBAR_W = 260
SIDEBAR_X = SCREEN_W - SIDEBAR_W
SIDEBAR_TOP_H = 200     # stats section
SIDEBAR_BOTTOM_H = 120  # bottom section
SIDEBAR_DIVIDER_1_Y = SIDEBAR_TOP_H
SIDEBAR_DIVIDER_2_Y = SCREEN_H - SIDEBAR_BOTTOM_H

SIDEBAR_COLOR = (18, 14, 28) # dark violet
SIDEBAR_BORDER_COLOR = (80, 50, 100) # desaturated violet
SIDEBAR_BORDER_W = 8
SIDEBAR_PADDING_X = 32
STAT_PADDING_Y = 32 # padding from the top of the screen to first stat
STAT_GAP = 16 # padding between stat items
MENU_PADDING_Y = 32 # padding from the top divider down to first menu item
MENU_GAP = 48 # padding between menu items
STAT_DAY = "DAY 1"
STAT_MONEY = "$41.63"
MENU_ITEMS = ["Q.SAVE", "SAVE", "LOAD", "HISTORY", "AUTO", "PREFS"]

# dialogue box
BG_W = SCREEN_W - SIDEBAR_W
DIALOG_H = 256
DIALOG_Y = SCREEN_H - DIALOG_H
DIALOG_BG_COLOR = (10, 10, 10, 200) # super transparent
DIALOG_PADDING_X = 48 # left/right margin
DIALOG_PADDING_Y = 24 # top/bottom margin
NAME_TEXT_GAP = 16 # vertical space under speaker name

# colors
TEXT_COLOR = (240, 240, 240) # off white

# fonts
FONT_NAME = "segoeui"
STAT_FONT_SIZE = 52
MENU_FONT_SIZE = 24
NAME_FONT_SIZE = 32
DIALOGUE_FONT_SIZE = 24

# typewriter effet speed
MS_PER_CHAR = 20


def load_script(script_id: str) -> list[dict]:
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets", "dialogue", f"{script_id}.json"
    )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class StoryScene(Scene):
    """ the visual novel content of the game! """

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

        self.font_stat = pygame.font.SysFont(FONT_NAME, STAT_FONT_SIZE, bold=True)
        self.font_menu = pygame.font.SysFont(FONT_NAME, MENU_FONT_SIZE)
        self.font_name = pygame.font.SysFont(FONT_NAME, NAME_FONT_SIZE)
        self.font_text = pygame.font.SysFont(FONT_NAME, DIALOGUE_FONT_SIZE)

        self.dialog_surface = pygame.Surface((BG_W, DIALOG_H), pygame.SRCALPHA)

    def on_enter(self) -> None:
        self.dialogue: list[dict] = load_script("demo") # the full list of lines loaded from JSON
        self.line_index = 0 # which line in dialogue we're on
        self.chars_revealed = 0 # how many characters of the current line to show (typewriter)
        self.typewriter_ms = 0 # ms accumulator between character reveals

    @property
    def current_line(self) -> dict | None:
        if self.line_index >= len(self.dialogue):
            return None
        return self.dialogue[self.line_index]

    def handle_event(self, event: pygame.event.Event) -> None:
        advance = (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ) or (
            event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)
        )
        if not advance or self.current_line is None:
            return

        if self.chars_revealed < len(self.current_line["text"]):
            # skip typewriter if not complete
            self.chars_revealed = len(self.current_line["text"])
        else:
            # go to next line if typewriter is complete
            self.line_index += 1
            self.chars_revealed = 0
            self.typewriter_ms = 0

    def update(self, dt: int) -> None:
        if self.current_line is None:
            return
        
        current_line_len = len(self.current_line["text"])
        if self.chars_revealed < current_line_len:
            self.typewriter_ms += dt
            new_chars, self.typewriter_ms = divmod(self.typewriter_ms, MS_PER_CHAR)
            self.chars_revealed = min(self.chars_revealed + new_chars, current_line_len)

    def draw(self, surface: pygame.Surface) -> None:
        draw_background(surface)
        draw_sidebar(surface, self.font_stat, self.font_menu)
        if self.current_line is not None:
            draw_dialogue(surface, self.dialog_surface, self.current_line, self.chars_revealed, self.font_name, self.font_text)


def draw_background(surface: pygame.Surface) -> None:
    pygame.draw.rect(surface, (0, 0, 0), (0, 0, BG_W, SCREEN_H))


def draw_sidebar(surface: pygame.Surface, font_stat: pygame.font.Font, font_menu: pygame.font.Font) -> None:
    # background
    pygame.draw.rect(surface, SIDEBAR_COLOR, (SIDEBAR_X, 0, SIDEBAR_W, SCREEN_H))

    # left border
    pygame.draw.rect(surface, SIDEBAR_BORDER_COLOR, (SIDEBAR_X, 0, SIDEBAR_BORDER_W, SCREEN_H))

    # section borders
    pygame.draw.rect(surface, SIDEBAR_BORDER_COLOR, (SIDEBAR_X, SIDEBAR_DIVIDER_1_Y, SIDEBAR_W, SIDEBAR_BORDER_W))
    pygame.draw.rect(surface, SIDEBAR_BORDER_COLOR, (SIDEBAR_X, SIDEBAR_DIVIDER_2_Y, SIDEBAR_W, SIDEBAR_BORDER_W))

    # stats
    day = font_stat.render(STAT_DAY, True, TEXT_COLOR)
    surface.blit(day, (SIDEBAR_X + SIDEBAR_PADDING_X, STAT_PADDING_Y))

    money = font_stat.render(STAT_MONEY, True, TEXT_COLOR)
    surface.blit(money, (SIDEBAR_X + SIDEBAR_PADDING_X, STAT_PADDING_Y + day.get_height() + STAT_GAP))

    # menu
    for i, item in enumerate(MENU_ITEMS):
        label = font_menu.render(item, True, TEXT_COLOR)
        surface.blit(label, (SIDEBAR_X + SIDEBAR_PADDING_X, SIDEBAR_DIVIDER_1_Y + SIDEBAR_BORDER_W + MENU_PADDING_Y + i * MENU_GAP))

    # bottom empty... for now


def draw_dialogue(
    surface: pygame.Surface,
    dialog_surf: pygame.Surface,
    line: dict,
    char_index: float,
    font_name: pygame.font.Font,
    font_text: pygame.font.Font,
) -> None:
    dialog_surf.fill(DIALOG_BG_COLOR)
    surface.blit(dialog_surf, (0, DIALOG_Y))

    name_surf = font_name.render(line["name"], True, TEXT_COLOR)
    surface.blit(name_surf, (DIALOG_PADDING_X, DIALOG_Y + DIALOG_PADDING_Y))

    text_rect = pygame.Rect(
        DIALOG_PADDING_X,
        DIALOG_Y + DIALOG_PADDING_Y + name_surf.get_height() + NAME_TEXT_GAP,
        BG_W - DIALOG_PADDING_X * 2,
        DIALOG_H - DIALOG_PADDING_Y * 2 - name_surf.get_height() - NAME_TEXT_GAP,
    )
    render_wrapped(surface, font_text, line["text"], char_index, TEXT_COLOR, text_rect)


def render_wrapped(
    surface: pygame.Surface,
    font: pygame.font.Font,
    full_text: str,
    chars_revealed: int,
    color: tuple,
    rect: pygame.Rect,
) -> None:
    """ word-wraps full_text for stable layout, then reveals only `chars_revealed` characters """
    words = full_text.split(" ")
    lines: list[str] = []
    current = "" # buffer for wrap in progress
    for word in words:
        # try to add the next word
        test = (current + " " + word).strip()
        if font.size(test)[0] <= rect.width:
            # if it fits, keep trying
            current = test
        else:
            # if it wraps, start a new line
            if current:
                lines.append(current)
            current = word # new line starts with word that broke the last line
    if current:
        lines.append(current)

    # reveal up to `chars_revealed` chars across the stable wrapped lines
    remaining = chars_revealed
    y = rect.y
    for i, line in enumerate(lines):
        if remaining <= 0:
            break

        if remaining >= len(line):
            surface.blit(font.render(line, True, color), (rect.x, y))
            remaining -= len(line) # + (1 if i < len(lines) - 1 else 0) for linebreaks???? test this
            
        else:
            surface.blit(font.render(line[:remaining], True, color), (rect.x, y))
            break

        y += font.get_linesize()
