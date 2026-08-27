import math
from turtle import *
import time

def hearta(k):
    return 15 * math.sin(k)**3

def heartb(k):
    return 12 * math.cos(k) - 5 * math.cos(2*k) - 2 * math.cos(3*k) - math.cos(4*k)

speed(0)
bgcolor("black")
pensize(2)
hideturtle()
tracer(0)

for i in range(500):
    color("#f73487")
    x = hearta(i) * 20
    y = heartb(i) * 20
    goto(x, y)
    goto(0, 0)

penup()
goto(0, -20)

colors = ["#ff007f", "#ff5da6", "#ff66cc", "#ff99e6", "#ffffff"]

for glow in range(20):
    color(colors[glow % len(colors)])
    write("MOM DAD", align="center", font=("Arial", 24 + glow, "bold"))
    time.sleep(0.2)
    undo()

color("#ff66cc")
write("MOM DAD", align="center", font=("Arial", 24, "bold"))

done()