import tkinter as tk
import math
import random
from datetime import datetime

# Base list of 24 ancient Egyptian symbols (one for each hour)
base_hour_markers24 = [
    "𓀀", "𓀁", "𓀂", "𓀃", "𓀄", "𓀅", "𓀆", "𓀇",
    "𓀈", "𓀉", "𓀊", "𓀋", "𓀌", "𓀍", "𓀎", "𓀏",
    "𓀐", "𓀑", "𓀒", "𓀓", "𓀔", "𓀕", "𓀖", "𓀗"
]

# Define 10 different themes for our clocks
themes = [
    {"bg": "black",    "face": "gold",    "hour_hand": "gold",   "minute_hand": "white",  "second_hand": "red",     "marker": "gold",    "center": "gold"},
    {"bg": "#001f3f",  "face": "silver",  "hour_hand": "silver", "minute_hand": "white",  "second_hand": "cyan",    "marker": "silver",  "center": "silver"},
    {"bg": "#800000",  "face": "#cd7f32", "hour_hand": "#cd7f32", "minute_hand": "white", "second_hand": "orange",  "marker": "#cd7f32", "center": "#cd7f32"},
    {"bg": "#013220",  "face": "#50c878", "hour_hand": "#50c878", "minute_hand": "#90ee90", "second_hand": "lime",  "marker": "#50c878", "center": "#50c878"},
    {"bg": "purple",   "face": "magenta", "hour_hand": "magenta", "minute_hand": "white",  "second_hand": "pink",    "marker": "magenta", "center": "magenta"},
    {"bg": "darkgray", "face": "lightgray", "hour_hand": "white",  "minute_hand": "lightblue", "second_hand": "red",   "marker": "lightgray", "center": "white"},
    {"bg": "navy",     "face": "gold",    "hour_hand": "gold",   "minute_hand": "white",  "second_hand": "red",     "marker": "gold",    "center": "gold"},
    {"bg": "black",    "face": "red",     "hour_hand": "red",    "minute_hand": "orange", "second_hand": "yellow",  "marker": "red",     "center": "red"},
    {"bg": "#654321",  "face": "#d2b48c", "hour_hand": "tan",    "minute_hand": "white",  "second_hand": "orange",  "marker": "tan",     "center": "tan"},
    {"bg": "#191970",  "face": "silver",  "hour_hand": "silver", "minute_hand": "lightblue", "second_hand": "cyan",  "marker": "silver",  "center": "silver"}
]

class Egyptian24Clock:
    def __init__(self, master, size=200, markers=None, theme=None):
        self.size = size
        self.center = (size / 2, size / 2)
        self.radius = size * 0.45
        self.theme = theme if theme else {
            "bg": "black", "face": "gold", "hour_hand": "gold",
            "minute_hand": "white", "second_hand": "red",
            "marker": "gold", "center": "gold"
        }
        # Use a shuffled copy of the 24 markers for a unique clock
        self.hour_markers = markers if markers else base_hour_markers24.copy()

        # Create the canvas with the theme's background color
        self.canvas = tk.Canvas(master, width=size, height=size, bg=self.theme["bg"], highlightthickness=0)
        self.canvas.pack()

        # Draw the clock face with 24 hour markers
        self.draw_face()

        # Create clock hands
        self.hour_hand = self.canvas.create_line(self.center[0], self.center[1],
                                                  self.center[0], self.center[1] - self.radius * 0.5,
                                                  width=4, fill=self.theme["hour_hand"])
        self.minute_hand = self.canvas.create_line(self.center[0], self.center[1],
                                                    self.center[0], self.center[1] - self.radius * 0.7,
                                                    width=3, fill=self.theme["minute_hand"])
        self.second_hand = self.canvas.create_line(self.center[0], self.center[1],
                                                    self.center[0], self.center[1] - self.radius * 0.8,
                                                    width=2, fill=self.theme["second_hand"])

        # Center decorative symbol (updates with current hour)
        self.center_text = self.canvas.create_text(self.center[0], self.center[1],
                                                   text="",
                                                   font=("Segoe UI Historic", int(size / 5)),
                                                   fill=self.theme["center"])
        self.update_center_symbol()

    def draw_face(self):
        # Outer circle
        self.canvas.create_oval(self.center[0] - self.radius, self.center[1] - self.radius,
                                self.center[0] + self.radius, self.center[1] + self.radius,
                                outline=self.theme["face"], width=3)
        # 24 hour markers arranged around the circle
        for i in range(24):
            angle = math.pi/2 - (i * 2 * math.pi / 24)
            x = self.center[0] + math.cos(angle) * self.radius * 0.85
            y = self.center[1] - math.sin(angle) * self.radius * 0.85
            self.canvas.create_text(x, y,
                                    text=self.hour_markers[i],
                                    font=("Segoe UI Historic", int(self.size / 12)),
                                    fill=self.theme["marker"])

    def update_center_symbol(self):
        # Display the symbol corresponding to the current hour in the center
        now = datetime.now()
        hour = now.hour  # 0-23
        symbol = self.hour_markers[hour]
        self.canvas.itemconfig(self.center_text, text=symbol)

    def update(self):
        # Update clock hands based on current 24-hour time
        now = datetime.now()
        hours = now.hour
        minutes = now.minute
        seconds = now.second

        hour_angle = math.pi/2 - ((hours + minutes/60.0 + seconds/3600.0) * (2 * math.pi / 24))
        minute_angle = math.pi/2 - ((minutes + seconds/60.0) * (2 * math.pi / 60))
        second_angle = math.pi/2 - (seconds * (2 * math.pi / 60))

        hour_x = self.center[0] + math.cos(hour_angle) * self.radius * 0.5
        hour_y = self.center[1] - math.sin(hour_angle) * self.radius * 0.5

        minute_x = self.center[0] + math.cos(minute_angle) * self.radius * 0.7
        minute_y = self.center[1] - math.sin(minute_angle) * self.radius * 0.7

        second_x = self.center[0] + math.cos(second_angle) * self.radius * 0.8
        second_y = self.center[1] - math.sin(second_angle) * self.radius * 0.8

        self.canvas.coords(self.hour_hand, self.center[0], self.center[1], hour_x, hour_y)
        self.canvas.coords(self.minute_hand, self.center[0], self.center[1], minute_x, minute_y)
        self.canvas.coords(self.second_hand, self.center[0], self.center[1], second_x, second_y)

        self.update_center_symbol()

def update_all():
    for clock in clocks:
        clock.update()
    root.after(1000, update_all)

# Main window setup
root = tk.Tk()
root.title("10 Different 24‑Hour Egyptian Clocks (Compact Edition)")

frame = tk.Frame(root, bg="black")
frame.pack(padx=10, pady=10)

clocks = []
num_clocks = 10
rows = 2
cols = 5
clock_size = 300  # Compact size for a 1024x768 window

# Arrange 10 clocks in a 2x5 grid
for i in range(num_clocks):
    r = i // cols
    c = i % cols
    clock_frame = tk.Frame(frame, bg=themes[i]["bg"])
    clock_frame.grid(row=r, column=c, padx=5, pady=5)
    markers = base_hour_markers24.copy()
    random.shuffle(markers)
    clock = Egyptian24Clock(clock_frame, size=clock_size, markers=markers, theme=themes[i])
    clocks.append(clock)

update_all()
root.mainloop()
