import tkinter as tk
import math

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Getting Over It")
        self.geometry("800x600")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, bg="white", width=800, height=600)
        self.canvas.pack()

        self.player_radius = 20
        self.player = self.canvas.create_oval(390, 290, 410, 310, fill="blue")
        
        self.hammer_length = 100
        self.hammer_angle = 0
        self.hammer = self.canvas.create_line(400, 300, 400 + self.hammer_length, 300, width=5)
        
        self.bind("<Motion>", self.update_hammer)
        self.bind("<Button-1>", self.apply_force)
        
        self.gravity = 0.5
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_grounded = False

        self.update_game()
        
    def update_hammer(self, event):
        x, y = self.canvas.coords(self.player)[:2]
        angle = math.atan2(event.y - y, event.x - x)
        self.hammer_angle = angle
        self.canvas.coords(self.hammer, x + 10, y + 10, x + 10 + self.hammer_length * math.cos(angle), y + 10 + self.hammer_length * math.sin(angle))

    def apply_force(self, event):
        if self.is_grounded:
            force = 10
            self.velocity_x -= force * math.cos(self.hammer_angle)
            self.velocity_y -= force * math.sin(self.hammer_angle)
            self.is_grounded = False

    def update_game(self):
        self.velocity_y += self.gravity
        
        x0, y0, x1, y1 = self.canvas.coords(self.player)
        new_x0 = x0 + self.velocity_x
        new_y0 = y0 + self.velocity_y
        new_x1 = x1 + self.velocity_x
        new_y1 = y1 + self.velocity_y
        
        if new_y1 >= 600:
            self.is_grounded = True
            self.velocity_y = 0
            new_y0 = 600 - self.player_radius * 2
            new_y1 = 600
            
        if new_x0 <= 0 or new_x1 >= 800:
            self.velocity_x = -self.velocity_x

        self.canvas.coords(self.player, new_x0, new_y0, new_x1, new_y1)
        self.canvas.coords(self.hammer, new_x0 + 10, new_y0 + 10, new_x0 + 10 + self.hammer_length * math.cos(self.hammer_angle), new_y0 + 10 + self.hammer_length * math.sin(self.hammer_angle))

        self.after(16, self.update_game)

if __name__ == "__main__":
    game = Game()
    game.mainloop()
