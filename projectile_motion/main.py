"""Entry point to the simulation."""

import pyglet
from pyglet.window import Window

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

pyglet.resource.path = ["../assets"]
pyglet.resource.reindex()

window = Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption="Projectile Motion")

background = pyglet.image.SolidColorImagePattern(
    (255, 255, 255, 255)).create_image(WINDOW_WIDTH, WINDOW_HEIGHT)
# cannon = pyglet.resource.image("cannon.png")


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)


pyglet.app.run()
