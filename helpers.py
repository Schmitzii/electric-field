import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

charges = []

"""NOCH ERLEDIGEN:
-600 durch Konstante ersetzen
-generell neue Konstanten einführen
-Programm lesen und verstehen (besonders helpers.py)
-Auch Größe der Ladungen schon innerhalb des GUIs ändern, anstatt nur in matplotlib
"""


class Charge:
    def __init__(self, q, pos, item, record):
        self.q = q  # Ladung
        self.pos = pos  # Position
        self.item = item  # Item in Canvas
        self.record = record  # Eintrag in Tabelle


def _create_circle(self, x, y, r, **kwargs):  # x=xKoordinate, y=yKoordinate, r=Radius
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


"""CALCULATION ELECTRIC FIELD LINES"""

# Formel, um elektrisches Feld durch eine Ladung zu berechnen


def EFieldSingleCharge(charge, x, y):
    q = charge.q
    r0 = charge.pos
    # calculates hypotenuse (distance between charge and wanted position)
    distance = np.hypot(x - r0[0], y - r0[1])
    return q * (x - r0[0]) / (distance**3), q * (y - r0[1]) / (distance**3)


def eField(density):

    # Arrays mit 256 Punkten von 0 bis 1
    # je größer die Anzahl an Punkten, desto genauer die Berechnung
    nx = 256
    ny = 256
    # teilt 0 - 1 in n Abschnitte ein (1/n, 2/n, 3/n...)
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)

    # Meshgrid verwenden, um Array aus Koordinaten für X und Y zu erstellen

    X, Y = np.meshgrid(x, y)

    # Initialize our field components to be zero

    # Arrays mit der gewünschten Form gefüllt mit Nullen wiedergeben
    Ex = np.zeros((ny, nx))
    Ey = np.zeros((ny, nx))

    # Für jede Ladung eigenes elektrisches Feld berechnen und zu Ex und Ey addieren

    for charge in charges:
        # Elektrisches Feld an jedem Punkt im Ausgabefeld für einzelne Ladung berechnen
        ex, ey = EFieldSingleCharge(charge, x=X, y=Y)
        Ex += ex
        Ey += ey

    # subplot erstellen

    fig = plt.figure(figsize=(8, 8))
    splot = fig.add_subplot(111)

    # Farbe abhängig von der Stärke des elektrischen Feldes

    color = np.log(np.hypot(Ex**2, Ey**2))

    # Mithilfe von streamplot Vektorfeld darstellen

    splot.streamplot(x, y, Ex, Ey, color=color, linewidth=1,
                     cmap=plt.cm.plasma, density=density, arrowstyle='->', arrowsize=1)

    # Kreise für positive und negative Ladungen hinzufügen

    qColors = {
        True: '#FF0000',
        False: '#0000FF'
    }
    for charge in charges:
        splot.add_artist(Circle(charge.pos, charge.q *
                         0.01, color=qColors[charge.q > 0]))  # Kreisgröße variiert je nach Ladungsmenge, default value 0.02

    # labels und sichtbaren Bereich festsetzen

    splot.set_xlabel('x')
    splot.set_ylabel('y')
    splot.set_xlim(0, 1)
    splot.set_ylim(0, 1)
    splot.set_aspect('equal')

    # Plot als png mit transparentem Hintergrund speichern
    plt.savefig("electric-field-output.png", transparent=True)
    # PLot anzeigen
    plt.show()
