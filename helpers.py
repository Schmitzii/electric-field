import tkinter as tk

charges = []


class charge:
    def __init__(self, q, pos):
        self.q = q
        self.pos = pos


def _create_circle(self, x, y, r, **kwargs):  # x=xCoordinate, y=yCoordinate, r=radius
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
