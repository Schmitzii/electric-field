import tkinter as tk
import copy
import matplotlib.pyplot as plt
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


def E_point_charge(q, a, x, y):
    print(q*(x-a[0])/((x-a[0])**2+(y-a[1])**2)**(1.5),
          q*(y-a[1])/((x-a[0])**2+(y-a[1])**2)**(1.5))
    return q*(x-a[0])/((x-a[0])**2+(y-a[1])**2)**(1.5), \
        q*(y-a[1])/((x-a[0])**2+(y-a[1])**2)**(1.5)


def E_total(x, y, temp_charges):
    Ex, Ey = 0, 0
    for C in temp_charges:
        E = E_point_charge(C.q, C.pos, x, y)
        Ex = Ex + E[0]
        Ey = Ey + E[1]
    return [Ex, Ey]


def E_dir(t, y, temp_charges):
    Ex, Ey = E_total(y[0], y[1], temp_charges)
    n = np.sqrt(Ex**2+Ey*Ey)
    return [Ex/n, Ey/n]


def onClick_efield():
    # *copy list and copy objects as well (copy.copy() would only copy list but not objects inside the list -->charges would get changed as well)
    temp_charges = copy.deepcopy(charges)
    # *define temporarily new positions for plotting charges
    for C in temp_charges:
        C.pos[0] = round(C.pos[0] / 600, 2)  # round to 2 decimal places
        C.pos[1] = round((600 - C.pos[1]) / 600, 2)

    # calculate field lines
    R = 0.01
    # loop over all charges
    xs, ys = [], []
    for C in temp_charges:
        # plot field lines starting in current charge
        dt = 0.8 * R
        if C.q < 0:
            # because the electric field lines start only from positive charge,
            # skip the process when the current charges is negative.
            continue
        # loop over field lines starting in different directions
        # around current charge #(2*pi*r)
        # the bigger the numbers the more lines
        for alpha in np.linspace(0, 2*np.pi*31/32, 32):
            r = ode(E_dir)  # *helps to solve differential equation
            r.set_integrator('vode')
            r.set_f_params(temp_charges)
            x = [C.pos[0] + np.cos(alpha)*R]
            y = [C.pos[1] + np.sin(alpha)*R]
            r.set_initial_value([x[0], y[0]], 0)
            cnt = 0
            #! MAYBE CHANGE OF MAXIMUM RANGE OF FIELD LINES WOULD MINIMIZE CALCULATING TIME
            while r.successful():  # as long as the line doesnt end and integration is succesful
                Enorm = E_total(r.y[0], r.y[1], temp_charges)
                Enorm = (Enorm[0]**2 + Enorm[1]**2)**0.5
                a = 5
                dt = R*a*Enorm**(-0.4)
                # if cnt % 1000 == 0:
                #    print(r.y[0],r.y[1],Enorm,dt2)
                # cnt += 1
                r.integrate(r.t+dt)
                x.append(r.y[0])
                y.append(r.y[1])
                hit_charge = False
                # check if field line ends in some charge
                for C2 in temp_charges:
                    if np.sqrt((r.y[0]-C2.pos[0])**2+(r.y[1]-C2.pos[1])**2) < R:
                        hit_charge = True
                if hit_charge:
                    break  # end line
            xs.append(x)  # append point list to line list which is plotted
            ys.append(y)

    fig = plt.figure(figsize=(7, 7), facecolor="w")
    ax = fig.add_subplot(111)  # 1x1 grid, first subplot

    # plot field line
    for x, y in zip(xs, ys):  # *zip() aggregates lists and combines them into a tuple
        # plot line with color k and linewidth 0.8
        ax.plot(x, y, color="k", lw=0.8)

    # plot point charges
    for C in temp_charges:
        if C.q > 0:
            ax.plot(C.pos[0], C.pos[1], 'ro', ms=10 *
                    np.sqrt(C.q))  # ro -> red circle markers for charges
        if C.q < 0:
            ax.plot(C.pos[0], C.pos[1], 'bo', ms=10 *
                    np.sqrt(-C.q))  # bo -> blue circle markers for charges

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', 'datalim')
    plt.savefig('electric_field_lines_pyplot_wo_mayavi.png',
                dpi=250, bbox_inches="tight", pad_inches=0.02)
    plt.show()
    # py.iplot_mpl(fig)
