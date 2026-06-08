import sys
import os
# pygbag runs main.py as __main__, so relative imports break without this:
sys.path.insert(0, os.path.dirname(__file__) or '.')

import asyncio
import pygame
try:
    from .engine.engine import Engine    # python -m game
    from .scenes.title import TitleScene
except ImportError:
    from engine.engine import Engine     # pygbag
    from scenes.title import TitleScene

SCREEN_W, SCREEN_H = 1280, 720
FPS = 60


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    # pygame.display.set_caption("something here")
    clock = pygame.time.Clock()

    engine = Engine()
    engine.switch(TitleScene(engine))

    running = True
    while running:
        dt = min(clock.tick(FPS), 100) # milliseconds since last frame (capped at 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.update(dt)
        engine.draw(screen)
        pygame.display.flip() # pushes the finished frame from the buffer to the display
        await asyncio.sleep(0) # yield point for browser event loop (required by pygbag)

    pygame.quit()


asyncio.run(main()) # pygbag patches this to use the browser event loop
