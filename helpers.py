import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import plotly.offline as py
from scipy.integrate import ode as ode  # solve differential equations

charges = []

"""NOCH ERLEDIGEN:
-600 durch Konstante ersetzen
-generell neue Konstanten einführen
-Programm lesen und verstehen (besonders helpers.py)
-Auch Größe der Ladungen schon innerhalb des GUIs ändern, anstatt nur in matplotlib
"""


class Charge:
    def __init__(self, q, pos, item, record):
        self.q = q  # charge
        self.pos = pos  # position
        self.item = item  # item in canvas
        self.record = record  # record in table


def _create_circle(self, x, y, r, **kwargs):  # x=xCoordinate, y=yCoordinate, r=radius
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


"""CALCULATION ELECTRIC FIELD LINES"""

# *formula to calculate electric field due to a single charge
# *We know that E(r) \propto q * \vec{r}/r^3


def EFieldSingleCharge(charge, x, y):
    q = charge.q
    r0 = charge.pos
    distance = np.hypot(x - r0[0], y - r0[1])
    return q * (x - r0[0]) / (distance**3), q * (y - r0[1]) / (distance**3)


def eField(density):

    # We create two linear arrays with 64 points in the range -2, 2

    nx = 128
    ny = 128
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)

    # And then we use meshgrid that creates an array of coordinates for X and Y

    X, Y = np.meshgrid(x, y)

    # Initialize our field components to be zero

    Ex = np.zeros((ny, nx))
    Ey = np.zeros((ny, nx))

    # And iterate over charges. Since we apply superposition principle we can
    # calculate the field created by each charge separatly and add up all fields in
    # the field vectors

    for charge in charges:
        ex, ey = EFieldSingleCharge(charge, x=X, y=Y)
        Ex += ex
        Ey += ey

    # Create a subplot

    fig = plt.figure()
    splot = fig.add_subplot(111)

    # Color is determined by the magnitude of the field

    color = np.log(np.hypot(Ex, Ey))

    # Perform a plot of the vector arrows using streamplot

    splot.streamplot(x, y, Ex, Ey, color=color, linewidth=0.5,
                     cmap=plt.cm.inferno, density=density, arrowstyle='->', arrowsize=1)

    # Add circles for positive and negative charges

    qColors = {
        True: '#FF0000',
        False: '#0000FF'
    }
    for charge in charges:
        splot.add_artist(Circle(charge.pos, 0.02, color=qColors[charge.q > 0]))

    # Set labels and areas

    splot.set_xlabel('x')
    splot.set_ylabel('y')
    splot.set_xlim(0, 1)
    splot.set_ylim(0, 1)
    splot.set_aspect('equal')

    # Done

    plt.show()
