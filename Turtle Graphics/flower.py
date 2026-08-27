import turtle

screen = turtle.Screen()
screen.bgcolor("black")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

turtle.tracer(1, 0)

colors = [
    "#ff1493",
    "#ff69b4",
    "#ba55d3",
    "#ba2be2",
    "#00bfff",
    "#00ffff"
]

def flower(size, depth):
    if depth == 0: 
        return

    t.color(colors[depth % len(colors)])

    for i in range(6):
        t.circle(size, 60)
        t.left(120)
        t.circle(size, 60)
        t.left(60)

    for i in range(6):
        t.forward(size)
        flower(size *0.35, depth - 1)
        t.backward(size)
        t.left(60)

flower(100, 4)

turtle.done()