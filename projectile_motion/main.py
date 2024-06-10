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
# project ASAP.

GRAVITY = 9.81
SPEED_MULTIPLIER = 3  # Increase to speed up the simulation
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FLOOR_HEIGHT = WINDOW_HEIGHT - 600
INITIAL_BALL_X = 25.0
TEXT = """Horizontal range: {}m
Maximum height: {}m
Total time: {}s
Angle: {} rad
Initial velocity: {}m/s
Horizontal velocity: {}m/s
Vertical velocity: {}m/s"""

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
cannonball.x = INITIAL_BALL_X

# Create bucket sprite
# WARNING: y-axis of the bucket is hardcoded.
bucket_image = pyglet.resource.image("bucket.png")
bucket = pyglet.sprite.Sprite(bucket_image, batch=batch)
bucket.scale = 0.2
bucket.x = (WINDOW_WIDTH // 2) - (bucket.width / 2)
bucket.y = FLOOR_HEIGHT + 3
bucket.dx = 400.0

# Create a ledge for cannonball
ledge_y = (bucket.y + bucket.height) - 35.0
ledge = shapes.Line(x=0, y=ledge_y, x2=75.0, y2=ledge_y,
                    width=5, color=(0, 0, 0), batch=batch)
INITIAL_BALL_Y = ledge_y
cannonball.y = INITIAL_BALL_Y

label = pyglet.text.Label(
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


def get_total_time(initial_vel, angle) -> float:
    return (2 * initial_vel * math.sin(angle)) / GRAVITY


# NOTE: This is probably a wrong method because the cannonball is elevated by
# the ledge so that means the maximum height should be greater.
def get_max_height(initial_vel, angle) -> float:
    return ((initial_vel ** 2) * (math.sin(angle) ** 2)) / 2 * GRAVITY


def get_horizontal_range() -> float:
    bucket_center_x = bucket.x + (bucket.width / 2)
    cannonball_center_x = cannonball.x + (cannonball.width / 2)
    return bucket_center_x - cannonball_center_x


started = False
horizontal_range = 0.0
max_height = 0.0
total_time = 0.0
angle = 0.0
initial_vel = 0.0
horizontal_vel = 0.0
projectile_time = 0.0


@window.event
def on_key_press(symbol, _):
    # Start the simulation
    if symbol == key.SPACE:
        global started, max_height, total_time, angle, initial_vel, horizontal_vel
        started = True
        derivative = find_vel_derivative(horizontal_range)
        angle = find_best_angle(derivative)[0]
        initial_vel = get_initial_vel(horizontal_range, angle)
        horizontal_vel = get_horizontal_vel(initial_vel, angle)
        max_height = get_max_height(initial_vel, angle)
        total_time = get_total_time(initial_vel, angle)
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


def update(dt):
    global horizontal_range

    if started:
        if cannonball.x <= (bucket.x + bucket.width / 2):
            global projectile_time
            projectile_time += dt * SPEED_MULTIPLIER

            initial_vertical_vel = initial_vel * math.sin(angle)
            cannonball.x = INITIAL_BALL_X + horizontal_vel * projectile_time
            cannonball.y = INITIAL_BALL_Y + initial_vertical_vel * projectile_time \
                - 0.5 * GRAVITY * (projectile_time ** 2)

            current_vertical_vel = initial_vertical_vel - GRAVITY * projectile_time

            # Update the text
            label.text = TEXT.format(
                round(horizontal_range, 2),
                round(max_height, 2),
                round(total_time, 2),
                round(angle, 2),
                round(initial_vel, 2),
                round(horizontal_vel, 2),
                round(current_vertical_vel, 2))
    else:
        move_bucket(dt)
        horizontal_range = get_horizontal_range()
        label.text = TEXT.format(round(horizontal_range, 2), 0, 0, 0, 0, 0, 0)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
