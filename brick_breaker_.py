from tkinter import *
import time
from math import *
from random import *

score = 1
dimention = 60
root = Tk()
root.title("Brick Breaker")
geometry = str(12 * dimention + 70) + 'x' + str(9 * dimention)
root.geometry(geometry)
root.resizable(height=False, width=False)
canvas = Canvas(width=12 * dimention + 70, height=9 * dimention)
canvas.pack()
canvas.create_rectangle(0, 0, 12 * dimention, 9 * dimention)
canvas.create_text(12 * dimention + 35, 70, text="score: " + str(score), tag="score")
rectangle = []
lost = False



def generate_rectangle():
    global score
    number = randint(2, 3)
    rectangles = []
    numbers = [0, 2, 4, 6, 8, 10]
    shuffle(numbers)
    for i in range(number):
        tag = "rectangle" + str(score) + "_" + str(i)
        rectangles.append(Rectangle(canvas, "blue", numbers[i] * dimention, 0, score, tag))
    rectangle.append(rectangles)


def direction(event):
    global lost
    if not lost:
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


def score_up():
    global score
    for i in range(score):
        lenght = len(rectangle[i])
        for j in range(lenght):
            rectangle[i][j].move()
    score += 1
    canvas.delete("score")
    canvas.create_text(12 * dimention + 35, 70, text="score: " + str(score), tag="score")


def startGame(event):
    global score
    global lost
    if not lost:
        canvas.delete("arrow")
        while ball.groundHit > 0:
            ball.move()
            root.update()
            time.sleep(0.005)
        score_up()
        generate_rectangle()
        ball.restore()


def lose():
    global score
    global lost
    lost = True
    canvas.create_text(6 * dimention, 4.5 * dimention, text="your score : " + str(score + 1), font=("Times", 30))


class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.position = canvas.create_oval(6 * dimention - 5, 9 * dimention - 15, 6 * dimention + 5, 9 * dimention - 5,
                                           fill=color, tag="ballInitial")
        self.groundHit = 1
        self.xDirection = 1
        self.yDirection = -1
        self.power = 0.5

    def setDirection(self, xDirection, yDirection):
        self.xDirection = xDirection
        self.yDirection = yDirection

    def restore(self):
        currentPosition = self.canvas.coords(self.position)
        self.canvas.delete("ballInitial")
        self.position = canvas.create_oval(currentPosition[0], currentPosition[1], currentPosition[2],
                                           currentPosition[3], fill="blue", tag="ballInitial")
        self.groundHit = 1
        self.power += 0.5

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
        for i in range(score):
            lenght = len(rectangle[i])
            for j in range(lenght):
                if rectangle[i][j].exist:
                    rectangle[i][j].react(ball)


class Rectangle:
    def __init__(self, canvas, color, x, y, straight, tag):
        self.tag = tag
        self.canvas = canvas
        self.position = canvas.create_rectangle(x, y, x + 2 * dimention, y + dimention, fill=color, tag=tag)
        self.straight = straight
        self.exist = True
        self.write_straight()
        self.color()

    def react(self, ball):
        hit = False
        currentPosition = ball.canvas.coords(ball.position)
        rectanglePosition = self.canvas.coords(self.position)
        if currentPosition[1] >= rectanglePosition[1] and currentPosition[1] <= rectanglePosition[3] and \
                currentPosition[0] <= rectanglePosition[2] and currentPosition[2] >= rectanglePosition[0]:
            ball.yDirection *= -1
            hit = True
        if currentPosition[3] >= rectanglePosition[1] and currentPosition[3] <= rectanglePosition[3] and \
                currentPosition[0] <= rectanglePosition[2] and currentPosition[2] >= rectanglePosition[0]:
            ball.yDirection *= -1
            hit = True
        if currentPosition[0] >= rectanglePosition[0] and currentPosition[0] <= rectanglePosition[2] and \
                currentPosition[1] <= rectanglePosition[3] and currentPosition[3] >= rectanglePosition[1]:
            ball.xDirection *= -1
            hit = True
        if currentPosition[2] >= rectanglePosition[0] and currentPosition[2] <= rectanglePosition[2] and \
                currentPosition[1] <= rectanglePosition[3] and currentPosition[3] >= rectanglePosition[1]:
            ball.xDirection *= -1
            hit = True
        if hit:
            self.straight -= ball.power
            self.canvas.delete("text" + self.tag)
            self.check_destruction()
            if self.exist:
                self.write_straight()
                self.color()

    def check_destruction(self):
        if self.straight <= 0:
            self.exist = False
            self.canvas.delete(self.tag)
            self.canvas.delete("text" + self.tag)

    def move(self):
        self.canvas.delete("text" + self.tag)
        global lost
        if self.exist:
            self.canvas.move(self.position, 0, dimention)
            rectanglePosition = self.canvas.coords(self.position)
            if rectanglePosition[3] == 9 * dimention:
                lose()
            self.write_straight()

    def write_straight(self):
        rectanglePosition = self.canvas.coords(self.position)
        x = (rectanglePosition[0] + rectanglePosition[2]) / 2
        y = (rectanglePosition[1] + rectanglePosition[3]) / 2
        a = self.straight
        if a - int(a) == 0:
            a = int(a)
        self.canvas.create_text(x, y, text=str(a), tag="text" + self.tag)

    def color(self):
        if self.straight < 4:
            self.canvas.itemconfig(self.position, fill="tomato2")
        elif self.straight < 8:
            self.canvas.itemconfig(self.position, fill="tomato3")
        elif self.straight < 12:
            self.canvas.itemconfig(self.position, fill="OrangeRed2")
        else:
            self.canvas.itemconfig(self.position, fill="red")


ball = Ball(canvas, "blue")
generate_rectangle()

canvas.bind("<B1-Motion>", direction)
canvas.bind("<ButtonRelease-1>", startGame)

root.mainloop()
