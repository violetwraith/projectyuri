import asyncio
import pygame
from .engine.engine import Engine
from .scenes.title import TitleScene

SCREEN_W, SCREEN_H = 1280, 720
FPS = 60


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    # pygame.display.set_caption("something here")
    clock = pygame.time.Clock()

    engine = Engine()
    engine.switch(TitleScene(engine)) # init engine with title screen scene

    running = True
    while running:
        dt = min(clock.tick(FPS), 100) # milliseconds since last frame (capped at 100)

        # feeds events to the active scene
        # https://www.pygame.org/docs/ref/event.html
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.update(dt) # the active scene updates before render time
        engine.draw(screen) # the active scene renders to the pygame frame buffer
        pygame.display.flip() # pushes the finished frame from the buffer to the display

        await asyncio.sleep(0) # yield point for browser rendering

    pygame.quit()


asyncio.run(main())
