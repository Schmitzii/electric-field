import constants as c
import helpers as h
import tkinter as tk

# wird nicht automatisch importiert, also explizit importieren
from tkinter import HORIZONTAL, messagebox
from tkinter import simpledialog
from tkinter import ttk

# eigene Methode, um Kreis zu erstellen, da sonst Probleme mit Koordinaten auftreten
tk.Canvas.create_circle = h._create_circle


class App():
    def __init__(self, parent):
        """VARIABLEN"""
        self.add_charge = False
        self.remove_charge = False
        self.counter = 0  # Anzahl an Ladungen

        """ROOT"""
        self.parent = parent
        self.parent.geometry("1200x800")  # Fenstergröße festsetzen
        self.parent.title("Visualisierung elektrischer Feldlinien")

        """MENÜ"""
        self.menubar = tk.Menu(self.parent)  # Menübar initialisieren

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
        # Padding zum Window Frame hinzufügen
        self.window_f.pack(padx=10, pady=10)

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

        # Eingabefeld
        self.canvas = tk.Canvas(
            self.plot_f, width=c.PLOT_SIZE, height=c.PLOT_SIZE)
        self.input_field = self.canvas.create_rectangle(
            0, 0, c.PLOT_SIZE, c.PLOT_SIZE, fill="white")
        self.canvas.tag_bind(
            self.input_field, "<Button-1>", self.onClick_inputField)

        # Sliders
        self.density_slider = tk.Scale(
            self.sliders_f, from_=0.0, to=2.0, digits=2, resolution=0.1, orient=HORIZONTAL, label="Feldliniendichte")
        self.density_slider.set(2.0)  # set Default Value of Slider
        self.thickness_slider = tk.Scale(
            self.sliders_f, from_=0.0, to=2.0, digits=2, resolution=0.1, orient=HORIZONTAL, label="Feldliniendicke")
        self.thickness_slider.set(1.0)  # set Default Value of Slider

        self.density_slider.grid(row=0, column=0)
        self.thickness_slider.grid(row=0, column=1)

        self.buttons_f.grid(column=0, row=0)
        self.canvas.grid(column=0, row=1)
        self.sliders_f.grid(column=0, row=2)

        self.window_f.pack()
        self.plot_f.grid(row=0, column=0)

        """TABELLE"""
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

    """BUTTON FUNKTIONEN"""

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
        h.eField(density=self.density_slider.get(),
                 thickness=self.thickness_slider.get())

    def onClick_inputField(self, event):
        x, y = event.x, event.y  # Mausklick-Position

        if self.add_charge:
            if len(h.charges) > 30:
                messagebox.showerror(
                    title="Zu viele Ladungen",
                    message="Es können maximal 30 Ladungen eingefügt werden.",
                )
            else:
                q = self.canvas.create_circle(
                    x, y, c.DEFAULT_CIRCLE_RADIUS, fill="red")
                coords = self.canvas.coords(q)
                self.canvas.tag_bind(q, "<Button-1>", self.onClick_charge)
                # Hinzufügen einer neuen Ladung zum Ladungsarray durch Berechnung der Mittelpunktskoordinaten des Kreises
                h.charges.append(
                    h.Charge(
                        1.0, [round((coords[0] + coords[2]) / 1200, 2),  # geteilt durch 1200 weil /2 wegen Durchschnitt und /600 wegen Koordinatensystem
                              round(1 - ((coords[1] + coords[3]) / 1200), 2)], q, None
                    )
                )
                record = self.table.insert(parent="", index="end", iid=self.counter, text="", values=(
                    h.charges[-1].pos, h.charges[-1].q))  # [-1] wählt letztes Element aus Liste aus
                # Tabelleneintrag zum Objekt hinzufügen, um diesen löschen zu können
                h.charges[-1].record = record
                self.counter += 1
                # Objekt-Attribute ausgeben
                print(h.charges[-1].__dict__)

    def onClick_charge(self, event):
        global counter
        x, y = event.x, event.y  # Mausklick-Position

        q = event.widget.find_closest(x, y)
        if self.remove_charge:
            for charge in h.charges:
                # prüfen, ob Ladung im Array dieselben Koordinaten wie die geklickte Ladung hat
                if self.canvas.coords(charge.item) == self.canvas.coords(q):
                    self.canvas.delete(q)
                    h.charges.remove(charge)
                    self.table.delete(charge.record)
        # Ladung auswählen, um Values zu ändern (muss noch erledigt werden)
        elif not self.remove_charge and not self.add_charge:
            pass

    def select_item(self, a):  # Argument a wird nicht benutzt, ist aber notwendig
        curItem = self.table.focus()
        values = self.table.item(curItem, 'values')
        user_inp = simpledialog.askfloat(
            "Änderung der Ladung", "Neuer Wert:", minvalue=-10.0, maxvalue=10.0)
        if user_inp is not None:
            self.table.item(curItem, values=(values[0], user_inp))
            for charge in h.charges:
                # prüfen, ob Tabelleneintrag der Ladung gleich dem ausgewählten Tabelleneintrag ist
                if curItem == charge.record:
                    charge.q = user_inp
                    # Farbe basierend auf mathematischen Operator ändern (<0:blue, =0:grey, >0:red)
                    self.canvas.itemconfig(charge.item, fill='blue') if user_inp < 0 else self.canvas.itemconfig(
                        charge.item, fill='grey') if user_inp == 0 else self.canvas.itemconfig(charge.item, fill='red')


root = tk.Tk()  # Root-Element initialisieren
window = App(root)
root.mainloop()
