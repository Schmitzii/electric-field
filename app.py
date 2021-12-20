import constants as c
import helpers as h
import tkinter as tk

# does not get imported automatically, so import it explicitly
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk


"""BUTTON FUCTIONS"""
add_charge = False
remove_charge = False
counter = 0  # counts the number of charges

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
    global counter
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
            canvas.tag_bind(q, "<Button-1>", onClick_charge)
            # add new charge to charges array by calculating center coordinates of circle
            h.charges.append(
                h.Charge(
                    1, [(coords[0] + coords[2]) / 2,
                        (coords[1] + coords[3]) / 2], q, None
                )
            )
            record = table.insert(parent="", index="end", iid=counter, text="", values=(
                h.charges[-1].pos, h.charges[-1].q))  # [-1] takes the last element of an array
            # add table record to object to be able to delete it
            h.charges[-1].record = record
            counter += 1
            print(h.charges[-1].__dict__)  # print out object attributes
    else:
        pass


def onClick_charge(event):
    global counter
    x, y = event.x, event.y  # mouse click position

    q = event.widget.find_closest(x, y)
    if remove_charge:
        for charge in h.charges:
            # check if charge in array has same coordinates as clicked charge
            if canvas.coords(charge.item) == canvas.coords(q):
                canvas.delete(q)
                h.charges.remove(charge)
                table.delete(charge.record)


def select_item():  # hier weiter machen, rest müssen funktionieren(PopUp-Fenster öffnet sich automatisch)
    curItem = table.focus()
    user_inp = simpledialog.askfloat(  # führt automatisch aus
        "Änderung der Ladung", "Neuer Wert:", minvalue=-10.0, maxvalue=10.0)
    # keine Möglichkeit um value des items abzurufen
    table.item(curItem, values=(curItem[0], user_inp))


"""ROOT"""
root = tk.Tk()  # initialise root element #vielleicht App-Klasse erstellen und Funktionen für bessere Lesbarkeit außerhalb definieren
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
efield_button = tk.Button(
    buttons_f, text="Elektrisches Feld", width=c.BUTTON_WIDTH)
cursor_button.grid(row=0, column=0)
addcharge_button.grid(row=0, column=1)
removecharge_button.grid(row=0, column=2)
efield_button.grid(row=0, column=3)

# Input Field
canvas = tk.Canvas(plot_f, width=c.PLOT_SIZE, height=c.PLOT_SIZE)
input_field = canvas.create_rectangle(
    0, 0, c.PLOT_SIZE, c.PLOT_SIZE, fill="white")
canvas.tag_bind(input_field, "<Button-1>", onClick_inputField)

buttons_f.grid(column=0, row=0)
canvas.grid(column=0, row=1)

window_f.pack()
plot_f.grid(row=0, column=0)

"""TABLE"""
table = ttk.Treeview(window_f, height=29)
table['columns'] = ('position', 'charge')

table.column("#0", width=0, stretch=tk.NO)
table.column("position", anchor=tk.CENTER, width=80)
table.column("charge", anchor=tk.CENTER, width=80)

table.heading("#0", text="", anchor=tk.CENTER)
table.heading("position", text="Position", anchor=tk.CENTER)
table.heading("charge", text="Ladung", anchor=tk.CENTER)

table.grid(row=0, column=1)

table.bind('<Button-1>', select_item)


root.mainloop()
