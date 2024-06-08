"""Entry point to the simulation."""

import pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet.window import mouse

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FLOOR_HEIGHT = WINDOW_HEIGHT - 600

pyglet.resource.path = ["../assets"]
pyglet.resource.reindex()

window = Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                caption="Projectile Motion")

# Monitor mouse state
mousebuttons = mouse.MouseStateHandler()
window.push_handlers(mousebuttons)

batch = pyglet.graphics.Batch()

# Create white background
background = pyglet.image.SolidColorImagePattern(
    (255, 255, 255, 255)).create_image(WINDOW_WIDTH, WINDOW_HEIGHT)

# Create a straight solid floor
floor = pyglet.shapes.Line(x=0, y=FLOOR_HEIGHT, x2=1280, y2=FLOOR_HEIGHT,
                           width=5, color=(0, 0, 0), batch=batch)

# Create cannon sprite
# WARNING: y-axis of the cannon is hardcoded.
cannon_image = pyglet.resource.image("cannon.png")
cannon = pyglet.sprite.Sprite(
    cannon_image, x=10, y=FLOOR_HEIGHT - 21, batch=batch)
cannon.scale = 0.1

# Create bucket sprite
# WARNING: y-axis of the bucket is hardcoded.
bucket_image = pyglet.resource.image("bucket.png")
bucket = pyglet.sprite.Sprite(
    bucket_image, x=WINDOW_WIDTH // 2, y=FLOOR_HEIGHT + 3, batch=batch)
bucket.scale = 0.2
bucket.dx = 400.0


@window.event
def on_key_press(symbol, _):
    if symbol == key.SPACE:
        # TODO: Start the simulation.
        pass
    elif symbol == key.R:
        # TODO: Implement reset mechanism.
        pass


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    batch.draw()


def move_bucket(dt):
    if mousebuttons[mouse.LEFT]:
        bucket.x -= bucket.dx * dt
    elif mousebuttons[mouse.RIGHT]:
        bucket.x += bucket.dx * dt


if __name__ == "__main__":
    pyglet.clock.schedule_interval(move_bucket, 1 / 60.0)
    pyglet.app.run()
