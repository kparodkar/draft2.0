import tkinter as tk
import random

def mix_colors(color1, color2, percent1, percent2):
    # Check if color strings are empty
    if not color1 or not color2:
        return "#FFFFFF"  # Return white if either color is not provided

    # Convert percentages to ratios
    total_percent = percent1 + percent2
    ratio1 = percent1 / total_percent
    ratio2 = percent2 / total_percent

    # Extract RGB values from color strings
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    # Interpolate RGB values based on the ratios
    r = int(r1 * ratio1 + r2 * ratio2)
    g = int(g1 * ratio1 + g2 * ratio2)
    b = int(b1 * ratio1 + b2 * ratio2)

    # Convert interpolated RGB values to hexadecimal format
    mixed_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    return mixed_color

class ColorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Color Chooser App")
        self.geometry("550x700")

        self.color1 = None
        self.color2 = None

        self.create_color_palette()

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(side=tk.TOP, padx=70)

        self.color1_square = self.canvas.create_rectangle(50, 50, 150, 150, outline='black', width=2)
        self.color2_square = self.canvas.create_rectangle(250, 50, 350, 150, outline='black', width=2)
        self.mixed_color_square = self.canvas.create_rectangle(100, 200, 300, 350, outline='black', width=2)

        self.random_color_canvas = tk.Canvas(self, width=400, height=50)
        self.random_color_canvas.pack(side=tk.TOP, padx=10, pady=10)

        self.display_random_colors()

    def create_color_palette(self):
        self.color_palette_frame = tk.Frame(self)
        self.color_palette_frame.pack()

        self.colors = ['#FF5733', '#33FF57', '#5733FF', '#FFD133', '#33FFF5', '#F533FF', '#33FFAA', '#AA33FF', '#FFAA33', '#AAFF33', '#33FF57', '#5733FF']
        for color in self.colors:
            button = tk.Button(self.color_palette_frame, bg=color, width=3, command=lambda c=color: self.set_selected_color(c))
            button.pack(side=tk.LEFT, padx=5, pady=5)

    def set_selected_color(self, color):
        if self.color1 is None:
            self.color1 = color
            self.canvas.itemconfig(self.color1_square, fill=self.color1)
        elif self.color2 is None:
            self.color2 = color
            self.canvas.itemconfig(self.color2_square, fill=self.color2)
            self.update_mixed_color()

    def update_mixed_color(self):
        if self.color1 is not None and self.color2 is not None:
            percent1 = 50  # Example: 50% of color1
            percent2 = 50  # Example: 50% of color2
            mixed_color = mix_colors(self.color1, self.color2, percent1, percent2)
            self.canvas.itemconfig(self.mixed_color_square, fill=mixed_color)

    def display_random_colors(self):
        random_colors = ['#A020F0', '#0D98BA', '#adff2f']
        random_color = random.choice(random_colors)
        self.random_color_canvas.create_rectangle(150, 10, 250, 50, fill=random_color, outline='black')

if __name__ == "__main__":
    app = ColorApp()
    app.mainloop()
