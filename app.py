import constants as c
import tkinter as tk
from helpers import *

"""ROOT"""
root = tk.Tk()  # initialise root element
root.title('Visualisierung elektrischer Feldlinien')
root.geometry("1200x800")

"""MENU"""
menubar = tk.Menu(root)

optionsmenu = tk.Menu(menubar)
optionsmenu.add_command(label="Einstellungen löschen", command=clear)
optionsmenu.add_command(label="Schließen", command=root.quit)

viewmenu = tk.Menu(menubar)
viewmenu.add_command(label="Einstellungen")
viewmenu.add_command(label="Darstellung")

menubar.add_cascade(label="Optionen", menu=optionsmenu)
menubar.add_cascade(label="Ansicht", menu=viewmenu)

root.config(menu=menubar, bg=c.BACKGROUND_COLOR)

"""WINDOW"""
window_f = tk.LabelFrame(
    root, text="Visualisierung elektrischer Feldlinien", padx=10, pady=10)
window_f.pack(padx=10, pady=10)

"""SETTINGS"""
plot_f = tk.Frame(window_f)
buttons_f = tk.Frame(plot_f)

# Buttons
cursor_button = tk.Button(buttons_f, text="Cursor", width=c.BUTTON_WIDTH)
addcharge_button = tk.Button(
    buttons_f, text="Ladung hinzufügen", width=c.BUTTON_WIDTH)
removecharge_button = tk.Button(
    buttons_f, text="Ladung entfernen", width=c.BUTTON_WIDTH)
efield_button = tk.Button(
    buttons_f, text="Elektrisches Feld", width=c.BUTTON_WIDTH)
cursor_button.grid(row=0, column=0)
addcharge_button.grid(row=0, column=1)
removecharge_button.grid(row=0, column=2)
efield_button.grid(row=0, column=3)

# Input Field
canvas = tk.Canvas(plot_f, width=c.PLOT_SIZE, height=c.PLOT_SIZE)
input_field = canvas.create_rectangle(
    0, 0, c.PLOT_SIZE, c.PLOT_SIZE, fill='white')

buttons_f.grid(column=0, row=0)
canvas.grid(column=0, row=1)


window_f.pack()
plot_f.pack()


root.mainloop()
