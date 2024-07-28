from tkinter import *
import time
import customtkinter as ctk
import random
import sys


MENU, PLAYING, GAME_OVER = "Menu", "Playing", "Game Over"
game_state = MENU


tk = ctk.CTk()
tk.title("Blackout")
tk.geometry("1920x1080")


c=Canvas(tk,width=1920,height=1080,background="grey8")
c.pack()


play_button = None
menu_button = None


def calculate_level(score):
    global level
    level = 0
    while True:
        marker = (25 / 2) * level ** 2 + (25 / 2) * level
        if marker > score:
            break
        level += 1
    return level - 1


def show_menu():
    global game_state, play_button
    game_state = MENU
    c.delete("all")  
    play_button = ctk.CTkButton(tk, text="Play", command=start_game, corner_radius=20, bg_color="grey8")
    play_button.place(relx=0.5, rely=0.5, anchor=CENTER)


def start_game():
    global game_state, player, score, scoretext, play_button, level, leveltext
    game_state = PLAYING
    score = 0
    level = calculate_level(score)
    c.delete("all")  


    if play_button is not None:
        play_button.destroy()
        play_button = None


    floor = c.create_rectangle(0, 1080, 1920, 1000, fill="black")
    blackouttext = c.create_text(960, 1025, text="BLACKOUT", font=('Arial 20 bold'), fill="white")
    scoretext = c.create_text(125, 50, text=f'Score: {score}', fill="gray71", font=('Arial 35 bold'))
    leveltext = c.create_text(125, 120, text=f'Level: {level}', fill="gray71", font=('Arial 35 bold'))


    player = Player(100, 100, 120, 60, "white")
    Obstacle()
    Obstacle()
    Obstacle()
    Obstacle()


def game_over():
    global game_state, play_button
    game_state = GAME_OVER
    c.delete("all")


    c.create_text(960, 400, text="Game Over", font=('Arial 35 bold'), fill="white")  # Adjusted y-coordinate
    scoretext = c.create_text(960, 300, text=f'Score: {score}', fill="deep sky blue", font=('Arial 35 bold'))
    leveltext = c.create_text(960, 200, text=f'Level: {level-1}', fill="deep sky blue", font=('Arial 35 bold'))


    play_button = ctk.CTkButton(tk, text="Play", command=start_game, corner_radius=20, bg_color="grey8")
    play_button.place(relx=0.5, rely=0.5, anchor=CENTER)


class Player():
    def __init__(self, x1, y1, x2, y2, color):
        global playercoords
        self.player = c.create_rectangle(x1, y1, x2, y2, fill=color)
        playercoords = c.bbox(self.player)
        self.vy = 0  
        self.jump_power = 13
        self.gravity = 0.7  
        self.ground = 1000
        self.jumpcount = 0
        self.crouching = False
        self.jumping = False
        tk.bind("<space>", self.jump)
        tk.bind("<Button-1>", self.crouch)
        tk.bind("<Button-3>", self.uncrouch)
        self.jumpanimate()
        self.crouchanimate()
        self.uncrouchanimate()


    def jumpanimate(self):
        self.gravity_effect()
        tk.after(10, self.jumpanimate)


    def crouchanimate(self):
        tk.after(10, self.crouchanimate)


    def uncrouchanimate(self):
        tk.after(10, self.uncrouchanimate)


    def gravity_effect(self):
        x1c, y1c, x2c, y2c = c.coords(self.player)
        if y2c <= self.ground:  
            self.vy += self.gravity
            self.jumping = False
        elif y2c >= self.ground and not self.jumping:
            self.vy = 0  
            self.jumping = False  
            if level < 2:
                self.jumpcount = 1
            else:
                self.jumpcount = 2
            c.coords(self.player, x1c, self.ground - (y2c - y1c), x2c, self.ground)
        c.move(self.player, 0, self.vy)  


    def crouch(self, event):
        if not self.crouching:
            self.crouching = True
            x1, y1, x2, y2 = c.coords(self.player)
            c.coords(self.player, x1, y1+20, x2, y2)


    def uncrouch(self, event):
        if self.crouching:
            x1, y1, x2, y2 = c.coords(self.player)
            c.coords(self.player, x1, y1-20, x2, y2)
            self.crouching = False


    def jump(self, event):
        if not self.jumping and self.crouching == False and self.jumpcount > 0:
            self.jumping = True
            self.vy += -self.jump_power  
            self.jumpcount -= 1






class Obstacle():
    def __init__(self):
        self.x1, self.y1, self.x2, self.y2 = self.random_position()
        self.obstacle = c.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white")
        self.speed = 4
        self.speedup()
        self.obstacle_color()
        self.movement()
        tk.bind('q', self.quitmanually)


    def random_position(self):
        x1 = random.randint(1920, 2920)  # xpos
        y1 = random.randint(850, 1000)  # ypos
        x2 = x1 + random.randint(10, 50)  # width
        y2 = y1 + random.randint(10, 50)  # height
        return x1, y1, x2, y2
   
    def obstacle_color(self):
        randomnum = random.randint(0, 5)
        if randomnum == 1:
            c.itemconfig(self.obstacle, fill="SteelBlue1")
        elif randomnum == 2:
            c.itemconfig(self.obstacle, fill="pale green")
        elif randomnum == 3:
            c.itemconfig(self.obstacle, fill="yellow2")
        elif randomnum == 4:
            c.itemconfig(self.obstacle, fill="orange2")
        elif randomnum == 5:
            c.itemconfig(self.obstacle, fill="thistle3")  
   
    def quitmanually(self, event):
        game_over()


    def speedup(self):
        level = calculate_level(score)
        self.speed = 4 + 4 * level
        c.itemconfig(leveltext, text=f'Level: {level}')


    def movement(self):
        self.speedup()  
        if self.x1 > 0:
            self.x1 -= self.speed
            self.x2 -= self.speed
            c.coords(self.obstacle, self.x1, self.y1, self.x2, self.y2)
            self.check_collision()
            tk.after(10, self.movement)
        else:
            global score
            score += 1
            c.delete(self.obstacle)
            c.itemconfig(scoretext, text=f'Score: {score}')
            Obstacle()


    def check_collision(self):
        obstacle_coords = c.bbox(self.obstacle)
        player_coords = c.bbox(player.player)
        if (obstacle_coords[0] < player_coords[2] < obstacle_coords[2] or obstacle_coords[0] < player_coords[0] < obstacle_coords[2]) and \
           (obstacle_coords[1] < player_coords[3] < obstacle_coords[3] or obstacle_coords[1] < player_coords[1] < obstacle_coords[3]):
            game_over()


    def debug(self):
        print(c.coords(self.obstacle))
        print(playercoords)


show_menu()


tk.mainloop()






