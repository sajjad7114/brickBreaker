from tkinter import *
import time
from math import *
from random import *

dimention = 60
root = Tk()
root.title("Brick Breaker")
geometry = str(12 * dimention) + 'x' + str(9 * dimention)
root.geometry(geometry)
root.resizable(height=False, width=False)
canvas = Canvas(width=12 * dimention, height=9 * dimention)
canvas.pack()


def direction(event):
    ballPosition = ball.canvas.coords(ball.position)
    ballx = (ballPosition[0] + ballPosition[2]) / 2
    bally = (ballPosition[1] + ballPosition[3]) / 2
    x = event.x - ballx
    y = event.y - bally
    if y > -1:
        y = -1
    a = sqrt(x * x + y * y)
    x = 5 * x / a
    y = 5 * y / a
    canvas.delete("arrow")
    canvas.create_line(ballx, bally, ballx + 10 * x, bally + 10 * y, arrow=LAST, tag="arrow")

    ball.setDirection(x, y)


def startGame(event):
    canvas.delete("arrow")
    while ball.groundHit >= 0:
        ball.move()
        root.update()
        time.sleep(0.01)
    ball.restore()


class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.position = canvas.create_oval(6 * dimention - 5, 9 * dimention - 15, 6 * dimention + 5, 9 * dimention - 5,
                                           fill=color, tag="ballInitial")
        self.groundHit = 2
        self.xDirection = 1
        self.yDirection = -1

    def setDirection(self, xDirection, yDirection):
        self.xDirection = xDirection
        self.yDirection = yDirection

    def restore(self):
        currentPosition = self.canvas.coords(self.position)
        self.canvas.delete("ballInitial")
        self.position = canvas.create_oval(currentPosition[0], currentPosition[1], currentPosition[2],
                                           currentPosition[3], fill="red", tag="ballInitial")
        self.groundHit = 2

    def move(self):
        self.canvas.move(self.position, self.xDirection, self.yDirection)
        currentPosition = self.canvas.coords(self.position)
        if currentPosition[1] <= 0:
            self.yDirection *= -1
        if currentPosition[3] >= 9 * dimention - 5:
            self.groundHit -= 1
            self.yDirection *= -1
        if currentPosition[0] <= 0:
            self.xDirection *= -1
        if currentPosition[2] >= 12 * dimention:
            self.xDirection *= -1


ball = Ball(canvas, "red")

canvas.bind("<B1-Motion>", direction)
canvas.bind("<ButtonRelease-1>", startGame)

root.mainloop()
