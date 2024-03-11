from PIL import Image, ImageTk
import tkinter as tk
import random
from src.service.art_canvas import Canvas
# Here what you are gonna cook
from src.service.arts.sixteen_segment import get, n_type


def display_selected_pixels(selected_type):
    # Get the selected set's RGB pixel values, width, and height
    print("Display type :", selected_type)
    canvas = get(selected_type)
    scale = 6
    
    # Create a new image with the specified width and height
    img = Image.new('RGB', (canvas.width, canvas.height))
    rgb_pixels = [(0, 255, 255) if canvas.get_pixel(x, y) == 1 else (0, 0, 0) for y in range(canvas.height) for x in range(canvas.width)]
    img.putdata(rgb_pixels)
    img = img.resize((canvas.width * scale, canvas.height * scale), Image.NEAREST)

    # Convert PIL image to Tkinter PhotoImage
    tk_img = ImageTk.PhotoImage(img)
    
    # Create a label to display the image
    label.config(image=tk_img)
    label.image = tk_img

selected_type = 0

def on_prev_click():
    global selected_type
    print("on_prev_click")
    selected_type = max(0, selected_type - 1)
    display_selected_pixels(selected_type)

def on_random():
    global selected_type
    print("on_prev_click")
    selected_type = random.randint(0, n_type - 1)
    display_selected_pixels(selected_type)

def on_next_click():
    global selected_type
    print("on_next_click")
    selected_type = min(n_type - 1, selected_type + 1)
    display_selected_pixels(selected_type)

# Create a Tkinter window
window = tk.Tk()
window.title("Canvas Sim")

label = tk.Label(window)
display_selected_pixels(0)
label.pack()

button_prev = tk.Button(window, text="<-", command=on_prev_click)
button_prev.pack(side=tk.LEFT)
button_next = tk.Button(window, text="Rand", command=on_random)
button_next.pack(side=tk.BOTTOM)
button_next = tk.Button(window, text="->", command=on_next_click)
button_next.pack(side=tk.RIGHT)

# Run the Tkinter event loop
window.mainloop()