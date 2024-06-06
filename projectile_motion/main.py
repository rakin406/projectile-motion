"""Entry point to the simulation."""

import pyglet

pyglet.resource.path = ["../assets"]
pyglet.resource.reindex()

window = pyglet.window.Window()
ground = pyglet.resource.image("ground.png")


@window.event
def on_draw():
    window.clear()
    ground.blit(0, 0)


pyglet.app.run()
