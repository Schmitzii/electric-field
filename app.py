import constants as c
import helpers as h
import tkinter as tk

# messagebox does not get imported automatically, so import it explicitly
from tkinter import messagebox


"""BUTTON FUCTIONS"""
add_charge = False
remove_charge = False

# apply method to create circle to tk.Canvas
tk.Canvas.create_circle = h._create_circle


def onClick_addCharge():
    global add_charge, remove_charge
    remove_charge = False

    if add_charge:
        add_charge = False
        addcharge_button.config(relief=tk.RAISED)
    else:
        add_charge = True
        addcharge_button.config(relief=tk.SUNKEN)
        removecharge_button.config(relief=tk.RAISED)


def onClick_removeCharge():
    global add_charge, remove_charge
    add_charge = False

    if remove_charge:
        remove_charge = False
        removecharge_button.config(relief=tk.RAISED)
    else:
        remove_charge = True
        removecharge_button.config(relief=tk.SUNKEN)
        addcharge_button.config(relief=tk.RAISED)


def onClick_inputField(event):
    x, y = event.x, event.y  # mouse click position
    if add_charge:
        if len(h.charges) > 9:
            messagebox.showerror(
                title="Zu viele Ladungen",
                message="Es können maximal 10 Ladungen eingefügt werden.",
            )
        else:
            q = canvas.create_circle(x, y, c.DEFAULT_CIRCLE_RADIUS, fill="red")
            coords = canvas.coords(q)
            # add new charge to charges array by calculating center coordinates of circle
            h.charges.append(
                h.Charge(
                    1, [(coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2], q
                )
            )
            print(h.charges[-1].__dict__)  # print out object attributes
    elif not add_charge and not remove_charge:
        for q in h.charges:  # loop through to charges to check if item was clicked
            coords = canvas.coords(q[2])
            if (
                coords[0] < x < coords[2] and coords[1] < y < coords[3]
            ):  # check if mouse click was inside the item
                pass


"""HIER WEITER MACHEN(KREIS HINZUFÜGEN UND GRÖßEN-TOGGLER)"""


"""ROOT"""
root = tk.Tk()  # initialise root element
root.title("Visualisierung elektrischer Feldlinien")  # set title
root.geometry("1200x800")  # set window size

"""MENU"""
menubar = tk.Menu(root)  # initialise menubar

optionsmenu = tk.Menu(menubar)
optionsmenu.add_command(label="Einstellungen löschen")
optionsmenu.add_command(label="Schließen", command=root.quit)

viewmenu = tk.Menu(menubar)
viewmenu.add_command(label="Einstellungen")
viewmenu.add_command(label="Darstellung")

menubar.add_cascade(label="Optionen", menu=optionsmenu)
menubar.add_cascade(label="Ansicht", menu=viewmenu)

root.config(menu=menubar, bg=c.BACKGROUND_COLOR)

"""WINDOW"""
window_f = tk.LabelFrame(
    root, text="Visualisierung elektrischer Feldlinien", padx=10, pady=10
)
window_f.pack(padx=10, pady=10)  # add padding to inside of frame

"""PLOT"""
plot_f = tk.Frame(window_f)
buttons_f = tk.Frame(plot_f)

# Buttons
cursor_button = tk.Button(buttons_f, text="Cursor", width=c.BUTTON_WIDTH)
addcharge_button = tk.Button(
    buttons_f, text="Ladung hinzufügen", width=c.BUTTON_WIDTH, command=onClick_addCharge
)
removecharge_button = tk.Button(
    buttons_f,
    text="Ladung entfernen",
    width=c.BUTTON_WIDTH,
    command=onClick_removeCharge,
)
efield_button = tk.Button(buttons_f, text="Elektrisches Feld", width=c.BUTTON_WIDTH)
cursor_button.grid(row=0, column=0)
addcharge_button.grid(row=0, column=1)
removecharge_button.grid(row=0, column=2)
efield_button.grid(row=0, column=3)

# Input Field
canvas = tk.Canvas(plot_f, width=c.PLOT_SIZE, height=c.PLOT_SIZE)
input_field = canvas.create_rectangle(0, 0, c.PLOT_SIZE, c.PLOT_SIZE, fill="white")
canvas.tag_bind(input_field, "<Button-1>", onClick_inputField)

buttons_f.grid(column=0, row=0)
canvas.grid(column=0, row=1)

window_f.pack()
plot_f.pack()


root.mainloop()
