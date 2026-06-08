# game/

the actual game code lives here!

## structure

The **engine** manages **scenes**, and **scenes** render **assets**.

## how scenes work

the `Engine` handles switching between them. each scene is responsible for its own rendering, input, and logic.

to switch scenes, a scene calls `self.engine.switch(SomeScene(self.engine))`

## adding a new scene (dishwashing minigame?)

1. create `scenes/myscene.py`, subclass `Scene`
2. override `handle_event`, `update`, and/or `draw`
3. switch to it from wherever: `self.engine.switch(MyScene(self.engine))`
