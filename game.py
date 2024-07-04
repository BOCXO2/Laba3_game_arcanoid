from tkinter import *
import random


class Ball():
    def __init__(self, canvas, platform, blocks, color):
        self.canvas = canvas
        self.platform = platform
        self.blocks = blocks
        self.oval = canvas.create_oval(200, 200, 215, 215, fill=color)
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -1
        self.touch_bottom = False

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]:
            if platform_pos[1] <= ball_pos[3] <= platform_pos[3]:
                return True
        return False

    def touch_block(self, ball_pos):
        for block in self.blocks:
            block_pos = self.canvas.coords(block.rect)
            if ball_pos[2] >= block_pos[0] and ball_pos[0] <= block_pos[2] and ball_pos[3] >= block_pos[1] and ball_pos[1] <= block_pos[3]:
                if ball_pos[1] >= block_pos[3] or ball_pos[3] <= block_pos[1]:
                    self.y = -self.y
                else:
                    self.blocks.remove(block)
                    self.canvas.delete(block.rect)
                    return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= 400:
            self.touch_bottom = True
        if self.touch_platform(pos):
            self.y = -3
        if self.touch_block(pos):
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= 500:
            self.x = -3


class Block():
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x+50, y+20, fill=color)


class Platform():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)

    def left(self, event):
        self.x = -2

    def right(self, event):
        self.x = 2

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= 500:
            self.x = 0


def show_game_over(outcome):
    game_over_window = Toplevel(window)
    game_over_window.title(outcome)
    game_over_window.geometry("600x500")
    game_over_window.config(bg="black")

    background_colors = ["red", "green", "blue", "yellow", "purple"]
    random_color = random.choice(background_colors)

    background_label = Label(game_over_window, bg=random_color)
    background_label.place(relwidth=1, relheight=1)

    game_over_label = Label(game_over_window, text=outcome, font=("Helvetica", 24, "bold"), fg="white", bg=random_color)
    game_over_label.place(relx=0.5, rely=0.4, anchor="center")


def game_loop():
    if not ball.touch_bottom and len(ball.blocks) > 0:
        ball.draw()
        platform.draw()
        window.after(10, game_loop)
    elif len(ball.blocks) == 0:
        show_game_over("WIN")
    else:
        show_game_over("LOSE")


window = Tk()
window.title("PLAY")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

canvas = Canvas(window, width=500, height=400)
canvas.pack()

platform = Platform(canvas, 'pink')

blocks = []
colors = ["red", "orange", "yellow", "green", "blue"]
for i in range(5):
    for j in range(5):
        block = Block(canvas, i*100, j*30, random.choice(colors))
        blocks.append(block)

ball = Ball(canvas, platform, blocks, 'blue')

game_loop()

window.mainloop()