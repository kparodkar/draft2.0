import tkinter as tk
from tkinter import ttk
import colorsys
import random

class ColorPicker(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Pick a Color")
        self.callback = callback
        self.colors = ["#000000", "#FAFA33", "#0047AB", "#90EE90", "#FFFFFF", "#FF0000", "#006400", "#E97451", "#CB9D06", "#003153", "#E34234", "#FFA700"]
        
        self.create_widgets()

    def create_widgets(self):
        self.color_frame = tk.Frame(self)
        self.color_frame.pack()

        self.brightness_frame = tk.Frame(self)
        self.brightness_frame.pack()

        # Create color buttons
        for color in self.colors:
            button = tk.Button(self.color_frame, bg=color, width=3, command=lambda c=color: self.callback(c, self.brightness_scale.get()))
            button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create brightness slider with increased size
        self.brightness_label1 = tk.Label(self.brightness_frame, text="Darker")
        self.brightness_label1.pack(side=tk.LEFT, padx=5)
        self.brightness_scale = tk.Scale(self.brightness_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Brightness", command=self.update_color_brightness, length=300)
        self.brightness_scale.pack(side=tk.LEFT)
        self.brightness_label2 = tk.Label(self.brightness_frame, text="Lighter")
        self.brightness_label2.pack(side=tk.LEFT, padx=5)

    def update_color_brightness(self, value):
        pass  # Implement brightness adjustment if needed

class ColorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Color Chooser App")
        self.geometry("550x350")

        self.color1 = "#FFFFFF"  # Initial color for color1 (white)
        self.color2 = "#FFFFFF"  # Initial color for color2 (white)

        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.pack(side=tk.TOP, padx=10)

        self.color1_square = self.canvas.create_rectangle(250, 50, 400, 150, fill=self.color1, outline='black', width=2)
        self.color2_square = self.canvas.create_rectangle(50, 50, 200, 150, fill=self.color2, outline='black', width=2)
        self.slider_pos = self.canvas.create_oval(250, 180, 260, 190, fill="red")  # Initial position of slider

        self.canvas.tag_bind(self.color1_square, "<Button-1>", lambda event: self.pick_color1())
        self.canvas.tag_bind(self.color2_square, "<Button-1>", lambda event: self.pick_color2())
        self.canvas.tag_bind(self.slider_pos, "<Button-1>", lambda event: self.move_slider(event))
        self.bind("<ButtonRelease-1>", self.release_slider)

        self.generate_random_color_button = tk.Button(self, text="Generate Random Color", command=self.generate_random_color)
        self.generate_random_color_button.pack(pady=10)

        self.selected_color_square = tk.Canvas(self, width=100, height=100)
        self.selected_color_square.pack(side=tk.LEFT, padx=10)

        self.update_selected_color()

    def pick_color1(self):
        self.show_color_dialog(self.set_color1)

    def pick_color2(self):
        self.show_color_dialog(self.set_color2)

    def set_color1(self, color, brightness):
        self.color1 = self.adjust_brightness(color, brightness)
        self.canvas.itemconfig(self.color1_square, fill=self.color1)
        self.update_mixed_color()
        self.update_selected_color()

    def set_color2(self, color, brightness):
        self.color2 = self.adjust_brightness(color, brightness)
        self.canvas.itemconfig(self.color2_square, fill=self.color2)
        self.update_mixed_color()
        self.update_selected_color()

    def adjust_brightness(self, color, brightness):
        # Convert hex color to RGB
        rgb_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

        # Convert RGB to HSL
        h, l, s = colorsys.rgb_to_hls(*rgb_color)

        # Adjust brightness (lightness)
        l = l * (brightness / 100)

        # Convert HSL back to RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)

        # Convert RGB to hex color
        hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"

        return hex_color

    def show_color_dialog(self, callback):
        dialog = ColorPicker(self, callback)

    def update_mixed_color(self):
        percent1 = 50  # Example: 50% of color1
        percent2 = 50  # Example: 50% of color2
        mixed_color = self.mix_colors(self.color1, self.color2, percent1, percent2)
        self.canvas.itemconfig(self.slider_pos, fill=mixed_color)
        self.update_selected_color()

    def mix_colors(self, color1, color2, percent1, percent2):
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

    def generate_random_color(self):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.selected_color_square.config(bg=color)
        self.update_selected_color()

    def update_selected_color(self):
        color = self.selected_color_square.cget("bg")
        self.selected_color_square.delete("all")
        self.selected_color_square.create_rectangle(0, 0, 100, 100, fill=color)

    def move_slider(self, event):
        x, y = event.x, event.y
        if 250 <= x <= 260 and 180 <= y <= 190:
            self.canvas.bind("<Motion>", self.slide_color)
    
    def slide_color(self, event):
        x = event.x
        if x < 250:
            x = 250
        elif x > 350:
            x = 350
        self.canvas.coords(self.slider_pos, x, 180, x + 10, 190)
        percent1 = (x - 250) / 100
        percent2 = 1 - percent1
        mixed_color = self.mix_colors(self.color1, self.color2, percent1, percent2)
        self.selected_color_square.config(bg=mixed_color)

    def release_slider(self, event):
        self.canvas.unbind("<Motion>")
        

if __name__ == "__main__":
    app = ColorApp()
    app.mainloop()
