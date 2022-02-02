import constants as c
import helpers as h
import tkinter as tk

# does not get imported automatically, so import it explicitly
from tkinter import HORIZONTAL, messagebox
from tkinter import simpledialog
from tkinter import ttk

# apply method to create circle to tk.Canvas
tk.Canvas.create_circle = h._create_circle

"""PROGRAM DOESNT WORK WHEN THERE ARE MORE POSITIVE THAN NEGATIVE CHARGES"""


class App():
    def __init__(self, parent):
        """VARIABLES"""
        self.add_charge = False
        self.remove_charge = False
        self.counter = 0  # counts the number of charges

        """ROOT"""
        self.parent = parent
        self.parent.geometry("1200x800")
        self.parent.title("Visualisierung elektrischer Feldlinien")

        self.parent.title(
            "Visualisierung elektrischer Feldlinien")  # set title
        self.parent.geometry("1200x800")  # set window size

        """MENU"""
        self.menubar = tk.Menu(self.parent)  # initialise menubar

        self.optionsmenu = tk.Menu(self.menubar)
        self.optionsmenu.add_command(label="Einstellungen löschen")
        self.optionsmenu.add_command(
            label="Schließen", command=self.parent.quit)

        self.viewmenu = tk.Menu(self.menubar)
        self.viewmenu.add_command(label="Einstellungen")
        self.viewmenu.add_command(label="Darstellung")

        self.menubar.add_cascade(label="Optionen", menu=self.optionsmenu)
        self.menubar.add_cascade(label="Ansicht", menu=self.viewmenu)

        self.parent.config(menu=self.menubar, bg=c.BACKGROUND_COLOR)

        """WINDOW"""
        self.window_f = tk.LabelFrame(
            self.parent, text="Visualisierung elektrischer Feldlinien", padx=10, pady=10
        )
        self.window_f.pack(padx=10, pady=10)  # add padding to inside of frame

        """PLOT"""
        self.plot_f = tk.Frame(self.window_f)
        self.buttons_f = tk.Frame(self.plot_f)
        self.sliders_f = tk.Frame(self.plot_f)

        # Buttons
        self.cursor_button = tk.Button(
            self.buttons_f, text="Cursor", width=c.BUTTON_WIDTH)
        self.addcharge_button = tk.Button(
            self.buttons_f, text="Ladung hinzufügen", width=c.BUTTON_WIDTH, command=self.onClick_addCharge
        )
        self.removecharge_button = tk.Button(
            self.buttons_f,
            text="Ladung entfernen",
            width=c.BUTTON_WIDTH,
            command=self.onClick_removeCharge,
        )
        self.efield_button = tk.Button(
            self.buttons_f, text="Elektrisches Feld", width=c.BUTTON_WIDTH, command=self.onClick_eField
        )
        self.cursor_button.grid(row=0, column=0)
        self.addcharge_button.grid(row=0, column=1)
        self.removecharge_button.grid(row=0, column=2)
        self.efield_button.grid(row=0, column=3)

        # Input Field
        self.canvas = tk.Canvas(
            self.plot_f, width=c.PLOT_SIZE, height=c.PLOT_SIZE)
        self.input_field = self.canvas.create_rectangle(
            0, 0, c.PLOT_SIZE, c.PLOT_SIZE, fill="white")
        self.canvas.tag_bind(
            self.input_field, "<Button-1>", self.onClick_inputField)

        # Sliders
        self.density_slider = tk.Scale(
            self.sliders_f, from_=0.0, to=2.0, digits=2, resolution=0.1, orient=HORIZONTAL, label="Feldliniendichte")
        self.density_slider.set(1.0)  # set Default Value of Slider
        self.density_slider.grid(row=0, column=0)

        self.buttons_f.grid(column=0, row=0)
        self.canvas.grid(column=0, row=1)
        self.sliders_f.grid(column=0, row=2)

        self.window_f.pack()
        self.plot_f.grid(row=0, column=0)

        """TABLE"""
        self.table = ttk.Treeview(self.window_f, height=29)
        self.table['columns'] = ('position', 'charge')

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("position", anchor=tk.CENTER, width=80)
        self.table.column("charge", anchor=tk.CENTER, width=80)

        self.table.heading("#0", text="", anchor=tk.CENTER)
        self.table.heading("position", text="Position", anchor=tk.CENTER)
        self.table.heading("charge", text="Ladung", anchor=tk.CENTER)

        self.table.grid(row=0, column=1)

        self.table.bind('<Double-Button-1>', self.select_item)

    """BUTTON FUCTIONS"""

    def onClick_addCharge(self):
        self.remove_charge = False

        if self.add_charge:
            self.add_charge = False
            self.addcharge_button.config(relief=tk.RAISED)
        else:
            self.add_charge = True
            self.addcharge_button.config(relief=tk.SUNKEN)
            self.removecharge_button.config(relief=tk.RAISED)

    def onClick_removeCharge(self):
        self.add_charge = False

        if self.remove_charge:
            self.remove_charge = False
            self.removecharge_button.config(relief=tk.RAISED)
        else:
            self.remove_charge = True
            self.removecharge_button.config(relief=tk.SUNKEN)
            self.addcharge_button.config(relief=tk.RAISED)

    def onClick_eField(self):
        h.eField(density=self.density_slider.get())

    def onClick_inputField(self, event):
        x, y = event.x, event.y  # mouse click position

        if self.add_charge:
            if len(h.charges) > 9:
                messagebox.showerror(
                    title="Zu viele Ladungen",
                    message="Es können maximal 10 Ladungen eingefügt werden.",
                )
            else:
                q = self.canvas.create_circle(
                    x, y, c.DEFAULT_CIRCLE_RADIUS, fill="red")
                coords = self.canvas.coords(q)
                self.canvas.tag_bind(q, "<Button-1>", self.onClick_charge)
                # add new charge to charges array by calculating center coordinates of circle
                h.charges.append(
                    h.Charge(
                        1.0, [round((coords[0] + coords[2]) / 1200, 2),  # divided by 1200 because /2 because of average and /600 because of coordinate system
                              round(1 - ((coords[1] + coords[3]) / 1200), 2)], q, None
                    )
                )
                record = self.table.insert(parent="", index="end", iid=self.counter, text="", values=(
                    h.charges[-1].pos, h.charges[-1].q))  # [-1] takes the last element of an array
                # add table record to object to be able to delete it
                h.charges[-1].record = record
                self.counter += 1
                # print out object attributes
                print(h.charges[-1].__dict__)

    def onClick_charge(self, event):
        global counter
        x, y = event.x, event.y  # mouse click position

        q = event.widget.find_closest(x, y)
        if self.remove_charge:
            for charge in h.charges:
                # check if charge in array has same coordinates as clicked charge
                if self.canvas.coords(charge.item) == self.canvas.coords(q):
                    self.canvas.delete(q)
                    h.charges.remove(charge)
                    self.table.delete(charge.record)
        elif not self.remove_charge and not self.add_charge:  # select charge to change values
            pass

    def select_item(self, a):  # argument a not used but is necessary
        curItem = self.table.focus()
        values = self.table.item(curItem, 'values')
        user_inp = simpledialog.askfloat(
            "Änderung der Ladung", "Neuer Wert:", minvalue=-10.0, maxvalue=10.0)
        if user_inp is not None:
            self.table.item(curItem, values=(values[0], user_inp))
            for charge in h.charges:
                # check if record of charge equals focused record
                if curItem == charge.record:
                    charge.q = user_inp
                    # change color based on mathematical operator (<0:blue, =0:grey, >0:red)
                    self.canvas.itemconfig(charge.item, fill='blue') if user_inp < 0 else self.canvas.itemconfig(
                        charge.item, fill='grey') if user_inp == 0 else self.canvas.itemconfig(charge.item, fill='red')
                    # PLACEHOLDER FOR CHANGING SIZE OF OVAL WHEN CHARGE GETS BIGGER OR SMALLER


root = tk.Tk()  # initialise root element
window = App(root)
root.mainloop()
