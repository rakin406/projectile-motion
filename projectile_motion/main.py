"""Entry point to the simulation."""

import math
import sympy as sym
import pyglet
from pyglet.window import Window
from pyglet import shapes
from pyglet.window import key
from pyglet.window import mouse

# You might be wondering why there's a cannonball but no cannon. Well, that's
# because I changed my mind and wanted to keep things simple and finish the
# project ASAP. Besides, I have no idea how to sync cannon with the cannonball
# lol.

GRAVITY = 9.81
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FLOOR_HEIGHT = WINDOW_HEIGHT - 600
TEXT = "Horizontal range: {distance}m"

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
floor = shapes.Line(x=0, y=FLOOR_HEIGHT, x2=1280, y2=FLOOR_HEIGHT,
                    width=5, color=(0, 0, 0), batch=batch)

# Create cannonball sprite
# WARNING: y-axis of the sprite is hardcoded.
cannonball_image = pyglet.resource.image("cannonball.png")
cannonball = pyglet.sprite.Sprite(cannonball_image, batch=batch)
cannonball.scale = 0.15
cannonball.x = 25.0
cannonball.y = FLOOR_HEIGHT

# Create bucket sprite
# WARNING: y-axis of the bucket is hardcoded.
bucket_image = pyglet.resource.image("bucket.png")
bucket = pyglet.sprite.Sprite(bucket_image, batch=batch)
bucket.scale = 0.2
bucket.x = (WINDOW_WIDTH // 2) - (bucket.width / 2)
bucket.y = FLOOR_HEIGHT + 3
bucket.dx = 400.0


def get_horizontal_range() -> int:
    bucket_center_x = bucket.x + (bucket.width / 2)
    cannonball_center_x = cannonball.x + (cannonball.width / 2)
    return math.ceil(bucket_center_x - cannonball_center_x)


label = pyglet.text.Label(TEXT.format(distance=get_horizontal_range()),
                          font_name="Times New Roman",
                          font_size=20,
                          color=(0, 0, 0, 255),
                          x=10, y=WINDOW_HEIGHT - 30,
                          width=500,
                          multiline=True,
                          batch=batch)


def find_vel_derivative(horizontal_range):
    """Find derivative of initial velocity."""
    x = sym.symbols("x")    # Angle
    return sym.diff(sym.sqrt((horizontal_range * GRAVITY) / sym.sin(2 * x)), x)


def find_best_angle(derivative):
    return sym.solve(sym.Eq(derivative, 0))


def get_initial_vel(horizontal_range, angle) -> float:
    return math.sqrt((horizontal_range * GRAVITY) / math.sin(2 * angle))


def get_horizontal_vel(initial_vel, angle) -> float:
    return initial_vel * math.cos(angle)


started = False
angle = None
initial_vel = None
horizontal_vel = None


@window.event
def on_key_press(symbol, _):
    # Start the simulation
    if symbol == key.SPACE:
        global started, angle, initial_vel, horizontal_vel
        started = True
        horizontal_range = get_horizontal_range()
        derivative = find_vel_derivative(horizontal_range)
        angle = find_best_angle(derivative)[0]
        initial_vel = get_initial_vel(horizontal_range, angle)
        horizontal_vel = get_horizontal_vel(initial_vel, angle)
    elif symbol == key.R:
        # TODO: Implement reset mechanism.
        pass


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    batch.draw()


def move_bucket(dt):
    if mousebuttons[mouse.LEFT] and bucket.x > (cannonball.x + cannonball.width):
        bucket.x -= bucket.dx * dt
    elif mousebuttons[mouse.RIGHT] and (bucket.x + bucket.width) < window.get_size()[0]:
        bucket.x += bucket.dx * dt

    # Update the text
    label.text = TEXT.format(distance=get_horizontal_range())


def update(dt):
    if started:
        # Move in x-axis with constant horizontal velocity
        if cannonball.x <= bucket.x:
            cannonball.x += horizontal_vel * dt
    else:
        move_bucket(dt)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
