import turtle
import math
import colorsys
import random

# ============================================================
#                    NEON HEART ANIMATION
# ============================================================

WIDTH = 900
HEIGHT = 750

HEART_SCALE = 16
NUMBER_OF_LINES = 280
ANIMATION_SPEED = 8

# ------------------------------------------------------------
# Screen
# ------------------------------------------------------------

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("❤️ Neon Mathematical Heart")
screen.tracer(0, 0)

# ------------------------------------------------------------
# Background stars
# ------------------------------------------------------------

stars = turtle.Turtle()
stars.hideturtle()
stars.penup()

for _ in range(100):
    x = random.randint(-WIDTH // 2, WIDTH // 2)
    y = random.randint(-HEIGHT // 2, HEIGHT // 2)

    size = random.choice([1, 1, 1, 2])

    stars.goto(x, y)
    stars.dot(size, "white")


# ------------------------------------------------------------
# Heart turtle
# ------------------------------------------------------------

heart = turtle.Turtle()
heart.hideturtle()
heart.speed(0)
heart.penup()


# ------------------------------------------------------------
# Mathematical heart
# ------------------------------------------------------------

def heart_point(t, scale=HEART_SCALE):
    """
    Parametric heart equation.

    t goes from 0 to 2π.
    """

    x = 16 * math.sin(t) ** 3

    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )

    return x * scale, y * scale


# ------------------------------------------------------------
# Rainbow color
# ------------------------------------------------------------

def rainbow_color(value):
    """
    Convert a value between 0 and 1
    into a rainbow RGB color.
    """

    r, g, b = colorsys.hsv_to_rgb(value % 1, 1, 1)

    return r, g, b


# Turtle normally accepts RGB values from 0-1
screen.colormode(1.0)


# ------------------------------------------------------------
# Pre-calculate heart points
# ------------------------------------------------------------

points = []

for i in range(NUMBER_OF_LINES):

    # IMPORTANT:
    # Full 0 → 2π range creates the complete heart.
    t = (2 * math.pi * i) / NUMBER_OF_LINES

    x, y = heart_point(t)

    points.append((x, y))


# ------------------------------------------------------------
# Animation
# ------------------------------------------------------------

current_line = 0


def draw_next_line():

    global current_line

    if current_line >= len(points):
        animate_pulse()
        return

    x, y = points[current_line]

    # Start from the center
    heart.goto(0, 0)

    # Rainbow color
    color = rainbow_color(
        current_line / NUMBER_OF_LINES
    )

    heart.pencolor(color)

    # Different line widths for a neon effect
    heart.pensize(1)

    heart.pendown()
    heart.goto(x, y)
    heart.penup()

    current_line += 1

    screen.update()

    # Draw the next line
    screen.ontimer(
        draw_next_line,
        ANIMATION_SPEED
    )


# ------------------------------------------------------------
# Pulse animation
# ------------------------------------------------------------

pulse_frame = 0


def animate_pulse():

    global pulse_frame

    heart.clear()

    pulse = 1 + 0.035 * math.sin(pulse_frame * 0.12)

    for i, (original_x, original_y) in enumerate(points):

        x = original_x * pulse
        y = original_y * pulse

        heart.goto(0, 0)

        color = rainbow_color(
            (i / NUMBER_OF_LINES)
            + pulse_frame * 0.002
        )

        heart.pencolor(color)

        # Main neon line
        heart.pensize(1)

        heart.pendown()
        heart.goto(x, y)
        heart.penup()

    screen.update()

    pulse_frame += 1

    screen.ontimer(
        animate_pulse,
        25
    )


# ------------------------------------------------------------
# Start animation
# ------------------------------------------------------------

draw_next_line()

turtle.done()