import tkinter as tk

charges = []


class Charge:
    def __init__(self, q, pos, item):
        self.q = q
        self.pos = pos
        self.item = item


def _create_circle(self, x, y, r, **kwargs):  # x=xCoordinate, y=yCoordinate, r=radius
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
