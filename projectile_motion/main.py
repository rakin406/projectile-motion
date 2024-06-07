"""Entry point to the simulation."""

import pyglet
from pyglet.window import Window

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FLOOR_HEIGHT = WINDOW_HEIGHT - 600

pyglet.resource.path = ["../assets"]
pyglet.resource.reindex()

window = Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                caption="Projectile Motion")
batch = pyglet.graphics.Batch()

# Create white background
background = pyglet.image.SolidColorImagePattern(
    (255, 255, 255, 255)).create_image(WINDOW_WIDTH, WINDOW_HEIGHT)

# Create a straight solid floor
floor = pyglet.shapes.Line(x=0, y=FLOOR_HEIGHT, x2=1280, y2=FLOOR_HEIGHT,
                           width=5, color=(0, 0, 0), batch=batch)

# cannon = pyglet.resource.image("cannon.png")


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    batch.draw()


pyglet.app.run()
