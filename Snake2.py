import sys
import tkinter as tk

# variables

window_height = 400
window_width = 2 * window_height
block_size = 20
y_tiles = window_height/block_size
x_tiles = window_width/block_size


mainWindow = tk.Tk()

l = tk.Label(mainWindow, text="Hello, World!")
l.pack()

w = tk.Canvas(mainWindow, width=window_width, height=window_height, borderwidth=0, highlightthickness=0, relief='ridge', background='black')

for x in range(0, int(window_width / block_size)):
    for y in range(0, int(window_height / block_size)):
        block_color = '#%02x%02x%02x' % (0, 20+y*2, 20+x*1)
        w.create_rectangle(x*block_size, y*block_size, x*block_size+block_size, y*block_size+block_size, fill=block_color, outline='')

w.pack()


mainWindow.mainloop()

